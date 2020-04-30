import tensorflow as tf
from .preprocess import convert_brats_data

convert_brats_data("data/original", "data/preprocessed")

print(tf.__version__)
