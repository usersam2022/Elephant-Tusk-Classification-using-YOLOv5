import sys
from tuskClassification.logger import logging  # Ensure logger is imported


def error_message_detail(error, error_detail: sys = None):
    if error_detail:
        _, _, exc_tb = error_detail.exc_info()
        file_name = exc_tb.tb_frame.f_code.co_filename
        error_message = "Error occurred in script: [{0}] at line number: [{1}] with message: [{2}]".format(
            file_name, exc_tb.tb_lineno, str(error)
        )
        return error_message
    return str(error)


class TuskClassificationError(Exception):
    """Base class for other exceptions"""

    def __init__(self, message, error_detail: sys = None):
        super().__init__(message)
        if error_detail:
            detailed_message = error_message_detail(message, error_detail)
            logging.error(detailed_message)
            self.error_message = detailed_message
        else:
            logging.error(message)
            self.error_message = message

    def __str__(self):
        return self.error_message


class DataNotFoundError(TuskClassificationError):
    """Raised when the required data is not found"""
    pass


class InvalidImageFormatError(TuskClassificationError):
    """Raised when an image is in an unsupported format"""
    pass


class ModelLoadingError(TuskClassificationError):
    """Raised when there is an error loading the model"""
    pass
