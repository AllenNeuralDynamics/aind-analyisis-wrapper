import json
import logging
import os
from pathlib import Path
from typing import Any

from aind_analysis_results.metadata import construct_processing_record, docdb_record_exists, write_results_and_metadata
from aind_analysis_results.analysis_dispatch_model import AnalysisDispatchModel
from analysis_wrapper.example_analysis_model import (
    ExampleAnalysisSpecification, ExampleAnalysisSpecificationCLI, ExampleAnalysisOutputs
)

DATA_PATH = Path("/data") # TODO: don't hardcode 
ANALYSIS_BUCKET = os.getenv("ANALYSIS_BUCKET")
logger = logging.getLogger(__name__)


def run_analysis(analysis_dispatch_inputs: AnalysisDispatchModel, **parameters) -> None:
    processing = construct_processing_record(analysis_dispatch_inputs, **parameters)
    if docdb_record_exists(processing):
        logger.info("Record already exists, skipping.")
        return

    ### Execute analysis and write to results folder
    ### using the passed parameters
    ### SEE EXAMPLE BELOW
    # Use NWBZarrIO to reads
    # for location in analysis_dispatch_inputs.file_location:
    #     with NWBZarrIO(location, 'r') as io:
    #         nwbfile = io.read()
    
    # acquisition_keys = list(nwbfile.acquisition.keys())
    # with open('/results/acquisition_keys.json', 'w') as f:
    #     json.dump(acquisition_keys, f)
        
    processing.output_parameters = ExampleAnalysisOutputs(
        isi_violations=["example_violation_1", "example_violation_2"],
        additional_info="This is an example of additional information about the analysis."
    )
    write_results_and_metadata(processing, ANALYSIS_BUCKET)
    logger.info(f"Successfully wrote record to docdb and s3")


# Most of the below code will not need to change per-analysis
# and will be moved to a shared library
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    input_model_paths = tuple(DATA_PATH.glob('job_dict/*'))
    logger.info(f"Found {len(input_model_paths)} input job models to run analysis on.")
    analysis_model_from_json = None
    analysis_spec = None

    analysis_spec_path = tuple(DATA_PATH.glob("analysis_parameters.json"))
    if analysis_spec_path:
        with open(analysis_spec_path[0], "r") as f:
            analysis_spec = json.load(f)

        logger.info(
            "Found analysis specification json. Parsing it"
        )
    else:
        logger.info(
            "No analysis parameters json found. Defaulting to parameters passed in via input arguments"
        )

    if analysis_spec is not None:
        analysis_dict_from_json = ExampleAnalysisSpecification(**analysis_spec).model_construct().model_dump()
    else:
        analysis_dict_from_json = {}

    analysis_model_cli = ExampleAnalysisSpecificationCLI()
    cli_data = analysis_model_cli.model_dump()

    logger.info(f"Analysis Specification: {analysis_spec}")

    for model_path in input_model_paths:
        with open(model_path, "r") as f:
            analysis_dispatch_inputs = AnalysisDispatchModel.model_validate(json.load(f))
        
        if analysis_dispatch_inputs.distributed_parameters:
            logger.info("Found distributed parameters from dispatch. Will combine, with distributed parameters taking priority")
            distributed_parameters = analysis_dispatch_inputs.distributed_parameters
        else:
            distributed_parameters = {}
        
        # Combine parameters - priority: json < command line < distributed parameters
        merged_parameters = {**analysis_dict_from_json, **cli_data, **distributed_parameters} 
        analysis_specification = ExampleAnalysisSpecification.model_validate(merged_parameters).model_dump()
        logger.info(f"Running with analysis specs {analysis_specification}")
        run_analysis(analysis_dispatch_inputs, **analysis_specification)
