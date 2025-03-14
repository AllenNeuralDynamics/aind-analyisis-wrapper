import utils
from pynwb import NWBFile


def run_analysis(nwb: NWBFile) -> None:
    # THIS IS WHERE ANALYSIS SPECIFIC CODE CAN GO?
    # IMPORT RELEVANT PACKAGES AND USE NWB TO DO WHAT YOU WANT
    pass


if __name__ == "__main__":
    input_json = utils.read_input_json()  # possibly change to pydantic model reading
    nwb = utils.read_nwb_from_s3(input_json["s3_location"])
    run_analysis(nwb)
