import logging, shutil, time, subprocess
import torch
from tuskClassification.exception import DataNotFoundError
from tuskClassification.pipeline.training_pipeline import TrainPipeline
from tuskClassification.utils.main_utils import *
from tuskClassification.utils.split_data import *
from tuskClassification.constant import *
from sklearn.metrics import f1_score, precision_score, recall_score
from torchvision.ops import box_iou
import numpy as np
from torch.utils.data import DataLoader
from torchvision.datasets import ImageFolder
from torchvision import transforms

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


def train_model():
    try:
        logging.info("Starting model training...")

        # Define the command to run YOLOv5 training
        command = [
            "python", "train.py",
            "--img", "960",
            "--batch", "4",
            "--epochs", "20",
            "--data", "data/data.yaml",
            "--weights", "yolov5s.pt",
            "--cache",
            "--device", "0",
            "--name", "itr0"
        ]

        # Run the command
        result = subprocess.run(command, cwd="C:/Users/Samya/PycharmProjects/Elephant-Tusk-Classification/yolov5",
                                check=True, text=True)

        logging.info("Model training completed successfully.")

    except subprocess.CalledProcessError as e:
        logging.error(f"Training failed with error code {e.returncode}")
        raise e


def validate_model(model, validation_loader, iou_threshold=0.5):
    logging.info("Validating the model...")

    all_labels = []
    all_preds = []
    all_iou_scores = []
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    model.eval()  # Set the model to evaluation mode
    model.to(device)  # Move model to device

    with torch.no_grad():
        for images, labels in validation_loader:
            images = images.to(device)  # Move images to device
            labels = [{k: v.to(device) for k, v in t.items()} for t in labels]  # Move labels to device

            # Get predictions
            outputs = model(images)

            # Process the predictions and ground truth
            for i, output in enumerate(outputs):
                pred_boxes = output['boxes'].cpu().numpy()  # Move back to CPU for processing
                pred_scores = output['scores'].cpu().numpy()
                true_boxes = labels[i]['boxes'].cpu().numpy()
                true_labels = labels[i]['labels'].cpu().numpy()

                # Filter predictions with IoU and confidence threshold
                pred_boxes = pred_boxes[pred_scores > iou_threshold]

                # Calculate IoU
                iou = box_iou(torch.tensor(pred_boxes), torch.tensor(true_boxes)).numpy()
                all_iou_scores.append(np.mean(iou))

                # Store predictions and ground truths
                all_preds.extend([1 if p > iou_threshold else 0 for p in pred_scores])
                all_labels.extend(true_labels)

    # Calculate F1 Score
    f1 = f1_score(all_labels, all_preds, average='weighted')
    precision = precision_score(all_labels, all_preds, average='weighted')
    recall = recall_score(all_labels, all_preds, average='weighted')
    mean_iou = np.mean(all_iou_scores)

    logging.info(f'F1 Score: {f1:.4f}')
    logging.info(f'Precision: {precision:.4f}')
    logging.info(f'Recall: {recall:.4f}')
    logging.info(f'Mean IoU: {mean_iou:.4f}')

    return mean_iou


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

    images_dir = source_images_dir
    labels_dir = source_labels_dir

    split_dataset(images_dir=images_dir, labels_dir=labels_dir)

    train_model()
    logging.info('Upto training using YOLOv5 done')

    # Load the trained model
    model = torch.load(
        'C:/Users/Samya/PycharmProjects/Elephant-Tusk-Classification/yolov5/runs/train/itr0/weights/best.pt')

    # Set up validation loader
    validation_transform = transforms.Compose([
        transforms.Resize((960, 960)),
        transforms.ToTensor(),
    ])

    validation_dataset = ImageFolder(root=val_images_dir, transform=validation_transform)
    validation_loader = DataLoader(validation_dataset, batch_size=4, shuffle=False)

    # Validate the model
    f1, mean_iou = validate_model(model, validation_loader)

    logging.info('Validation completed')
    logging.info(f'F1 Score: {f1:.4f}, Mean IoU: {mean_iou:.4f}')


if __name__ == "__main__":
    main()

# python train.py --img 640 --batch 16 --epochs 50 --data data/data.yaml --weights yolov5s.pt --cache --device 0 --name itr0
