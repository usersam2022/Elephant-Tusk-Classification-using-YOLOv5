import os
import sys
from tuskClassification.logger import logging
from tuskClassification.exception import TuskClassificationError
from tuskClassification.entity.config_entity import DataIngestionConfig, DataValidationConfig
from tuskClassification.entity.artifacts_entity import DataValidationArtifact, DataIngestionArtifact


class DataValidation:
    def __init__(
            self,
            data_ingestion_artifact: DataIngestionArtifact,
            data_validation_config: DataValidationConfig,
    ):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
        except Exception as e:
            raise TuskClassificationError(e, sys)

    def validate_all_files_exist(self) -> bool:
        try:
            validation_status = None

            all_files = os.listdir(self.data_ingestion_artifact.feature_store_path)

            # Check for required files excluding data.yaml
            missing_files = [file for file in self.data_validation_config.required_file_list if file not in all_files]

            if missing_files:
                validation_status = False
                os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
                with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
                    f.write(f"Validation status: {validation_status}\n")
                    f.write(f"Missing files: {', '.join(missing_files)}")
            else:
                validation_status = True
                os.makedirs(self.data_validation_config.data_validation_dir, exist_ok=True)
                with open(self.data_validation_config.valid_status_file_dir, 'w') as f:
                    f.write(f"Validation status: {validation_status}")

            return validation_status

        except Exception as e:
            raise TuskClassificationError(e, sys)

    def validate_file_formats(self) -> bool:
        try:
            images_dir = os.path.join(self.data_ingestion_artifact.feature_store_path, 'images')
            labels_dir = os.path.join(self.data_ingestion_artifact.feature_store_path, 'labels')
            valid_image_format = ".jpg"
            valid_label_format = ".txt"

            image_files = [f for f in os.listdir(images_dir) if f.endswith(valid_image_format)]
            label_files = [f for f in os.listdir(labels_dir) if f.endswith(valid_label_format)]

            for img_file in image_files:
                corresponding_label_file = img_file.replace(valid_image_format, valid_label_format)
                if corresponding_label_file not in label_files:
                    return False

            return True

        except Exception as e:
            raise TuskClassificationError(e, sys)

    def validate_directory_structure(self) -> bool:
        try:
            expected_dirs = ['train', 'val', 'test']
            base_dirs = ['images', 'labels']

            for base_dir in base_dirs:
                base_path = os.path.join(self.data_ingestion_artifact.feature_store_path, base_dir)
                for expected_dir in expected_dirs:
                    if not os.path.exists(os.path.join(base_path, expected_dir)):
                        return False

            return True

        except Exception as e:
            raise TuskClassificationError(e, sys)

    def initiate_data_validation(self) -> DataValidationArtifact:
        logging.info("Entered initiate_data_validation method of DataValidation class")
        try:
            validation_status = self.validate_all_files_exist() and \
                                self.validate_file_formats() and \
                                self.validate_directory_structure()

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status)

            logging.info("Exited initiate_data_validation method of DataValidation class")
            logging.info(f"Data validation artifact: {data_validation_artifact}")

            return data_validation_artifact

        except Exception as e:
            raise TuskClassificationError(e, sys)
