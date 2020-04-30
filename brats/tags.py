import pydicom


def add_tags(path, patient, modality):
    ds = pydicom.read_file(path)  # (rtplan.dcm is in the testfiles directory)

    ds[0x10, 0x10].value = patient.name
    ds[0x10, 0x20].value = patient.patientId
    ds[0x10, 0x30].value = patient.birth
    ds.StudyID = patient.studyId
    ds[0x08, 0x60].value = modality

    # print(f'Patientname: {ds[0x10, 0x10].value}, modality: {modality}')
    ds.save_as(path)


def copy_tags(from_path, to_path):

    print(from_path, to_path)

    ds = pydicom.read_file(from_path)

    dicom_data = X('x')
    dicom_data.name = ds[0x10, 0x10].value
    dicom_data.patientId = ds[0x10, 0x20].value
    dicom_data.birth = ds[0x10, 0x30].value
    dicom_data.studyId = ds.StudyID
    dicom_data.modality = ds[0x08, 0x60].value

    ts = pydicom.read_file(to_path)

    ts[0x10, 0x10].value = dicom_data.name
    ts[0x10, 0x20].value = dicom_data.patientId
    ts[0x10, 0x30].value = dicom_data.birth
    ts.StudyID = dicom_data.studyId
    ts[0x08, 0x60].value = "PRED"

    ts.save_as(to_path)


class X(str):
    pass


if __name__ == "__main__":
    import os
    from_path = os.path.abspath("data/test/t1.dcm")
    to_path = os.path.abspath("data/test/t1.dcm")
    copy_tags(from_path, to_path)
