import sys
from tuskClassification.components.data_ingestion import DataIngestion
from tuskClassification.components.data_transformation import DataTransformation
from tuskClassification.components.data_validation import DataValidation
from tuskClassification.entity.artifacts_entity import (DataIngestionArtifact, DataValidationArtifact,
                                                        DataTransformationArtifact)
from tuskClassification.entity.config_entity import (DataIngestionConfig, DataValidationConfig,
                                                     DataTransformationConfig)
from tuskClassification.exception import TuskClassificationError
from tuskClassification.logger import logging


class TrainPipeline:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_ingestion_config = DataIngestionConfig()

    def start_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logging.info(
                "Entered the start_data_ingestion method of TrainPipeline class"
            )
            logging.info("Getting the data from URL")

            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config
            )

            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Got the data from URL")
            logging.info(
                "Exited the start_data_ingestion method of TrainPipeline class"
            )

            return data_ingestion_artifact

        except Exception as e:
            raise TuskClassificationError(e, sys)

    def start_data_validation(
            self, data_ingestion_artifact: DataIngestionArtifact
    ) -> DataValidationArtifact:
        logging.info("Entered the start_data_validation method of TrainPipeline class")

        try:
            data_validation = DataValidation(
                data_ingestion_artifact=data_ingestion_artifact,
                data_validation_config=self.data_validation_config,
            )

            data_validation_artifact = data_validation.initiate_data_validation()

            logging.info("Performed the data validation operation")
            logging.info("Exited the start_data_validation method of TrainPipeline class")
            return data_validation_artifact

        except Exception as e:
            raise TuskClassificationError(e, sys) from e

    def start_data_transformation(
            self, data_validation_artifact: DataValidationArtifact
    ) -> DataTransformationArtifact:
        logging.info("Entered the start_data_transformation method of TrainPipeline class")

        try:
            data_transformation = DataTransformation(
                config=self.data_transformation_config
            )

            data_transformation_artifact = data_transformation.initiate_data_transformation()

            logging.info("Performed the data transformation operation")
            logging.info("Exited the start_data_transformation method of TrainPipeline class")
            return data_transformation_artifact

        except Exception as e:
            raise TuskClassificationError(e, sys) from e

    def run_pipeline(self) -> None:
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact)
            self.start_data_transformation(data_validation_artifact)

            # Optionally, you can log or print the results of each step
            print("Data Ingestion, Validation, and Transformation completed successfully!")

        except Exception as e:
            raise TuskClassificationError(e, sys)
