import os
from faker import Faker
from patient import Patient
from tags import addTags

data_path = 'C:\dane\BRATS-2019-data\BraTS_data_dicom_copy'

fake = Faker()

shuffle = 0
modality = ['FLAIR', 'SEG', 'T1', 'T1CE', 'T2']
nModalities = len(modality)

for dcm_file in os.scandir(data_path):

    if shuffle % nModalities == 0:
        patientData = Patient(fake)

    addTags(dcm_file.path, patientData, modality[shuffle % nModalities])

    shuffle = shuffle + 1
