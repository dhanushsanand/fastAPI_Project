from pydantic import BaseModel

class Address(BaseModel):
    city:str
    state:str
    pin:str

class Patient(BaseModel):
    name:str
    gender:str = 'Male'
    age:int
    address:Address
    
    
address_dict = {
    'city':'Tumakuru',
    'state':'Karnataka',
    'pin':'572103'
}

address = Address(**address_dict)

patient_dict = {
    'name':'Dhanush',
    'age':26,
    'address':address
}

patient = Patient(**patient_dict)

def insert_patient_data(patient:Patient):
    print(patient.name)
    print(patient.address)
    print('Inserted Patient into DB')
    
#insert_patient_data(patient)

temp = patient.model_dump(exclude={'address':{'state'}}, exclude_unset=False)

print(temp)
print(type(temp))