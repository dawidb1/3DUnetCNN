import SimpleITK as sitk
import os
from os import walk
import sys
from PIL import Image
import numpy as np
import pydicom
from pathlib import Path
import uuid

def readImageFromDir(inputDir):
    reader = sitk.ImageSeriesReader()

    # reading all files, not the same series
    # dicom_names = reader.GetGDCMSeriesFileNames(inputDir)
    for (dirpath, dirnames, names) in walk(inputDir):
        filenames = [os.path.join(dirpath, name) for name in names]

    reader.SetFileNames(filenames)
    image = reader.Execute()
    return image

def pngToDicom(pngPath, dicomPath, outputPath, studyUid, seriesUid):
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
    ds.StudyInstanceUID = studyUid
    ds.SeriesInstanceUID = seriesUid
    ds.save_as(outputPath)


def convertPngToDicom(in_folder, out_folder):
    dcm_truth_dirs = ["DICOM_anon", "Ground"]
    for (dirpath, dirnames, filenames) in walk(in_folder):
        for dirNo in dirnames:
            out_dcm_img_dir = os.path.join(out_folder, dirNo, dcm_truth_dirs[0])
            out_ground_img_dir = os.path.join(out_folder, dirNo, dcm_truth_dirs[1])

            Path(out_ground_img_dir).mkdir(parents=True, exist_ok=True)
            Path(out_dcm_img_dir).mkdir(parents=True, exist_ok=True)

            dcm_path = os.path.join(dirpath, dirNo, dcm_truth_dirs[0])
            groundPath = os.path.join(dirpath, dirNo, dcm_truth_dirs[1])
            for (dirDcmPath, dirDcmNames, dcmFilenames), (dirGroundPath, dirGroundNames, groundFilenames) in zip(walk(dcm_path), walk(groundPath)):
                for dcmName, pngName in zip(dcmFilenames, groundFilenames):
                    seriesUid = str(uuid.uuid4())
                    studyUid = str(uuid.uuid4())
                    out_img = os.path.join(out_ground_img_dir, "ground" + dcmName)
                    pngToDicom(os.path.join(dirGroundPath, pngName), os.path.join(dirDcmPath, dcmName), out_img, studyUid, seriesUid)

                    dcmImagePath = os.path.join(dirDcmPath, dcmName) 
     
                    img = sitk.ReadImage(out_img)
    
                    binaryImg = otsuBinaryTh(img)
                    sitk.WriteImage(binaryImg, out_img)
                    copyDicom(dcmImagePath, os.path.join(out_dcm_img_dir, dcmName))

def showImage(img, title):
    image_viewer = sitk.ImageViewer()
    image_viewer.SetApplication('C:/Program Files/ITK-SNAP 3.8/bin/ITK-SNAP.exe')
    image_viewer.SetTitle(title)
    image_viewer.Execute(img)

def readImage(imagePath):
    img = sitk.ReadImage(imagePath)

def binaryThreshold(img):
    seg = sitk.BinaryThreshold(img,
                           lowerThreshold=-1000, upperThreshold=1300,
                           insideValue=1, outsideValue=0)
    return seg

def otsuBinaryTh(img):
    otsu_filter = sitk.OtsuThresholdImageFilter()
    otsu_filter.SetInsideValue(0)
    otsu_filter.SetOutsideValue(1)
    seg = otsu_filter.Execute(img)
    return seg

def copyDicom(in_dir, out_dir):
    ds = pydicom.dcmread(in_dir)
    ds.save_as(out_dir)


def readSeriesAndSaveAsFile(in_folder, out_folder):
    dcm_truth_dirs = ["DICOM_anon", "Ground"]
    for (dirpath, dirnames, filenames) in walk(in_folder):
        for dirNo in dirnames:
            dcm_path = os.path.join(dirpath, dirNo, dcm_truth_dirs[0])
            groundPath = os.path.join(dirpath, dirNo, dcm_truth_dirs[1])
            for (samplepath, dcm_truth_dirnames, fff) in walk(os.path.join(dirpath, dirNo)):
                for dcm_truth_dir in dcm_truth_dirnames:
                    image = readImageFromDir(os.path.join(samplepath, dcm_truth_dir))

                    new_out_dir = os.path.join(out_folder,dirNo)
                    Path(new_out_dir).mkdir(parents=True, exist_ok=True)

                    saveImage(image, new_out_dir, dcm_truth_dir + ".nii.gz")                    

def saveImage(image, dirOut, filename):
    writer = sitk.ImageFileWriter()
    writer.SetFileName(os.path.join(dirOut, filename))
    writer.Execute(image)
    

def main():
    dirIn = "C:/dane/CHAOS/Train_Sets/CT"
    dirOut = os.path.abspath("data/chaos/dicom2ds")
    convertPngToDicom(dirIn, dirOut)
    in_folder = dirOut
    out_folder = "data/chaos/nifti"
    readSeriesAndSaveAsFile(in_folder, out_folder)


if __name__ == "__main__":
    main()
