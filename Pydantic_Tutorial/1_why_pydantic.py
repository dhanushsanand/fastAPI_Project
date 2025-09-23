from pydantic import BaseModel, EmailStr, AnyUrl, Field
from typing import List, Dict, Optional, Annotated

class Patient(BaseModel):
  name: Annotated[str, Field(max_length=50,title='Name of the patient',description='Enter the name of the patient in less than 50 characters', examples=['Dhanush','Shivanand'])]
  email:EmailStr
  linkedin_url: Optional[AnyUrl] = None
  age:int
  weight:Annotated[float, Field(ge=0,le=120, strict=True)]
  allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
  contact_details:Dict[str,str]
  married: Annotated[bool, Field(default=None, description='Is the patient married or not')]

def insert_patient_data(patient:Patient):
  print(patient.name)
  print(patient.age)
  print(patient.allergies)
  print('Inserted into Database')


#'allergies':['Gluten','Pollen']
patient_info = {'name':'Dhanush', 'age':30, 'weight':76.2,'email':'dhanush@gmail.com', 'contact_details':{'phone_num':'1234567890'}, 'married':'True'}

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