import yaml
import os
import sys
import base64
from tuskClassification.exception import TuskClassificationError
from tuskClassification.logger import logging


def read_yaml_file(file_path: str) -> dict:
    """
    Reads a YAML file and returns its content as a dictionary.
    """
    try:
        with open(file_path, "rb") as yaml_file:
            logging.info(f"Reading YAML file: {file_path}")
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise TuskClassificationError(e, sys) from e


def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    """
    Writes content to a YAML file. If replace is True, an existing file will be overwritten.
    """
    try:
        if replace and os.path.exists(file_path):
            os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, "w") as file:
            yaml.dump(content, file)
            logging.info(f"Writing to YAML file: {file_path}")
    except Exception as e:
        raise TuskClassificationError(e, sys)

# if images are recived in Base64 string, use code below

# def decodeimage(imgstring, filename):
#     """
#     Decodes a base64 image string and saves it to the specified file.
#     """
#     try:
#         imgdata = base64.b64decode(imgstring)
#         with open(f"./data/{filename}", 'wb') as f:
#             f.write(imgdata)
#             logging.info(f"Image decoded and saved as {filename}")
#     except Exception as e:
#         raise AppException(e, sys)
#
#
# def encodeimageintobase64(croppedimagepath):
#     """
#     Encodes an image file into a base64 string.
#     """
#     try:
#         with open(croppedimagepath, "rb") as f:
#             logging.info(f"Image encoded from {croppedimagepath}")
#             return base64.b64encode(f.read())
#     except Exception as e:
#         raise AppException(e, sys)
