# aind-analysis-wrapper

This capsule is the 2nd one in this pipeline: PUT PIPELINE LINK that runs the analysis on the input model and analysis specification. Currently assumes running in Code Ocean

### Setup
There are several things that need to be setup. The first of these is some environment variables. In the environment tab, set the `DOCDB_COLLECTION` variable to the project collection you want to write to. In addition, you will need to create a secret for a code ocean token. See [CodeOcean docs](https://docs.codeocean.com/user-guide/code-ocean-api/authentication). After this, add any necessary packages you need to run analysis in the environment. 

### Inputs
There are 2 inputs currently to this capsule. The first is the output of the the [job dispatch capsule](https://codeocean.allenneuraldynamics.org/capsule/9303168/tree). The second is the analysis specification. This can be provided in 2 ways, either through a json file or the command line. An example of using the json file with the required schema is below:
```json
[
    {
        
        "analysis_name": "Unit Yield",
        "analysis_version": "v0.0.5",
        "analysis_libraries": [
            "aind-ephys-utils"
        ],
        "analysis_parameters": {
            "isi_violations": 0.5
        },
        "s3_output_bucket": "aind-scratch-data/arjun.sridhar"
    },

    {
        
        "analysis_name": "Unit Filtering",
        "analysis_version": "v0.0.5",
        "analysis_libraries": [
            "aind-ephys-utils"
        ],
        "analysis_parameters": {
            "isi_violations": 0.5, "amplitude_cutoff": 0.1
        },
        "s3_output_bucket": "aind-scratch-data/arjun.sridhar"
    }
]
```

### Running Analysis
In the `run_analysis` function in `analysis_wrapper/run_capsule.py`, add in relevant code and save necessary output to the `/results` folder. The results folder will be put in the output bucket specified in the analysis specification and the metadata for the analysis will be written to the docdb collection specified from the steps above.
