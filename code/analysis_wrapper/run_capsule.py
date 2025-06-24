import json
import logging

from aind_analysis_results.metadata import construct_processing_record, docdb_record_exists, write_results_and_metadata
from aind_analysis_results.analysis_dispatch_model import AnalysisDispatchModel
import analysis_wrapper.utils as utils
from analysis_wrapper.example_analysis_model import (ExampleAnalysisSpecification,
                                             ExampleAnalysisSpecificationCLI)

S3_PATH_TO_BUCKET = None # REPLACE WITH DESIRED PATH
logger = logging.getLogger(__name__)


def run_analysis(analysis_dispatch_inputs: AnalysisDispatchModel, **parameters) -> None:
    processing = construct_processing_record(analysis_dispatch_inputs, **parameters)
    if docdb_record_exists(processing):
        return

    ### Execute analysis and write to results folder
    ### using the passed parameters
    ### SEE EXAMPLE BELOW
    # Use NWBZarrIO to reads
    # with NWBZarrIO(s3_url, 'r') as io:
    #     nwbfile = io.read()
    
    # acquisition_keys = list(nwbfile.acquisition.keys())
    # with open('/results/acquisition_keys.json', 'w') as f:
    #     json.dump(acquisition_keys, f)
        
    write_results_and_metadata(process, ANALYSIS_BUCKET)
    logger.info(f"Successfully wrote record to docdb and s3 to path {processing.output_path}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    input_model_paths = tuple(utils.DATA_PATH.glob('job_dict/*'))
    logger.info(f"Found {len(input_model_paths)} input job models to run analysis on.")
    analysis_specs = None

    analysis_spec_path = tuple(utils.DATA_PATH.glob("analysis_parameters.json"))
    if analysis_spec_path:
        with open(analysis_spec_path[0], "r") as f:
            analysis_specs = json.load(f)

        logger.info(
            "Found analysis specification json. Parsing list of analysis specifications"
        )
    else:
        logger.info(
            "No analysis parameters json found. Defaulting to parameters passed in via input arguments"
        )

    ### WAY TO PARSE FROM USER DEFINED APP PANEL
    # if analysis_specs is None:
    #     analysis_specs = ExampleAnalysisSpecificationCLI().model_dump_json()

    logger.info(f"Analysis Specification: {analysis_specs}")

    for model_path in input_model_paths:
        with open(model_path, "r") as f:
            analysis_dispatch_inputs = AnalysisDispatchModel.model_validate(json.load(f))
        
        analysis_specification = ExampleAnalysisSpecification.model_validate(analysis_specs).model_dump()
        logger.info(f"Running analysis with specification {analysis_specification} and input data {analysis_job_dict['asset_name']}")
        run_analysis(analysis_dispatch_inputs, **analysis_specification)
