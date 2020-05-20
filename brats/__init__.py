from preprocess import convert_brats_data
convert_brats_data("data/original", "data/preprocessed")

import tensorflow as tf
print(tf.__version__)