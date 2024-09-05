import logging, shutil, time, subprocess
from tuskClassification.exception import DataNotFoundError
from tuskClassification.pipeline.training_pipeline import TrainPipeline
from tuskClassification.utils.main_utils import *
from tuskClassification.utils.split_data import *
from tuskClassification.constant import *
import os
import torch
from yolov5.utils.general import check_file
from yolov5.models.yolo import Model

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
        command = train_command

        # Run the command
        result = subprocess.run(command, cwd=yolov5_loc, check=True, text=True)

        logging.info("Model training completed successfully.")

    except subprocess.CalledProcessError as e:
        logging.error(f"Training failed with error code {e.returncode}")
        raise e


yolov5_repo_path = 'C:/Users/Samya/PycharmProjects/Elephant-Tusk-Classification/yolov5'
os.chdir(yolov5_repo_path)


def test_model(weights_path, test_images_dir, img_size=960, conf_thres=0.25):
    logging.info("Starting model testing...")

    command = [
        "python", "detect.py",
        "--weights", weights_path,
        "--img-size", str(img_size),
        "--conf-thres", str(conf_thres),
        "--source", test_images_dir
    ]

    try:
        result = subprocess.run(command, cwd=yolov5_repo_path, check=True, text=True)
        logging.info("Model testing completed successfully.")
        logging.info(f"Output: {result.stdout}")

    except subprocess.CalledProcessError as e:
        logging.error(f"Testing failed with error code {e.returncode}")
        logging.error(f"Standard Error: {e.stderr}")
        logging.error(f"Standard Output: {e.stdout}")
        raise e


def save_model(model, save_path):
    logging.info(f"Saving model to: {save_path}")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    dummy_input = torch.randn(1, 3, 960, 960).to('cuda' if torch.cuda.is_available() else 'cpu')

    torch.onnx.export(
        model,
        dummy_input,
        save_path,
        export_params=True,
        opset_version=11,
        do_constant_folding=True,
        input_names=['input'],
        output_names=['output'],
        dynamic_axes={'input': {0: 'batch_size'}, 'output': {0: 'batch_size'}}
    )

    logging.info(f"Model saved to: {save_path}")


def main():
    logging.basicConfig(filename='debug.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    PACKAGE_VERSION = '0.1'
    logging.info(f'This is custom log for v{PACKAGE_VERSION}')

    model_path = r'C:\Users\Samya\PycharmProjects\Elephant-Tusk-Classification\yolov5\runs\train\itr2_b8_e50\weights\best.pt'
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    model = torch.load(model_path, map_location=device)['model'].float()
    model.to(device)
    model.eval()

    test_images_dir = r'C:\Users\Samya\PycharmProjects\Elephant-Tusk-Classification\data\images\test'

    test_model(weights_path=model_path, test_images_dir=test_images_dir)

    save_model(
        model=model,
        save_path='C:/Users/Samya/PycharmProjects/Elephant-Tusk-Classification/yolov5/saved_models/model0.onnx'
    )


if __name__ == "__main__":
    main()

"""
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
    logging.info('Training using YOLOv5 done')

    time.sleep(10)

    # Set the path to the models directory and ensure it is added to sys.path
    path_to_models_directory = yolov5_loc
    if path_to_models_directory not in sys.path:
        sys.path.append(path_to_models_directory)

    # Load the trained model on the GPU if available
    model_path = best_model_path
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = torch.load(model_path, map_location=device)

    # Set up the validation data loader
    validation_transform = transforms.Compose([
        transforms.Resize((960, 960)),
        transforms.ToTensor(),
    ])

    validation_dataset = CustomDataset(image_dir=val_images_dir, transform=validation_transform)
    validation_loader = DataLoader(validation_dataset, batch_size=4, shuffle=False)

    # Validate the model
    f1, mean_iou = validate_model(model, validation_loader)

    logging.info('Validation done')
    logging.info(f'F1 Score: {f1:.4f}, Mean IoU: {mean_iou:.4f}')

    test_model(weights_path=best_model_path, test_images_dir=test_images_dir)

    # Save the model in ONNX format
    save_model(
        model=model,
        save_path='C:/Users/Samya/PycharmProjects/Elephant-Tusk-Classification/yolov5/saved_models/model0.onnx'
    )


if __name__ == "__main__":
    main()
"""

# python train.py --img 640 --batch 16 --epochs 50 --data data/data.yaml --weights yolov5s.pt --cache --device 0 --name itr0
