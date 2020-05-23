import SimpleITK as sitk
import os
from os import walk
import sys
from PIL import Image
import numpy as np
import pydicom
from pathlib import Path

def readImageFromDir(inputDir):
    reader = sitk.ImageSeriesReader()

    dicom_names = reader.GetGDCMSeriesFileNames(inputDir)
    reader.SetFileNames(dicom_names)

    image = reader.Execute()
    return image

def pngToDicom(pngPath, dicomPath, outputPath):
    im_frame = Image.open(pngPath)
    ds = pydicom.dcmread(dicomPath)
    np_frame = np.array(im_frame.getdata(),dtype=np.uint8)
    ds.Rows = im_frame.height
    ds.Columns = im_frame.width
    ds.PhotometricInterpretation = "MONOCHROME1"
    ds.SamplesPerPixel = 1
    ds.BitsStored = 8
    ds.BitsAllocated = 8
    ds.HighBit = 7
    ds.PixelRepresentation = 0
    ds.PixelData = np_frame.tobytes()
    ds.save_as(outputPath)


def convertPngToDicom(in_folder, out_folder):
    dcm_truth_dirs = ["DICOM_anon", "Ground"]
    for (dirpath, dirnames, filenames) in walk(in_folder):
        for dirNo in dirnames:
            out_img_dir = os.path.join(out_folder, dirNo)
            Path(out_img_dir).mkdir(parents=True, exist_ok=True)
            dcm_path = os.path.join(dirpath, dirNo, dcm_truth_dirs[0])
            groundPath = os.path.join(dirpath, dirNo, dcm_truth_dirs[1])
            for (dirDcmPath, dirDcmNames, dcmFilenames), (dirGroundPath, dirGroundNames, groundFilenames) in zip(walk(dcm_path), walk(groundPath)):
                for dcmName, pngName in zip(dcmFilenames, groundFilenames):
                    out_img = os.path.join(out_img_dir, "ground" + dcmName)
                    pngToDicom(os.path.join(dirGroundPath, pngName), os.path.join(dirDcmPath, dcmName), out_img)
            # image = readImageFromDir(os.path.join(samplepath, dcm_truth_dir))
            # save_image_to_nifti(image, out_folder, dirNo)


# def readAndConvertAll(in_folder, out_folder):
#     dcm_truth_dirs = ["DICOM_anon", "Ground"]
#     for (dirpath, dirnames, filenames) in walk(in_folder):
#         for dirNo in dirnames:
#             dcm_path = os.path.join(dirpath, dirNo, dcm_truth_dirs[1])
#             groundPath = os.path.join(dirpath, dirNo, dcm_truth_dirs[2])
#             for (samplepath, dcm_truth_dirnames, fff) in walk(os.path.join(dirpath, dirNo)):
#                 for dcm_truth_dir in dcm_truth_dirnames:
#                     image = readImageFromDir(os.path.join(samplepath, dcm_truth_dir))
#                     save_image_to_nifti(image, out_folder, dirNo)                    


def save_image_to_nifti(image, dirOut, filename):
    writer = sitk.ImageFileWriter()

    # dicomFormat = ".dcm" # .png the same length
    # onlyName = filename[:-len(dicomFormat)]
    writer.SetFileName(os.path.join(dirOut, filename + ".nii.gz"))
    writer.Execute(image)


def main():
    dirIn = "C:/dane/CHAOS/Train_Sets/CT/test"
    dirOut = os.path.abspath("data/nifti-chaos/test2")
    convertPngToDicom(dirIn, dirOut)


if __name__ == "__main__":
    main()
