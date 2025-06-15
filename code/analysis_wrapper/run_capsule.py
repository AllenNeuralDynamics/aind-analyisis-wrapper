import logging

import aind_analysis_results.files as files
import aind_analysis_results.metadata as metadata
import analysis_wrapper.utils as utils
from analysis_wrapper.analysis_model import (AnalysisSpecification,
                                             AnalysisSpecificationCLI)

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
    logger.info(f"Successfully wrote record to docdb and s3 to path {processing.output_path}")


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
    )

    analysis_job_dict = utils.read_input_json("job_dict")
    analysis_specs = None
    try:
        analysis_specs = utils.read_input_json("analysis_parameters")
        logger.info(
            "Found analysis specification json. Parsing list of analysis specifications"
        )
    except FileNotFoundError as e:
        logger.info(
            "No analysis parameters json found. Defaulting to parameters passed in via input arguments"
        )

    if analysis_specs is None:
        analysis_specs = [AnalysisSpecificationCLI().model_dump_json()]

    logger.info(f"Analysis Specification: {analysis_specs}")

    for specification in analysis_specs:
        analysis_specification = AnalysisSpecification.model_validate(specification).model_dump()
        logger.info(f"Running analysis with specification {analysis_specification} and input data {analysis_job_dict['asset_name']}")
        analysis_job_dict["parameters"] = analysis_specification
        run_analysis(analysis_job_dict)
