import utils
import aind_analysis_results.metadata as metadata
# ADD USER ANALYSIS IMPORTS

def run_analysis(analysis_job_dict: dict) -> None:
    processing = metadata.construct_processing_record(analysis_job_dict)
    if metadata.docdb_record_exists(processing):
        return
    
    ### RUN ANALYSIS CODE HERE
    # TODO: templates for reading and writing to/from S3
    # RUN ANALYSIS

    s3_bucket = 'PUT PROJECT BUCKET NAME HERE' # REPLACE WITH YOUR BUCKET
    processing_complete = copy_results_to_s3(processing, s3_bucket)
    metadata.write_to_docdb(processing_complete)

if __name__ == "__main__":
    analysis_job_dict = utils.read_input_json()
    run_analysis(analysis_job_dict)
