from dataclasses import dataclass


@dataclass
class DataIngestionArtifact:
    data_zip_file_path: str
    feature_store_path: str


@dataclass
class DataValidationArtifact:
    validation_status: bool


@dataclass
class DataTransformationArtifact:
    transformed_data_dir: str
    transformed_train_dir: str
    transformed_val_dir: str
    transformed_test_dir: str
    message: str
