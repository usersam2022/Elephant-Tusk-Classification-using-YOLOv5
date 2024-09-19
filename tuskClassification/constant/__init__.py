source_images_dir = 'C:\\Users\\Samya\\PycharmProjects\\Elephant-Tusk-Classification\\data\\images\\train'
source_labels_dir = 'C:\\Users\\Samya\\PycharmProjects\\Elephant-Tusk-Classification\\data\\labels\\train'
transformed_data_dir = 'C:\\Users\\Samya\\PycharmProjects\\Elephant-Tusk-Classification\\artifacts'

image_size = (640, 640)

aug_params = ['flip', 'rotate', 'brightness_contrast']

data_validation_dir = 'C:\\Users\\Samya\\PycharmProjects\\Elephant-Tusk-Classification\\artifacts'

rar_loc = r'C:\Program Files\WinRAR\UnRAR.exe'

drive_prefix = 'https://drive.google.com/uc?/export=download&id='

aug_source_images_dir = 'C:\\Users\\Samya\\PycharmProjects\\Elephant-Tusk-Classification\\artifacts\\data_transformation\\images'
aug_source_labels_dir = 'C:\\Users\\Samya\\PycharmProjects\\Elephant-Tusk-Classification\\artifacts\\data_transformation\\labels'

images_dir = r'C:\Users\Samya\PycharmProjects\Elephant-Tusk-Classification\data\images\train'
labels_dir = r'C:\Users\Samya\PycharmProjects\Elephant-Tusk-Classification\data\labels\train'

train_images_dir = r'C:\Users\Samya\PycharmProjects\Elephant-Tusk-Classification\data\images\train'
val_images_dir = r'C:\Users\Samya\PycharmProjects\Elephant-Tusk-Classification\data\images\val'
test_images_dir = r'C:\Users\Samya\PycharmProjects\Elephant-Tusk-Classification\data\images\test'

train_labels_dir = r'C:\Users\Samya\PycharmProjects\Elephant-Tusk-Classification\data\labels\train'
val_labels_dir = r'C:\Users\Samya\PycharmProjects\Elephant-Tusk-Classification\data\labels\val'
test_labels_dir = r'C:\Users\Samya\PycharmProjects\Elephant-Tusk-Classification\data\labels\test'

yolov5_loc = "C:/Users/Samya/PycharmProjects/Elephant-Tusk-Classification/yolov5"
trained_model_path = r'C:/Users/Samya/PycharmProjects/Elephant-Tusk-Classification/yolov5/runs/train/itr9_b4_e3/weights/best.pt'

train_command = [
    "python", "train.py",
    "--img", "960",
    "--batch", "4",
    "--epochs", "3",
    "--data", "data/data.yaml",
    "--weights", "yolov5s.pt",
    "--device", "0",
    "--name", "itr9_b4_e3"
]
model_save_path = 'C:/Users/Samya/PycharmProjects/Elephant-Tusk-Classification/yolov5/saved_models/model5.onnx'
