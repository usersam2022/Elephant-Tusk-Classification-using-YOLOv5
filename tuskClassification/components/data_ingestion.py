import os, requests
import sys
import rarfile
import gdown
import platform
from tuskClassification.constant import *
from tuskClassification.logger import logging
from tuskClassification.exception import TuskClassificationError
from tuskClassification.entity.config_entity import DataIngestionConfig
from tuskClassification.entity.artifacts_entity import DataIngestionArtifact
import shutil

# if platform.system() == 'Windows':
#     rar_loc = rar_loc
# else:  # Linux environment
#     rar_loc = None


def extract_rar_file(rar_file_path: str) -> str:

    try:
        # Set the path directly to the root project directory
        root_project_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        # Define the path for the 'data' folder directly under the root project directory
        feature_store_path = os.path.join(root_project_dir, 'data')

        with rarfile.RarFile(rar_file_path) as rar_ref:
            # Extract the contents of the .rar file to the root project directory
            rar_ref.extractall(root_project_dir)

            # Check if the extracted 'data' folder exists
            extracted_data_folder = os.path.join(root_project_dir, 'data')
            if os.path.exists(extracted_data_folder) and os.path.isdir(extracted_data_folder):
                # Move contents up one level if a 'data' folder is found
                for item in os.listdir(extracted_data_folder):
                    source = os.path.join(extracted_data_folder, item)
                    destination = os.path.join(feature_store_path, item)
                    shutil.move(source, destination)

                # Now remove the empty 'data' folder, only if it is empty
                try:
                    os.rmdir(extracted_data_folder)
                except OSError:
                    logging.warning(f"Cannot remove non-empty directory: {extracted_data_folder}")

        logging.info(f"Extracted rar file: {rar_file_path} into dir: {feature_store_path}")

        return feature_store_path

    except Exception as e:
        raise TuskClassificationError(e, sys)


class DataIngestion:
    def __init__(self, data_ingestion_config: DataIngestionConfig = DataIngestionConfig()):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise TuskClassificationError(e, sys)

    def download_data(self) -> str:
        try:
            dataset_url = self.data_ingestion_config.data_download_url
            data_download_dir = self.data_ingestion_config.data_ingestion_dir
            os.makedirs(data_download_dir, exist_ok=True)
            data_file_name = "data.rar"
            rar_file_path = os.path.join(data_download_dir, data_file_name)
            logging.info(f"Downloading data from {dataset_url} into file {rar_file_path}")

            if "drive.google.com" in dataset_url:
                # Handle Google Drive URL
                file_id = dataset_url.split("/")[-2]
                gdown.download(f'https://drive.google.com/uc?export=download&id={file_id}', rar_file_path, quiet=False)

            else:
                # Handle non-Google Drive URLs (e.g., S3)
                response = requests.get(dataset_url, stream=True)
                if response.status_code == 200:
                    with open(rar_file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                    logging.info(f"Downloaded data from {dataset_url} into file {rar_file_path}")
                else:
                    raise Exception(f"Failed to download file. Status code: {response.status_code}")

            return rar_file_path

        except Exception as e:
            raise TuskClassificationError(e, sys)

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered initiate_data_ingestion method of Data_Ingestion class")
        try:
            rar_file_path = self.download_data()
            feature_store_path = extract_rar_file(rar_file_path)

            data_ingestion_artifact = DataIngestionArtifact(
                data_zip_file_path=rar_file_path,
                feature_store_path=feature_store_path
            )

            logging.info("Exited initiate_data_ingestion method of Data_Ingestion class")
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise TuskClassificationError(e, sys)
