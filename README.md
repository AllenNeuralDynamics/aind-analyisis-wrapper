# aind-analysis-wrapper

⚠️ **IMPORTANT: This is a Template Repository** ⚠️

This repository serves as an **example template** for building your own analysis workflows. **You should duplicate this repository and customize it for your specific analysis needs.** Do not modify this template directly - instead, create your own copy and build your analysis on top of the provided framework.

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

## Getting Started: Creating Your Analysis

### Step 0: Duplicate This Repository

**Before anything else**, you need to create your own copy of this template:

1. **In Code Ocean**: Navigate to this capsule and click "Duplicate" to create your own version
2. **In GitHub**: Fork this repository or create a new repository using this as a template
3. **Name your analysis**: Give your duplicated repository a descriptive name (e.g., `my-ephys-analysis-wrapper`, `behavior-analysis-pipeline`)

This template provides the essential framework components:
- ✅ Infrastructure for processing job input models
- ✅ Metadata tracking and result storage
- ✅ Integration with the AIND analysis ecosystem
- ✅ Example schema definitions and analysis structure

**What you need to customize:**
- 🔧 Analysis schema in `analysis_wrapper/analysis_dispatch_model.py`
- 🔧 Your analysis logic in `analysis_wrapper/run_capsule.py`
- 🔧 Dependencies in the environment files
- 🔧 Any additional modules your analysis requires

## Installation and Setup

After duplicating this template, you'll have your own [Code Ocean](https://codeocean.allenneuraldynamics.org/capsule/7739912/tree) capsule to customize for your analysis.

### Environment Configuration

Configure the following environment variables in your duplicated Code Ocean capsule:

| Variable | Description | Example |
|----------|-------------|---------|
| `DOCDB_COLLECTION` | Document database collection name for your project | `ephys_pipeline_results` |
| `CODEOCEAN_EMAIL` | Your Code Ocean email for tracking | `user@example.com` |
| `ANALYSIS_BUCKET` | S3 bucket where results will be stored | `s3://my-analysis-results` |

### Required Credentials

