# aind-analysis-wrapper

The **analysis wrapper** is a standardized framework for running large-scale data analysis workflows on cloud infrastructure. It processes job input models from the [job dispatcher](https://github.com/AllenNeuralDynamics/aind-analysis-job-dispatch), executes your custom analysis code, and automatically handles metadata tracking and result storage.

## What it does

The analysis wrapper:
1. **Receives** job input models containing data file locations and analysis parameters
2. **Executes** your custom analysis code on the specified datasets
3. **Tracks** metadata including inputs, parameters, code versions, and execution details
4. **Stores** results to cloud storage and writes metadata records to a document database
5. **Prevents** duplicate processing by checking if analysis has already been completed

## Key Concepts

- **Job Input Model**: A standardized JSON structure (`AnalysisDispatchModel`) that contains S3 file locations, asset IDs, and analysis parameters for a specific dataset.

- **Analysis Specification**: A user-defined schema (`AnalysisSpecification`) that defines the parameters your analysis requires (e.g., filtering thresholds, algorithm settings).

- **Analysis Outputs**: A structured format (`AnalysisOutputs`) for your analysis results that will be saved and tracked.

- **Processing Record**: Comprehensive metadata about the analysis execution, including input data, parameters, code version, timestamps, and output locations.

- **Duplicate Detection**: The system automatically checks if an analysis with the same inputs and parameters has already been completed to avoid redundant processing.

## Installation and Setup

This is a [Code Ocean](https://codeocean.allenneuraldynamics.org/capsule/7739912/tree) capsule designed to be used as part of an analysis pipeline.

### Environment Configuration

Configure the following environment variables in Code Ocean:

| Variable | Description | Example |
|----------|-------------|---------|
| `DOCDB_COLLECTION` | Document database collection name for your project | `ephys_pipeline_results` |
| `CODEOCEAN_EMAIL` | Your Code Ocean email for tracking | `user@example.com` |
| `ANALYSIS_BUCKET` | S3 bucket where results will be stored | `s3://my-analysis-results` |

### Required Credentials

1. **Code Ocean API Token**: Create a secret in Code Ocean environment
   - See [Code Ocean API docs](https://docs.codeocean.com/user-guide/code-ocean-api/authentication)
   - Name the secret `CODEOCEAN_API_TOKEN`

2. **AWS Credentials**: Configure AWS access for S3 operations
   - Use the AWS assumable role credentials in the environment

### Installing Analysis Dependencies

Add any packages your analysis needs in the Code Ocean environment:
```dockerfile
# Example additions to Dockerfile
RUN pip install -U --no-cache-dir \
    scikit-learn==1.3.0 \
    matplotlib==3.7.1 \
    your-analysis-package==1.0.0
```

## Usage

### Step 1: Define Your Analysis Schema

First, customize the analysis specification in `analysis_wrapper/analysis_model.py`:

```python
class AnalysisSpecification(GenericModel):
    """Define the parameters your analysis needs"""
    
    analysis_name: str = Field(..., description="Name for your analysis")
    analysis_tag: str = Field(..., description="Tag to organize results")
    
    # Add your custom parameters here
    threshold: float = Field(..., description="Analysis threshold value")
    method: str = Field(..., description="Analysis method to use")
    n_components: int = Field(default=10, description="Number of components")

class AnalysisOutputs(GenericModel):
    """Define the structure of your analysis outputs"""
    
    # Add your custom output fields here
    filtered_units: List[str] = Field(..., description="List of filtered unit IDs")
    quality_metrics: Dict[str, float] = Field(..., description="Quality metrics")
    plots_generated: List[str] = Field(..., description="List of generated plot files")
```

### Step 2: Create Analysis Parameters File

Create an `distributed_paramters.json` file with your analysis settings:

```json
[
    {
        "analysis_name": "Unit Quality Filtering",
        "analysis_tag": "v1.0_strict_criteria",
        "threshold": 0.05,
        "method": "isolation_distance",
        "n_components": 15
    }
]
```
This file will need to be stored in your `/data/job_dict` directory

### Step 3: Implement Your Analysis Logic

Modify the `run_analysis` function in `analysis_wrapper/run_capsule.py`:

```python
def run_analysis(analysis_dispatch_inputs: AnalysisDispatchModel, **parameters) -> None:
    processing = construct_processing_record(analysis_dispatch_inputs, **parameters)
    
    # Check if analysis already completed
    if docdb_record_exists(processing):
        logger.info("Record already exists, skipping.")
        return

    ### YOUR ANALYSIS CODE GOES HERE ###
    
    # Example: Load data from S3
    results = {}
    for location in analysis_dispatch_inputs.file_location:
        # Process each file
        with NWBZarrIO(location, 'r') as io:
            nwbfile = io.read()
            
        # Run your analysis
        filtered_units = run_quality_filtering(
            nwbfile, 
            threshold=parameters['threshold'],
            method=parameters['method']
        )
        
        results[location] = filtered_units
    
    # Save results to /results folder
    with open('/results/filtered_units.json', 'w') as f:
        json.dump(results, f)
    
    # Generate plots
    create_quality_plots(results, '/results/quality_plots.png')
    
    # Define structured outputs
    processing.output_parameters = AnalysisOutputs(
        filtered_units=list(results.keys()),
        quality_metrics={"mean_threshold": parameters['threshold']},
        plots_generated=["quality_plots.png"]
    )
    
    # Automatically save results and metadata
    write_results_and_metadata(processing, ANALYSIS_BUCKET)
    logger.info("Successfully wrote record to docdb and s3")
```

### Step 4: Input Data

The wrapper expects two types of input:

#### 1. Job Input Models (from job dispatcher)
JSON files in `/data/job_dict/` containing:
```json
{
    "s3_location": ["s3://bucket/path/to/dataset"],
    "asset_id": ["data-asset-id"],
    "asset_name": ["dataset_name"],
    "file_location": ["s3://bucket/path/to/data.nwb"],
    "distributed_parameters": {
        "custom_param": "value"
    }
}
```

#### 2. Analysis Parameters
File at `/data/analysis_parameters.json` containing your analysis configuration.

## Advanced Features

### Custom Parameter Parsing

You can also parse parameters from command line arguments:

```python
# Uncomment this section in run_capsule.py
if analysis_specs is None:
    analysis_specs = AnalysisSpecificationCLI().model_dump_json()
```

### Batch Processing

The wrapper automatically processes all job models found in `/data/job_dict/`:

```python
input_model_paths = tuple(utils.DATA_PATH.glob('job_dict/*'))
for model_path in input_model_paths:
    # Process each job model
    run_analysis(analysis_dispatch_inputs, **analysis_specification)
```

### Distributed Parameters

Handle job-specific parameters from the dispatcher:

```python
def run_analysis(analysis_dispatch_inputs: AnalysisDispatchModel, **parameters) -> None:
    # Access distributed parameters from the input model
    if analysis_dispatch_inputs.distributed_parameters:
        custom_params = analysis_dispatch_inputs.distributed_parameters
        # Merge with global parameters
        parameters.update(custom_params)
```

## Output and Results

### Result Storage

- **Local Results**: Save files to `/results/` directory during analysis
- **S3 Storage**: Results automatically uploaded to the configured `ANALYSIS_BUCKET`
- **Metadata Database**: Processing records written to the configured `DOCDB_COLLECTION`

### Metadata Tracking

Each analysis run creates a comprehensive processing record including:
- Input data locations and asset IDs
- Analysis parameters and code version
- Execution timestamps and environment details
- Output file locations and analysis results
- Error messages (if any)

### Querying Results

Use the example notebook to query your analysis results:

```python
from aind_analysis_results.metadata import get_docdb_records_partial
from aind_analysis_results.result_files import list_results_files

# Get records for specific analysis
records = get_docdb_records_partial(
    analysis_name="Unit Quality Filtering",
    latest_only=True
)

# List result files for a record
files = list_results_files(records[0])

# Download and examine results
import fsspec
fs = fsspec.filesystem('s3')
with fs.open(files[0]) as f:
    results = json.load(f)
```

## Integration with Pipeline

This wrapper is typically used as part of a larger analysis pipeline:

1. **[Job Dispatcher](https://github.com/AllenNeuralDynamics/aind-analysis-job-dispatch)** → Creates job input models
2. **Analysis Wrapper** (this repository) → Processes each job
3. **Result Analysis** → Query and analyze results using the metadata database

See the [pipeline template](https://github.com/AllenNeuralDynamics/aind-analysis-pipeline-template) for a complete workflow example.

## Examples

### Electrophysiology Analysis

```python
def run_analysis(analysis_dispatch_inputs: AnalysisDispatchModel, **parameters) -> None:
    # ... setup code ...
    
    spike_data = []
    for location in analysis_dispatch_inputs.file_location:
        with NWBZarrIO(location, 'r') as io:
            nwbfile = io.read()
            
        # Extract spike times
        units = nwbfile.units
        spike_times = units['spike_times'][:]
        
        # Calculate ISI violations
        isi_violations = calculate_isi_violations(
            spike_times, 
            cutoff=parameters['isi_violations_cutoff']
        )
        
        spike_data.append({
            'asset_id': analysis_dispatch_inputs.asset_id[0],
            'isi_violations': isi_violations
        })
    
    # Save results
    with open('/results/spike_analysis.json', 'w') as f:
        json.dump(spike_data, f)
    
    processing.output_parameters = AnalysisOutputs(
        isi_violations=[d['isi_violations'] for d in spike_data],
        additional_info=f"Processed {len(spike_data)} datasets"
    )
```

### Behavioral Analysis

```python
def run_analysis(analysis_dispatch_inputs: AnalysisDispatchModel, **parameters) -> None:
    # ... setup code ...
    
    for location in analysis_dispatch_inputs.file_location:
        with NWBZarrIO(location, 'r') as io:
            nwbfile = io.read()
        
        # Extract behavioral data
        trials = nwbfile.trials
        reaction_times = trials['reaction_time'][:]
        
        # Analyze performance
        performance_metrics = analyze_behavior(
            reaction_times,
            method=parameters['analysis_method']
        )
        
        # Create visualization
        plot_path = f'/results/behavior_{analysis_dispatch_inputs.asset_id[0]}.png'
        create_behavior_plot(performance_metrics, plot_path)
    
    processing.output_parameters = AnalysisOutputs(
        performance_score=performance_metrics['score'],
        plot_files=[plot_path]
    )
```

## Troubleshooting

### Common Issues

**Missing environment variables**: Ensure all required environment variables are set in Code Ocean
**S3 access errors**: Verify AWS credentials are properly configured
**Duplicate processing**: Check if `docdb_record_exists` is working correctly
**Import errors**: Add missing packages to your environment

### Debugging

Enable detailed logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check processing records:
```python
# View what would be written to the database
processing = construct_processing_record(analysis_dispatch_inputs, **parameters)
print(processing.model_dump_json(indent=2))
```

## Development

### Local Testing

```bash
# Clone the repository
git clone <repository-url>
cd aind-analysis-wrapper/code

# Install dependencies
pip install -e .

# Create test data
mkdir -p /data/job_dict
echo '{"s3_location": ["test"], "asset_id": ["test"]}' > /data/job_dict/test.json
echo '{"analysis_name": "test"}' > /data/analysis_parameters.json

# Run analysis
python -m analysis_wrapper.run_capsule
```

### Code Structure

- `analysis_wrapper/run_capsule.py`: Main execution logic and analysis orchestration
- `analysis_wrapper/analysis_model.py`: Analysis parameter and output schemas  
- `analysis_wrapper/utils.py`: Utility functions and path definitions
- `example_notebooks/querying_results.ipynb`: Example of how to query analysis results

## Additional Resources

- [Job Dispatcher](https://github.com/AllenNeuralDynamics/aind-analysis-job-dispatch): Creates the input models for this wrapper
- [Pipeline Template](https://github.com/AllenNeuralDynamics/aind-analysis-pipeline-template): Complete pipeline example
- [Analysis Results Utils](https://github.com/AllenNeuralDynamics/analysis-pipeline-utils): Core utilities for metadata and result handling
- [Code Ocean Documentation](https://docs.codeocean.com/): Platform-specific documentation
