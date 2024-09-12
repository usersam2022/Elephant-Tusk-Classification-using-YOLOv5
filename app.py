import logging, shutil, time, subprocess
from tuskClassification.exception import DataNotFoundError
from tuskClassification.pipeline.training_pipeline import TrainPipeline
from tuskClassification.utils.main_utils import *
from tuskClassification.utils.split_data import *
from tuskClassification.constant import *
import os
import torch
import warnings

warnings.filterwarnings("ignore")

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
        print('Model training done')

    except subprocess.CalledProcessError as e:
        logging.error(f"Training failed with error code {e.returncode}")
        raise e


os.chdir(yolov5_loc)
sys.path.append(yolov5_loc)

# Suppress albumentations warnings

warnings.filterwarnings("ignore", category=UserWarning, module='albumentations')
warnings.filterwarnings("ignore", category=torch.jit.TracerWarning)

from yolov5.utils.general import check_file
from yolov5.models.yolo import Model


def load_model(weights_path, device):
    model_config_path = os.path.join(yolov5_loc, 'models', 'yolov5s.yaml')
    model = Model(cfg=model_config_path, ch=3, nc=2)

    # Load the entire model directly
    checkpoint = torch.load(weights_path, map_location=device)

    if isinstance(checkpoint, dict) and 'model' in checkpoint:
        model.load_state_dict(checkpoint['model'].state_dict())  # Ensure compatibility with YOLOv5 checkpoints
    else:
        model = checkpoint  # If the model is stored directly, assign it

    model.to(device)
    model.eval()
    return model


def test_model(weights_path, test_images_dir, img_size=960, conf_thres=0.01, iou_thres=0.35):
    logging.info("Starting model testing...")

    command = [
        "python", "detect.py",
        "--weights", weights_path,
        "--img-size", str(img_size),
        "--conf-thres", str(conf_thres),
        "--source", test_images_dir,
        "--iou_thres", str(iou_thres)
    ]

    try:
        result = subprocess.run(command, cwd=yolov5_loc, check=True, text=True)
        logging.info("Model testing completed successfully.")
        logging.info(f"Output: {result.stdout}")

    except subprocess.CalledProcessError as e:
        logging.error(f"Testing failed with error code {e.returncode}")
        logging.error(f"Standard Error: {e.stderr}")
        logging.error(f"Standard Output: {e.stdout}")
        raise e


def save_model(model, save_path):
    logging.info(f"Saving model to: {save_path}")

    # Ensure the saved_models directory exists
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    # Create a dummy input tensor with the same size as your validation images
    dummy_input = torch.randn(1, 3, 960, 960).to('cuda' if torch.cuda.is_available() else 'cpu')

    # Save the model in ONNX format
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
    print('Model saved')


def main():
    warnings.filterwarnings("ignore")

    pipeline = TrainPipeline()
    pipeline.run_pipeline()

    logging.info(f"Checking if data_transformation directories exist before moving files.")
    if not os.path.exists(aug_source_images_dir):
        logging.error(f"Image directory {aug_source_images_dir} does not exist.")
    if not os.path.exists(aug_source_labels_dir):
        logging.error(f"Label directory {aug_source_labels_dir} does not exist.")

    move_augmented_files()

    images_dir = source_images_dir
    labels_dir = source_labels_dir

    split_dataset(images_dir=images_dir, labels_dir=labels_dir)

    train_model()
    logging.info('Training using YOLOv5 done')

    # Load the trained model
    best_model_path = trained_model_path
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = load_model(best_model_path, device)  # Use the corrected load_model function

    # Test the model
    test_model(weights_path=best_model_path, test_images_dir=test_images_dir)

    # Save the model in ONNX format
    save_model(
        model=model,
        save_path=model_save_path
    )


if __name__ == "__main__":
    main()

# python train.py --img 640 --batch 16 --epochs 50 --data data/data.yaml --weights yolov5s.pt --cache --device 0 --name itr0
# C:\Users\Samya\PycharmProjects\Elephant-Tusk-Classification\yolov5\train.py:412: FutureWarning: `torch.cuda.amp.autocast(args...)` is deprecated.
# Please use `torch.amp.autocast('cuda', args...)` instead.
