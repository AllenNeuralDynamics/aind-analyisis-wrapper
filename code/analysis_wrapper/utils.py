import json
import pathlib

DATA_PATH = pathlib.Path("/data")
S3_FILESYSTEM = s3fs.S3FileSystem()


def read_input_json() -> dict:
    """
    Reads an NWB file from an S3 location.

    This function checks if the S3 location is a directory or a file. If it is a directory,
    the function uses the `NWBZarrIO` class to read the NWB file. If it is a file,
    the function reads the NWB file using `pynwb.NWBHDF5IO`.

    Parameters
    ----------
    s3_location : str
        The S3 URI pointing to the location of the NWB file, either a directory or a file.

    Returns
    -------
    pynwb.NWBFile
        The NWB file read from the specified S3 location.

    Raises
    ------
    FileNotFoundError
        If the specified S3 location does not exist.
    """
    input_json_path = tuple(DATA_PATH.glob("*.json"))
    if not input_json_path:
        raise FileNotFoundError("No input json model found")

    with open(input_json_path[0], "r") as f:
        input_json = json.load(f)

    return input_json
