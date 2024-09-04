import tensorflow as tf
import keras
import torch
import torchvision

print(tf.__version__, keras.__version__)

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))

print(torch.__version__)
print(torchvision.__version__)

print("CUDA available: ", torch.cuda.is_available())
