import os
import shutil
import random
from sklearn.model_selection import train_test_split
from tuskClassification.constant import *


def split_dataset(images_dir, labels_dir, train_ratio=0.8, val_ratio=0.1, test_ratio=0.1, random_state=42):
    # Define paths for train, val, and test splits
    train_images_dir = os.path.join(images_dir, "..", "train")
    val_images_dir = os.path.join(images_dir, "..", "val")
    test_images_dir = os.path.join(images_dir, "..", "test")

    train_labels_dir = os.path.join(labels_dir, "..", "train")
    val_labels_dir = os.path.join(labels_dir, "..", "val")
    test_labels_dir = os.path.join(labels_dir, "..", "test")

    # List all images and labels
    images = sorted(os.listdir(images_dir))
    labels = sorted(os.listdir(labels_dir))

    # Ensure only image and label files are considered (avoid directory names)
    images = [f for f in images if os.path.isfile(os.path.join(images_dir, f))]
    labels = [f for f in labels if os.path.isfile(os.path.join(labels_dir, f))]

    # Split data into train, val, test
    train_images, temp_images, train_labels, temp_labels = train_test_split(
        images, labels, test_size=(val_ratio + test_ratio), random_state=random_state
    )
    val_images, test_images, val_labels, test_labels = train_test_split(
        temp_images, temp_labels, test_size=(test_ratio / (val_ratio + test_ratio)), random_state=random_state
    )

    # Function to move files
    def move_files(file_list, source_dir, destination_dir):
        for file_name in file_list:
            shutil.move(os.path.join(source_dir, file_name), os.path.join(destination_dir, file_name))

    # Move files to their respective directories
    move_files(train_images, images_dir, train_images_dir)
    move_files(val_images, images_dir, val_images_dir)
    move_files(test_images, images_dir, test_images_dir)

    move_files(train_labels, labels_dir, train_labels_dir)
    move_files(val_labels, labels_dir, val_labels_dir)
    move_files(test_labels, labels_dir, test_labels_dir)

    # Logging the result
    print(f"Training images: {len(os.listdir(train_images_dir))}")
    print(f"Validation images: {len(os.listdir(val_images_dir))}")
    print(f"Test images: {len(os.listdir(test_images_dir))}")