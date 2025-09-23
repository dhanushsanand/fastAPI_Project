from pydantic import AnyUrl, EmailStr, Field, BaseModel
from typing import List, Dict, Annotated, Optional

class Patient(BaseModel):
    name:str
    age:int
    email:EmailStr
    weight:float
    married:bool
    allergies:Optional[List[str]] = None
    contact_details:Dict[str,str]
    
def update_patient_details(patient:Patient):
    print(patient.name)
    print(patient.age)
    print('Updated the DB')

patient1 = {'name':'Dhanush','age':26,'email':'dhanush@gmail.com','weight':76.6,'married':True, 'contact_details':{'phone_number':'6025654666'} }

patient = Patient(**patient1)
    


update_patient_details(patient)