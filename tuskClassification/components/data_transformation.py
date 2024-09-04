import cv2
import shutil
import numpy as np
from tuskClassification.entity.artifacts_entity import DataTransformationArtifact
from tuskClassification.entity.config_entity import DataTransformationConfig
from tuskClassification.logger import *
import albumentations as alb


class DataTransformation:
    def __init__(self, config: DataTransformationConfig):
        self.config = config
        # Initialize the augmentation pipeline
        self.transforms = alb.Compose([
            alb.Resize(*self.config.image_size),
            alb.HorizontalFlip(p=0.5),
            alb.RandomRotate90(p=0.5),
            alb.RandomBrightnessContrast(p=0.2),
        ])

        # Ensure the directories exist
        os.makedirs(self.config.transformed_images_dir, exist_ok=True)
        os.makedirs(self.config.transformed_labels_dir, exist_ok=True)

    def transform(self, image):
        # Apply the augmentations
        augmented = self.transforms(image=image)
        transformed_image = augmented['image']
        return transformed_image

    def apply_transformations(self, image_path, label_path, num_augmented_images=9):
        image = cv2.imread(image_path)
        if image is None:
            raise ValueError(f"Failed to read image {image_path}")

        basename = os.path.basename(image_path).split('.')[0]

        for i in range(num_augmented_images):
            try:
                transformed_image = self.transform(image)
                if transformed_image is None:
                    raise ValueError(f"Transformed image is None for {image_path}")

                transformed_image_path = os.path.join(
                    self.config.transformed_images_dir, f"{basename}_aug_{i}.jpg")
                success = cv2.imwrite(transformed_image_path, transformed_image)
                if not success:
                    raise Exception(f"Failed to save image {transformed_image_path}")

                transformed_label_path = os.path.join(
                    self.config.transformed_labels_dir, f"{basename}_aug_{i}.txt")
                shutil.copy(label_path, transformed_label_path)
            except Exception as e:
                logging.error(f"Error during augmentation or saving for {image_path}: {e}")
                raise

    def initiate_data_transformation(self):
        image_paths = [os.path.join(self.config.source_images_dir, fname) for fname in
                       os.listdir(self.config.source_images_dir)]
        label_paths = [os.path.join(self.config.source_labels_dir, fname) for fname in
                       os.listdir(self.config.source_labels_dir)]

        for image_path, label_path in zip(image_paths, label_paths):
            self.apply_transformations(image_path, label_path)

        logging.info(f"Transformation complete. Data saved in {self.config.transformed_data_dir}")

        return DataTransformationArtifact(
            transformed_train_dir=self.config.transformed_images_dir,
            transformed_val_dir=self.config.transformed_labels_dir,
            transformed_test_dir=self.config.transformed_labels_dir,
            transformed_data_dir=self.config.transformed_data_dir,
            message="Data transformation completed successfully"
        )
