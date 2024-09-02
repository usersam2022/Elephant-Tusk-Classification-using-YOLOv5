import logging
import shutil
from tuskClassification.exception import DataNotFoundError
from tuskClassification.pipeline.training_pipeline import TrainPipeline
from tuskClassification.utils.main_utils import *
from tuskClassification.constant import *

logging.basicConfig(filename='debug.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

PACKAGE_VERSION = '0.1'

logging.info(f'This is custom log for v{PACKAGE_VERSION}')


def load_data(data_path):
    # Implement data loading logic here
    logging.info(f"Loading data from: {data_path}")
    # Example: Check if path exists
    if not os.path.exists(data_path):
        raise DataNotFoundError(f"Data path {data_path} does not exist.")
    # Add actual data loading logic
    pass


def preprocess_data(images, labels):
    # Implement data preprocessing logic here (resize, normalize, etc.)
    logging.info("Preprocessing data...")
    pass


def move_augmented_files():
    # Copy augmented images
    if os.path.exists(aug_source_images_dir):
        for filename in os.listdir(aug_source_images_dir):
            src_path = os.path.join(aug_source_images_dir, filename)
            dest_path = os.path.join(source_images_dir, filename)
            shutil.copy(src_path, dest_path)  # Changed from shutil.move to shutil.copy
        print("Augmented images copied successfully.")

    # Copy augmented labels
    if os.path.exists(aug_source_labels_dir):
        for filename in os.listdir(aug_source_labels_dir):
            src_path = os.path.join(aug_source_labels_dir, filename)
            dest_path = os.path.join(source_labels_dir, filename)
            shutil.copy(src_path, dest_path)  # Changed from shutil.move to shutil.copy
        print("Augmented labels copied successfully.")


def train_model(images, labels):
    # Implement the model training logic here
    logging.info("Training the model...")
    pass


def validate_model(model, validation_data):
    # Implement the validation logic here
    logging.info("Validating the model...")
    pass


def test_model(model, test_data):
    # Implement the testing logic here
    logging.info("Testing the model...")
    pass


def save_model(model, save_path):
    # Implement model saving logic here
    logging.info(f"Saving model to: {save_path}")
    pass


def main():
    # Run the pipeline
    pipeline = TrainPipeline()
    pipeline.run_pipeline()

    # Ensure the directories exist
    logging.info(f"Checking if data_transformation directories exist before moving files.")
    if not os.path.exists(aug_source_images_dir):
        logging.error(f"Image directory {aug_source_images_dir} does not exist.")
    if not os.path.exists(aug_source_labels_dir):
        logging.error(f"Label directory {aug_source_labels_dir} does not exist.")

    # Move the augmented images and labels
    move_augmented_files()


if __name__ == "__main__":
    main()
