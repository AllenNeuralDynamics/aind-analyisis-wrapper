import utils
from pynwb import NWBFile


def get_input_parser() -> argparse.ArgumentParser:
    """
    Creates and returns an argument parser for input arguments.

    Parameters
    ----------
    None

    Returns
    -------
    argparse.ArgumentParser
        A configured ArgumentParser object with predefined command-line arguments for:
        - `--analysis_name`: A string argument for the analysis to be run
        - `--file_extension`: A string argument for optionally specifying whether or not to look for the given file extension

    """

    parser = argparse.ArgumentParser()
    parser.add_argument("--analysis_name", type=str, default="")
    parser.add_argument("--analysis_version", type=str, default="")
    parser.add_argument("--analysis_libraries", type=str, default="")
    parser.add_argument("--analysis_parameters", type=str, default="")

    return parser


def run_analysis(nwb: NWBFile) -> None:
    # THIS IS WHERE ANALYSIS SPECIFIC CODE CAN GO?
    # IMPORT RELEVANT PACKAGES AND USE NWB TO DO WHAT YOU WANT
    pass


if __name__ == "__main__":
    input_json = utils.read_input_json()  # possibly change to pydantic model reading
    nwb = utils.read_nwb_from_s3(input_json["s3_location"])
    run_analysis(nwb)
