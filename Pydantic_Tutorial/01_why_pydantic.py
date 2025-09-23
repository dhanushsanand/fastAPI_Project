from pydantic import BaseModel

class Patient(BaseModel):
    name:str
    age:int
    weight:float


def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print('Inserted into DB')

patient = {'name':'Dhanush', 'age':26, 'weight':77.2}
patient1 = Patient(**patient)
insert_patient_data(patient1)