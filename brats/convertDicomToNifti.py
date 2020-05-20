import SimpleITK as sitk
import os
from os import walk


def readAndConvertAll(in_folder, out_folder):
    for (dirpath, dirnames, filenames) in walk(in_folder):
        for file in filenames:
            read_dicom_save_nifti(dirpath, out_folder, file)


def read_dicom_save_nifti(dirIn, dirOut, filename):

    dicom_path = os.path.join(dirIn, filename)
    reader = sitk.ImageFileReader()
    reader.SetFileName(dicom_path)
    image1 = reader.Execute()
    writer = sitk.ImageFileWriter()

    dicomFormat = ".dcm"
    onlyName = filename[:-len(dicomFormat)]
    writer.SetFileName(os.path.join(dirOut, onlyName + ".nii.gz"))
    writer.Execute(image1)


def main():
    dirIn = os.path.abspath("data/dicom")
    dirOut = os.path.abspath("data/converted")
    readAndConvertAll(dirIn, dirOut)


if __name__ == "__main__":
    main()
