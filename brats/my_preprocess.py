import sys
sys.path.append('C:/repos/3DUnetCNN')

from preprocess import convert_brats_data

convert_brats_data("data/original", "data/prep-tumor")

