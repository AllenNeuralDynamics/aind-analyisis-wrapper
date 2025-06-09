import json
import pathlib

DATA_PATH = pathlib.Path("/data")


def read_input_json(filename: str) -> dict:
    """
    Reads the input analysis model from the dispatcher

    Returns
    -------
    dict
        The input analysis model
    """
    input_json_path = tuple(DATA_PATH.glob(f"{filename}.json"))
    if not input_json_path:
        raise FileNotFoundError("No input json model found")

    with open(input_json_path[0], "r") as f:
        input_json = json.load(f)

    return input_json
