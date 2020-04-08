from brats.dicom.tags import copy_tags
from brats.train_isensee2017 import config, write_data_to_file
import os
import glob
import tables
import numpy as np
import nibabel as nib
import SimpleITK as sitk

from unet3d.prediction import predict, patch_wise_prediction, prediction_to_image
from unet3d.training import load_old_model


def read_dicom_save_nifti(dir, modality):
    dicom_path = os.path.join(dir, modality + ".dcm")
    reader = sitk.ImageFileReader()
    reader.SetFileName(dicom_path)
    image1 = reader.Execute()
    writer = sitk.ImageFileWriter()
    writer.SetFileName(os.path.join(dir, modality + ".nii.gz"))
    writer.Execute(image1)


def fetch_training_data_files(return_subject_ids=False):
    training_data_files = list()
    subject_ids = list()
    for subject_dir in glob.glob(config["to_predict_path"]):
        subject_ids.append(os.path.basename(subject_dir))
        subject_files = list()
        for modality in config["training_modalities"] + ["flair"]:
            read_dicom_save_nifti(subject_dir, modality)
            subject_files.append(os.path.join(subject_dir, modality + ".nii.gz"))
        training_data_files.append(tuple(subject_files))
    if return_subject_ids:
        return training_data_files, subject_ids
    else:
        return training_data_files


def predict_from_file(hdf5_file):
    data_index = 0
    data_file = tables.open_file(hdf5_file, "r")
    affine = data_file.root.affine[data_index]
    test_data = np.asarray([data_file.root.data[data_index]])

    training_modalities = config["training_modalities"]
    output_dir = config["prediction_output"]

    for i, modality in enumerate(training_modalities):
        image = nib.Nifti1Image(test_data[0, i], affine)
        image.to_filename(os.path.join(
            output_dir, "data_{0}.nii.gz".format(modality)))

    model_file = config["model_file"]
    model = load_old_model(model_file)
    patch_shape = tuple([int(dim) for dim in model.input.shape[-3:]])
    if patch_shape == test_data.shape[-3:]:
        prediction = predict(model, test_data)  # care permute=permute
    else:
        labels = config["labels"]
        output_label_map = True
        threshold = 0.5
        permute = False
        overlap = 16

        prediction = patch_wise_prediction(
            model=model, data=test_data, overlap=overlap, permute=permute)[np.newaxis]
    prediction_image = prediction_to_image(prediction, affine, label_map=output_label_map, threshold=threshold,
                                           labels=labels)
    if isinstance(prediction_image, list):
        for i, image in enumerate(prediction_image):
            image.to_filename(os.path.join(
                output_dir, "prediction_{0}.nii.gz".format(i + 1)))
    else:
        path_name = os.path.join(output_dir, "prediction.nii.gz")
        prediction_image.to_filename(path_name)
        img = sitk.ReadImage(path_name)
        sitk.WriteImage(img, "prediction/prediction4.dcm")


def main(overwrite=False):
    config["data_file"] = os.path.abspath("predict_data.h5")
    config["to_predict_path"] = os.path.join(os.path.dirname(__file__), "data", "toPredict", "*")
    config["prediction_output"] = os.path.abspath("prediction")

    training_files, subject_ids = fetch_training_data_files(True)
    write_data_to_file(training_files, config["data_file"], image_shape=config["image_shape"], subject_ids=subject_ids)
    predict_from_file(config["data_file"])

    subject_dir = glob.glob(config["to_predict_path"])[0]
    example_dicom_tags = os.path.join(subject_dir, "flair.dcm")
    dicom_to_override = os.path.join(config["prediction_output"], "prediction4.dcm")
    copy_tags(example_dicom_tags, dicom_to_override)


if __name__ == "__main__":
    main(overwrite=config["overwrite"])
