import doctest
import json
import pathlib

import pynwb
import s3fs
from hdmf_zarr.nwb import NWBZarrIO

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


def read_nwb_from_s3(s3_location: str) -> pynwb.NWBFile:
    """
    >>> nwb = read_nwb_from_s3('s3://codeocean-s3datasetsbucket-1u41qdg42ur9/7f1eaf10-01bc-41cb-bc88-6464d0425b51/nwb/behavior_769038_2025-02-10_13-16-09.nwb')
    >>> type(nwb)
    <class 'pynwb.file.NWBFile'>
    """
    if not S3_FILESYSTEM.exists(s3_location):
        raise FileNotFoundError(f"{s3_location} does not exist")

    # TODO: Replace with nwb utils module when ready
    if S3_FILESYSTEM.isdir(s3_location):
        with NWBZarrIO(s3_location, mode="r") as io:
            nwb = io.read()
    else:  # have to download and then read
        with S3_FILESYSTEM.open(s3_location, "rb") as s3_file:
            with pynwb.NWBHDF5IO(s3_file, mode="r") as io:
                nwb = io.read()

    return nwb


if __name__ == "__main__":
    doctest.testmod()
