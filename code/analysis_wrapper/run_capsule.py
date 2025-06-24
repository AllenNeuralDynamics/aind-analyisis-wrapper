import json
import logging

import aind_analysis_results.files as files
import aind_analysis_results.metadata as metadata
import analysis_wrapper.utils as utils
from analysis_wrapper.analysis_model import (AnalysisSpecification,
                                             AnalysisSpecificationCLI)

S3_PATH_TO_BUCKET = None # REPLACE WITH DESIRED PATH
logger = logging.getLogger(__name__)


def run_analysis(analysis_job_dict: dict) -> None:
    processing = metadata.construct_processing_record(analysis_job_dict)
    if metadata.docdb_record_exists(processing):
        return

    ### Execute analysis and write to results folder
    ### SEE EXAMPLE BELOW
    # Use NWBZarrIO to read
    # with NWBZarrIO(s3_url, 'r') as io:
    #     nwbfile = io.read()
    
    # acquisition_keys = list(nwbfile.acquisition.keys())
    # with open('/results/acquisition_keys.json', 'w') as f:
    #     json.dump(acquisition_keys, f)
        
    processing_updated = files.copy_results_to_s3(
        processing, 
    )
    metadata.write_to_docdb(processing_updated)
    logger.info(f"Successfully wrote record to docdb and s3 to path {processing.output_path}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    input_model_paths = tuple(utils.DATA_PATH.glob('job_dict/*'))
    logger.info(f"Found f{len(input_model_paths)} input job models to run analysis on.")
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
    #     analysis_specs = [AnalysisSpecificationCLI().model_dump_json()]

    logger.info(f"Analysis Specification: {analysis_specs}")

    for model_path in input_model_paths:
        with open(model_path, "r") as f:
            analysis_job_dict = json.load(f)
        
        for specification in analysis_specs:
            analysis_specification = AnalysisSpecification.model_validate(specification).model_dump()
            logger.info(f"Running analysis with specification {analysis_specification} and input data {analysis_job_dict['asset_name']}")
            analysis_job_dict["parameters"] = analysis_specification
            run_analysis(analysis_job_dict)
