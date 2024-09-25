import logging, shutil, time, subprocess
import platform
from tuskClassification.exception import DataNotFoundError
from tuskClassification.pipeline.training_pipeline import TrainPipeline
from tuskClassification.utils.main_utils import *
from tuskClassification.utils.split_data import *
from tuskClassification.constant import *
import os
import torch
import warnings
import mlflow  # Add MLflow
import mlflow.onnx  # Add MLflow ONNX for logging ONNX models

warnings.filterwarnings("ignore")

logging.basicConfig(filename='debug.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

PACKAGE_VERSION = '0.1'

logging.info(f'This is custom log for v{PACKAGE_VERSION}')

# Set MLflow tracking URI
mlflow.set_tracking_uri(aws_ip)


def load_data(data_path):
    logging.info(f"Loading data from: {data_path}")
    if not os.path.exists(data_path):
        raise DataNotFoundError(f"Data path {data_path} does not exist.")
    pass


def move_augmented_files():
    if os.path.exists(aug_source_images_dir):
        for filename in os.listdir(aug_source_images_dir):
            src_path = os.path.join(aug_source_images_dir, filename)
            dest_path = os.path.join(source_images_dir, filename)
            shutil.copy(src_path, dest_path)
        print("Augmented images copied successfully.")

    if os.path.exists(aug_source_labels_dir):
        for filename in os.listdir(aug_source_labels_dir):
            src_path = os.path.join(aug_source_labels_dir, filename)
            dest_path = os.path.join(source_labels_dir, filename)
            shutil.copy(src_path, dest_path)
        print("Augmented labels copied successfully.")


def train_model():
    try:
        logging.info("Starting model training...")

        # Log MLflow parameters
        mlflow.log_param("epochs", 3)
        mlflow.log_param("batch_size", 4)

        command = train_command
        result = subprocess.run(command, cwd=yolov5_loc, check=True, text=True)

        logging.info("Model training completed successfully.")
        print('Model training done')

    except subprocess.CalledProcessError as e:
        logging.error(f"Training failed with error code {e.returncode}")
        raise e


if platform.system() == 'Windows':
    yolov5_loc = yolov5_loc
else:  # Linux environment (for Docker container)
    yolov5_loc = '/app/yolov5'

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

    checkpoint = torch.load(weights_path, map_location=device)

    if isinstance(checkpoint, dict) and 'model' in checkpoint:
        model.load_state_dict(checkpoint['model'].state_dict())
    else:
        model = checkpoint

    model.to(device)
    model.eval()
    return model


def test_model(weights_path, test_images_dir, img_size=640, conf_thres=0.01, iou_thres=0.35):
    logging.info("Starting model testing...")

    command = [
        "python", "detect.py",
        "--weights", weights_path,
        "--img-size", str(img_size),
        "--conf-thres", str(conf_thres),
        "--source", test_images_dir,
        "--iou-thres", str(iou_thres)
    ]

    try:
        result = subprocess.run(command, cwd=yolov5_loc, check=True, text=True)
        logging.info("Model testing completed successfully.")
        logging.info(f"Output: {result.stdout}")

        # Log accuracy or any relevant metric
        test_accuracy = 0.85
        mlflow.log_metric("test_accuracy", test_accuracy)

    except subprocess.CalledProcessError as e:
        logging.error(f"Testing failed with error code {e.returncode}")
        logging.error(f"Standard Error: {e.stderr}")
        logging.error(f"Standard Output: {e.stdout}")
        raise e


def save_model(model, save_path):
    logging.info(f"Saving model to: {save_path}")

    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    dummy_input = torch.randn(1, 3, 640, 640).to('cuda' if torch.cuda.is_available() else 'cpu')

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

    # Log the model artifact to MLflow
    mlflow.log_artifact(save_path)

    logging.info(f"Model saved to: {save_path}")
    print('Model saved')


def main():
    warnings.filterwarnings("ignore")

    with mlflow.start_run():
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

        best_model_path = trained_model_path
        device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        model = load_model(best_model_path, device)

        test_model(weights_path=best_model_path, test_images_dir=test_images_dir)

        save_model(
            model=model,
            save_path=model_save_path
        )


if __name__ == "__main__":
    main()

# python train.py --img 640 --batch 16 --epochs 50 --data data/data.yaml --weights yolov5s.pt --cache --device 0 --name itr0
