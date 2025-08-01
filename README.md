# aind-analysis-wrapper

⚠️ **IMPORTANT: This is a Template Repository** ⚠️

This repository serves as an **example template** for building your own analysis workflows. **You should duplicate this repository and customize it for your specific analysis needs.** Do not modify this template directly - instead, create your own copy and build your analysis on top of the provided framework.

The **analysis wrapper** is a standardized framework for running large-scale data analysis workflows on cloud infrastructure. It processes job input models from the [job dispatcher](https://github.com/AllenNeuralDynamics/aind-analysis-job-dispatch), executes your custom analysis code, and automatically handles metadata tracking and result storage.

### What it does

The analysis wrapper:
1. **Receives** job input models containing data file locations and analysis parameters
2. **Executes** your custom analysis code on the specified datasets
3. **Tracks** metadata including inputs, parameters, code versions, and execution details
4. **Stores** results to cloud storage and writes metadata records to a document database
5. **Prevents** duplicate processing by checking if analysis has already been completed

### Environment Setup
The steps below are needed to configure the analysis wrapper
1. 

### Analysis Wrapper - User Defined Analysis Parameters
To help faciliate tracking of analysis parameters, a user should define their own pydantic model in the analysis wrapper. Follow steps below:

1. In the file /code/example_analysis_model.py, first rename this to user's own model.
2. Then add any fields that need to be kept track of. Recommeneded to add a field to tag the version run.
3. Additionally, for any numerical outputs - define these in the output model.
4. Once this is done, be sure to change lines 9, 38 66, and 69 to the user defined model, and user defined output model respectively.

### Testing Analysis Wrapper
To test, a reproducible run can be executed. **Be sure to set the dry run flag in the app panel to 1 so the results are not posted**.
