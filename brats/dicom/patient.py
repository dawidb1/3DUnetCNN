class Patient:

    def __init__(self, fake):
        self.name = fake.last_name() + ' ' + fake.first_name()
        self.patientId = fake.uuid4()
        self.studyId = fake.uuid4()
        self.birth = self.fakeDate(fake)

    def fakeDate(self, fake):
        return fake.date(pattern='%Y%m%d')

    def __str__(self):
        return "Patientname: {0}, Birthname: {1}, StudyId: {2}, PatientId: {3}".format(self.name, self.birth, self.studyId, self.patientId)
