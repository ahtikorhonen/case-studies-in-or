import json
from pathlib import Path


def read_json(file_name: str) -> dict:
    """
    Reads a json file to Python dict.
    :file_name (str): name of the json file to be read
    :return (dict): the json file as a python dict
    """
    path = Path().cwd().joinpath(f"{file_name}.json")
    try:
        with open(path, "r") as f:
            json_file = json.load(f)
            
            return json_file
        
    except Exception as e:
        raise Exception(f"Failed to read {file_name} - {str(e)}")