1. **Code Ocean API Token**: Create a secret in Code Ocean environment
   - See [Code Ocean API docs](https://docs.codeocean.com/user-guide/code-ocean-api/authentication)
   - Name the secret `CODEOCEAN_API_TOKEN`
   - **Important**: Configure the token with **read-only permissions** for security

2. **AWS Credentials**: Configure AWS access for S3 operations
   - Use the AWS assumable role credentials in the environment

### Installing Analysis Dependencies

Add any packages your specific analysis needs in your Code Ocean environment:
```dockerfile
# Example additions to Dockerfile for your analysis
RUN pip install -U --no-cache-dir \
    scikit-learn==1.3.0 \
    matplotlib==3.7.1 \
    seaborn==0.12.0 \
    your-specific-analysis-package==1.0.0
```

## Building Your Analysis

### Step 1: Define Your Analysis Schema (CRITICAL)

**This is the most important step** - you must customize the analysis specification in `analysis_wrapper/analysis_dispatch_model.py` to match your analysis requirements.

#### Understanding the Analysis Schema

The `analysis_dispatch_model.py` file contains three key classes that define your analysis:

1. **`AnalysisSpecification`**: Defines the input parameters your analysis accepts
2. **`AnalysisOutputs`**: Defines the structure of your analysis results  
3. **`AnalysisSpecificationCLI`**: Enables command-line parameter parsing (optional)

#### Customizing AnalysisSpecification

Replace the example schema with your analysis parameters:

```python
from typing import List, Optional, Union
from aind_data_schema.base import GenericModel
from pydantic import Field
from pydantic_settings import BaseSettings

class AnalysisSpecification(GenericModel):
    """
    Define ALL parameters your analysis needs.
    This schema will be used by the job dispatcher and validated automatically.
    """
    
    # Required fields - customize these for your analysis
    analysis_name: str = Field(..., description="Name identifying your analysis type")
    analysis_tag: str = Field(..., description="Version/variant tag for organizing results")
    
    # Add your analysis-specific parameters here
    # Examples for different analysis types:
    
    # For spike sorting quality analysis:
    isi_violation_threshold: float = Field(..., description="ISI violation threshold for unit quality")
    amplitude_cutoff: float = Field(default=0.1, description="Amplitude cutoff for unit filtering")
    
    # For behavioral analysis:
    # reaction_time_window: List[float] = Field(..., description="Time window [start, end] for reaction time analysis")
    # trial_types: List[str] = Field(..., description="List of trial types to include")
    
    # For imaging analysis:
    # roi_threshold: float = Field(..., description="Threshold for ROI detection")
    # baseline_frames: int = Field(default=30, description="Number of frames for baseline calculation")
    
    # For custom analysis parameters:
    # custom_param_1: str = Field(..., description="Description of your parameter")
    # custom_param_2: Optional[int] = Field(default=None, description="Optional parameter")

class AnalysisOutputs(GenericModel):
    """
    Define the structure of your analysis results.
    This ensures consistent output format and enables result querying.
    """
    
    # Add fields that describe your analysis outputs
    # Examples:
    
    # For spike analysis:
    filtered_units: List[str] = Field(..., description="List of unit IDs that passed filtering")
    quality_metrics: dict = Field(..., description="Dictionary of quality metrics per unit")
    
    # For behavioral analysis:
    # performance_score: float = Field(..., description="Overall performance score")
    # trial_success_rate: float = Field(..., description="Percentage of successful trials")
    
    # For any analysis:
    plots_generated: List[str] = Field(default_factory=list, description="List of plot filenames generated")
    summary_statistics: Optional[dict] = Field(default=None, description="Summary statistics from analysis")
    
class AnalysisSpecificationCLI(AnalysisSpecification, BaseSettings, cli_parse_args=True):
    """
    Enables command-line parsing of analysis parameters.
    Only needed if you want to override parameters from command line.
    """
    pass
```

#### Key Guidelines for Schema Design:

1. **Be Specific**: Each parameter should have a clear description and appropriate type
2. **Use Validation**: Leverage Pydantic's validation features (e.g., `Field(gt=0)` for positive numbers)
3. **Set Defaults**: Provide sensible defaults for optional parameters
4. **Document Everything**: Good descriptions help users understand parameters and enable automatic documentation

#### Example Schemas for Different Analysis Types:

**Electrophysiology Analysis:**
```python
class AnalysisSpecification(GenericModel):
    analysis_name: str = Field(..., description="Analysis identifier")
    analysis_tag: str = Field(..., description="Analysis version/variant")
    isi_violations_cutoff: float = Field(..., description="ISI violations threshold (0-1)")
    amplitude_cutoff_threshold: float = Field(default=0.1, description="Amplitude cutoff threshold")
    isolation_distance_threshold: float = Field(default=20.0, description="Minimum isolation distance")
    spike_count_threshold: int = Field(default=100, description="Minimum spike count for inclusion")
```

**Behavioral Analysis:**
```python
class AnalysisSpecification(GenericModel):
    analysis_name: str = Field(..., description="Analysis identifier") 
    analysis_tag: str = Field(..., description="Analysis version/variant")
    response_window: List[float] = Field(..., description="Response window [start, end] in seconds")
    trial_types: List[str] = Field(..., description="Trial types to analyze")
    minimum_trials: int = Field(default=50, description="Minimum trials required for analysis")
    outlier_threshold: float = Field(default=3.0, description="Standard deviations for outlier removal")
```

### Step 2: Set Up Analysis Parameters

Create an `analysis_parameters.json` file in the `/data/analysis_parameters/` folder. The structure depends on whether you're running a single analysis configuration or multiple variants:

**Choose ONE of these approaches:**

**Option A - Single Analysis (same parameters for all datasets):**
```json
{
    "analysis_parameter": {
        "analysis_name": "Your Analysis Name",
        "analysis_tag": "v1.0_baseline",
        "your_parameter_1": 0.05,
        "your_parameter_2": "method_name"
    }
}
```

**Option B - Distributed Analysis (multiple parameter sets):**
```json
{
    "distributed_parameters": [
        {
            "analysis_name": "Your Analysis Name",
            "analysis_tag": "v1.0_strict",
            "your_parameter_1": 0.03,
            "your_parameter_2": "method_a"
        },
        {
            "analysis_name": "Your Analysis Name", 
            "analysis_tag": "v1.0_lenient",
            "your_parameter_1": 0.07,
            "your_parameter_2": "method_b"
        }
    ]
}
```

**Important**: Replace `your_parameter_1`, `your_parameter_2`, etc. with the actual parameter names you defined in your `AnalysisSpecification` schema.
### Step 3: Implement Your Analysis Logic

**This is where you build your actual analysis.** Modify the `run_analysis` function in `analysis_wrapper/run_capsule.py` to implement your specific analysis:

```python
def run_analysis(analysis_dispatch_inputs: AnalysisDispatchModel, **parameters) -> None:
    """
    This is YOUR analysis function - customize it completely for your needs.
    The framework handles job management, metadata, and result storage.
    You focus on the science!
    """
    
    # Create processing record (framework handles this)
    processing = construct_processing_record(analysis_dispatch_inputs, **parameters)
    
    # Check if analysis already completed (framework handles this)
    if docdb_record_exists(processing):
        logger.info("Record already exists, skipping.")
        return

    ### REPLACE THIS SECTION WITH YOUR ANALYSIS CODE ###
    
    # Initialize results structure
    analysis_results = {}
    plots_created = []
    
    # Process each data file
    for i, location in enumerate(analysis_dispatch_inputs.file_location):
        logger.info(f"Processing file {i+1}/{len(analysis_dispatch_inputs.file_location)}: {location}")
        
        # STEP 1: Load your data
        # Replace this with your data loading logic
        # Examples:
        # - For NWB files: with NWBHDF5IO(location, 'r') as io: nwbfile = io.read()
        # - For other formats: data = your_custom_loader(location)
        
        try:
            # Example for NWB files (replace with your data loading)
            with NWBZarrIO(location, 'r') as io:
                nwbfile = io.read()
            
            # STEP 2: Run your analysis
            # Replace this with your analysis logic
            result = your_analysis_function(
                nwbfile,
                parameter_1=parameters['your_parameter_1'],
                parameter_2=parameters['your_parameter_2']
                # Add all parameters from your AnalysisSpecification
            )
            
            # STEP 3: Store results
            analysis_results[location] = result
            
            # STEP 4: Generate plots/visualizations (optional)
            plot_filename = f'analysis_plot_{i}.png'
            your_plotting_function(result, f'/results/{plot_filename}')
            plots_created.append(plot_filename)
            
        except Exception as e:
            logger.error(f"Failed to process {location}: {str(e)}")
            # Decide how to handle errors - continue or stop
            continue  # or raise e to stop processing
    
    # STEP 5: Save summary results
    # Save your results in whatever format makes sense
    results_file = '/results/analysis_summary.json'
    with open(results_file, 'w') as f:
        json.dump(analysis_results, f, indent=2, default=str)
    
    # STEP 6: Create structured outputs (must match your AnalysisOutputs schema)
    processing.output_parameters = AnalysisOutputs(
        # Replace these with your actual output fields
        filtered_units=list(analysis_results.keys()),  # Example
        quality_metrics={"processed_files": len(analysis_results)},  # Example
        plots_generated=plots_created,
        summary_statistics={"total_processed": len(analysis_results)}
    )
    
    # Framework handles saving to S3 and database
    write_results_and_metadata(processing, ANALYSIS_BUCKET)
    logger.info("Successfully wrote record to docdb and s3")

# ADD YOUR CUSTOM ANALYSIS FUNCTIONS HERE
def your_analysis_function(data, parameter_1, parameter_2, **kwargs):
    """
    Implement your specific analysis logic here.
    
    Args:
        data: Your loaded data (NWB file, DataFrame, etc.)
        parameter_1, parameter_2: Parameters from your AnalysisSpecification
        **kwargs: Any additional parameters
    
    Returns:
        Your analysis results in whatever format you need
    """
    # Your analysis code here
    # Examples:
    # - Spike train analysis
    # - Behavioral metric calculation  
    # - Image processing
    # - Machine learning model fitting
    
    result = {
        "analysis_output": "your_results_here",
        "metrics": {"metric1": 0.5, "metric2": 0.8},
        "processed_timestamp": datetime.now().isoformat()
    }
    
    return result

def your_plotting_function(results, output_path):
    """
    Create visualizations of your results.
    
    Args:
        results: Output from your_analysis_function
        output_path: Where to save the plot
    """
    import matplotlib.pyplot as plt
    
    # Your plotting code here
    fig, ax = plt.subplots(1, 1, figsize=(10, 6))
    # Create your plots...
    ax.plot([1, 2, 3], [1, 4, 2])  # Replace with your plotting logic
    ax.set_title("Your Analysis Results")
    
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    plt.close()
```

#### Key Points for Implementation:

1. **Focus on the science**: The framework handles job management, metadata, and storage
2. **Use your schema**: All parameters from your `AnalysisSpecification` are available in the `parameters` dict
3. **Handle errors gracefully**: Decide whether to continue or stop on individual file failures
4. **Save intermediate results**: Use `/results/` directory for all output files
5. **Match your output schema**: Ensure `AnalysisOutputs` matches what you actually produce

### Step 4: Test Your Analysis

Before running on real data, test your analysis locally:

```bash
# In your duplicated repository
cd code

# Install dependencies  
pip install -e .

# Create test data that matches your schema
mkdir -p /data/job_dict
mkdir -p /data/analysis_parameters

# Create a test job input model
echo '{"s3_location": ["test"], "asset_id": ["test"], "file_location": ["path/to/test/file"]}' > /data/job_dict/test.json

# Create test parameters using YOUR schema
echo '{
    "analysis_parameter": {
        "analysis_name": "test_analysis",
        "analysis_tag": "test_run",
        "your_parameter_1": 0.05,
        "your_parameter_2": "test_value"
    }
}' > /data/analysis_parameters/analysis_parameters.json

# Run your analysis
python -m analysis_wrapper.run_capsule
```

## Understanding the Framework Components

This template provides several key components that you can build upon:

### Core Files You Should Modify:

1. **`analysis_wrapper/analysis_dispatch_model.py`** - Define your analysis schema (REQUIRED)
2. **`analysis_wrapper/run_capsule.py`** - Implement your analysis logic (REQUIRED)  
3. **`environment/`** - Add your analysis dependencies (LIKELY NEEDED)

### Core Files You Should NOT Modify:

1. **`analysis_wrapper/utils.py`** - Framework utilities for file handling and paths
2. **Framework integration code** - Metadata tracking, S3 upload, database operations

## Using Your Analysis in Production

Once you've built and tested your analysis:

1. **Deploy your capsule** in Code Ocean with proper environment variables
2. **Use with the job dispatcher** to process large datasets
3. **Query results** using the provided example notebooks
4. **Share your analysis** by making your capsule public or sharing with collaborators

## Framework Features (Built-in)

The following features are provided by the framework and work automatically:

### Automatic Parameter Parsing

The framework automatically parses parameters from your analysis_parameters.json file. You can also enable command-line parsing:

```python
# Uncomment this section in run_capsule.py
if analysis_specs is None:
    analysis_specs = AnalysisSpecificationCLI().model_dump_json()
```

### Automatic Batch Processing

The framework automatically processes all job models found in `/data/job_dict/`. You don't need to modify this:

```python
input_model_paths = tuple(utils.DATA_PATH.glob('job_dict/*'))
for model_path in input_model_paths:
    # Process each job model
    run_analysis(analysis_dispatch_inputs, **analysis_specification)
```

### Automatic Distributed Parameter Handling

The framework automatically handles job-specific parameters from the dispatcher. In your analysis function, these are merged into the `parameters` dict:

```python
def run_analysis(analysis_dispatch_inputs: AnalysisDispatchModel, **parameters) -> None:
    # All parameters (both from file and job-specific) are automatically
    # available in the parameters dict - no extra code needed!
    
    your_threshold = parameters['your_threshold_parameter']
    your_method = parameters['your_method_parameter']
    # Use these in your analysis...
```

## Automatic Framework Features

The following features work automatically - you don't need to implement them:

### ✅ Result Storage and Metadata
- Results automatically uploaded to S3
- Metadata automatically written to document database  
- Processing records include full provenance information

### ✅ Duplicate Detection
- Framework checks if analysis with same inputs/parameters already exists
- Prevents redundant processing automatically

### ✅ Error Handling and Logging
- Comprehensive logging throughout the framework
- Error messages captured and stored with results

### ✅ Parameter Validation
- Your `AnalysisSpecification` schema automatically validates input parameters
- Clear error messages for invalid parameters

## Integration with Analysis Pipeline

Your analysis wrapper integrates into the larger AIND analysis ecosystem:

1. **[Job Dispatcher](https://github.com/AllenNeuralDynamics/aind-analysis-job-dispatch)** → Discovers data and creates job input models
2. **Your Analysis Wrapper** (this repository) → Processes each job with your custom analysis
3. **Result Querying** → Use metadata database to find and download results

See the [pipeline template](https://github.com/AllenNeuralDynamics/aind-analysis-pipeline-template) for complete workflow examples.

## Troubleshooting Your Analysis

### Common Issues When Building Your Analysis

**Schema validation errors**: Check that your `AnalysisSpecification` matches your parameter files exactly
**Import errors**: Add missing packages to your environment configuration
**File loading errors**: Ensure your data loading code handles the file formats in your datasets
**Memory issues**: Consider processing data in chunks for large datasets

### Debugging Your Analysis

Enable detailed logging in your analysis code:
```python
import logging
logging.basicConfig(level=logging.DEBUG)

def run_analysis(analysis_dispatch_inputs: AnalysisDispatchModel, **parameters) -> None:
    logger.info(f"Starting analysis with parameters: {parameters}")
    logger.info(f"Processing {len(analysis_dispatch_inputs.file_location)} files")
    
    # Add logging throughout your analysis
    for i, location in enumerate(analysis_dispatch_inputs.file_location):
        logger.info(f"Processing file {i+1}: {location}")
        # Your analysis code...
```

Test your schema and outputs:
```python
# Test your schema validation
from your_analysis_wrapper.analysis_dispatch_model import AnalysisSpecification, AnalysisOutputs

# Validate your parameters
params = {"analysis_name": "test", "your_param": 0.05}
spec = AnalysisSpecification(**params)  # Should not raise errors

# Test your outputs structure  
outputs = AnalysisOutputs(your_output_field="test_value")
```

## Development and Testing

### Local Development of Your Analysis

```bash
# Clone YOUR duplicated repository
git clone <your-analysis-repository-url>
cd your-analysis-wrapper/code

# Install in development mode
pip install -e .

# Create test data matching YOUR schema
mkdir -p /data/job_dict /data/analysis_parameters

# Test with minimal data
echo '{"s3_location": ["test"], "asset_id": ["test"], "file_location": ["path/to/test/file"]}' > /data/job_dict/test.json

# Use YOUR analysis parameters
echo '{
    "analysis_parameter": {
        "analysis_name": "test", 
        "analysis_tag": "test_run",
        "your_custom_parameter": "test_value"
    }
}' > /data/analysis_parameters/analysis_parameters.json

# Run YOUR analysis
python -m analysis_wrapper.run_capsule
```

## Additional Resources for Building Your Analysis

- **[Job Dispatcher](https://github.com/AllenNeuralDynamics/aind-analysis-job-dispatch)**: Creates the input models for your analysis wrapper  
- **[Pipeline Template](https://github.com/AllenNeuralDynamics/aind-analysis-pipeline-template)**: Complete pipeline example showing how to use your analysis
- **[Analysis Results Utils](https://github.com/AllenNeuralDynamics/analysis-pipeline-utils)**: Core utilities for metadata and result handling
- **[Code Ocean Documentation](https://docs.codeocean.com/)**: Platform-specific documentation for deployment

## Getting Help

When building your analysis:

1. **Start simple**: Begin with a minimal analysis and gradually add complexity
2. **Test locally**: Always test your analysis with sample data before deploying  
3. **Use the examples**: The provided examples show common patterns for different analysis types
4. **Check the schema**: Ensure your `AnalysisSpecification` and `AnalysisOutputs` match your implementation

Remember: **This repository is your starting point, not your final destination.** Build your analysis, make it your own, and contribute back to the community by sharing your analysis patterns and approaches!
