import logging

import aind_analysis_results.files as files
import aind_analysis_results.metadata as metadata
import analysis_wrapper.utils as utils
from analysis_wrapper.analysis_model import AnalysisSpecification, AnalysisSpecificationCLI

logger = logging.getLogger(__name__)


def run_analysis(analysis_job_dict: dict) -> None:
    processing = metadata.construct_processing_record(analysis_job_dict)
    if metadata.docdb_record_exists(processing):
        return

    ### Execute analysis and write to results folder
    processing_updated = files.copy_results_to_s3(
        processing, analysis_job_dict["parameters"]["s3_output_bucket"]
    )
    metadata.write_to_docdb(processing_updated)

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    analysis_job_dict = utils.read_input_json("job_dict")
    analysis_parameters = None
    try:
        analysis_parameters = utils.read_input_json("analysis_parameters")
        logging.info("Found analysis specification json. Using that")
    except FileNotFoundError as e:
        logger.info(
            "No analysis parameters json found. Defaulting to parameters passed in via input arguments"
        )

    if analysis_parameters is not None:
        analysis_specification = AnalysisSpecification.model_validate(analysis_parameters).model_dump_json()
    else:
        analysis_specification = AnalysisSpecificationCLI().model_dump_json()

    logging.info(f"Analysis Specification: {analysis_specification}")

    analysis_job_dict["parameters"] = analysis_specification

    run_analysis(analysis_job_dict)
