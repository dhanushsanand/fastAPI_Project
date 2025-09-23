from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional

class Patient(BaseModel):
  name:str
  email:EmailStr
  linkedin_url: AnyUrl
  age:int
  weight:float = Field(gt=0, lt=120)
  allergies:Optional[List[str]] = Field(max_length=5)
  contact_details:Dict[str,str]
  married:Optional[bool] = False

def insert_patient_data(patient:Patient):
  print(patient.name)
  print(patient.age)
  print(patient.allergies)
  print('Inserted into Database')


#'allergies':['Gluten','Pollen']
patient_info = {'name':'Dhanush', 'age':30, 'weight':76.2,'email':'dhanush@gmail.com', 'contact_details':{'phone_num':'1234567890','email':'abc@gmail.com'}}

patient1 = Patient(**patient_info)

#insert_patient_data(patient1)

def update_patient_data(patient:Patient):
    print(patient.name)
    print(patient.age)
    print(patient.allergies)
    print(patient.married)
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