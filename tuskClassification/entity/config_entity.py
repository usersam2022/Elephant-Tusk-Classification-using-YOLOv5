import os
from dataclasses import dataclass, field
from datetime import datetime
from tuskClassification.constant.training_pipeline import *
from tuskClassification.constant import *


@dataclass
class TrainingPipelineConfig:
    artifacts_dir: str = ARTIFACTS_DIR


training_pipeline_config: TrainingPipelineConfig = TrainingPipelineConfig()


@dataclass
class DataIngestionConfig:
    data_ingestion_dir: str = os.path.join(
        training_pipeline_config.artifacts_dir, DATA_INGESTION_DIR_NAME
    )

    feature_store_file_path: str = os.path.join(
        data_ingestion_dir, DATA_INGESTION_FEATURE_STORE_DIR
    )

    data_download_url: str = DATA_DOWNLOAD_URL


@dataclass
class DataValidationConfig:
    # Directory where validation status and required files are checked
    data_validation_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_DIR_NAME)

    # Path for the validation status file
    valid_status_file_dir: str = os.path.join(data_validation_dir, DATA_VALIDATION_STATUS_FILE)

    # List of required files for validation
    required_file_list = DATA_VALIDATION_ALL_REQUIRED_FILES


@dataclass
class DataTransformationConfig:
    def __init__(self):
        self.transformed_data_dir = transformed_data_dir
        self.source_images_dir = source_images_dir
        self.source_labels_dir = source_labels_dir
        self.transformed_images_dir = os.path.join(transformed_data_dir, "data_transformation", "images")
        self.transformed_labels_dir = os.path.join(transformed_data_dir, "data_transformation", "labels")
        self.image_size = image_size
