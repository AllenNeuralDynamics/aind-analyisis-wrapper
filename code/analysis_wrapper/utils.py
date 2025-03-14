import doctest
import json
import pathlib

import pynwb
import s3fs
from hdmf_zarr.nwb import NWBZarrIO

S3_FILESYSTEM = s3fs.S3FileSystem()


def read_input_json() -> dict:
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
