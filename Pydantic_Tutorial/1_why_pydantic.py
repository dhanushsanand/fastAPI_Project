from pydantic import BaseModel

class Patient(BaseModel):
  name:str
  age:int
  weight:float

def insert_patient_data(patient:Patient):
  print(patient.name)
  print(patient.age)
  print('Inserted into Database')

patient_info = {'name':'Dhanush', 'age':30}

patient1 = Patient(**patient_info)

#insert_patient_data(patient1)

def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print('Updated info')
    
update_patient_data(patient1)

# def insert_patient_data(name:str, age:int):
#   if(type(name) == str and type(age) == int):
#     if(age < 0):
#       raise ValueError('Age cannot be negative value')
#     print(name)
#     print(age)
#     print('Inserted into Database')
#   else:
#     raise TypeError('Incorrect data type')
  
# insert_patient_data('Dhanush', 26)