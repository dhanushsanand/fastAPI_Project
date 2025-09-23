from pydantic import AnyUrl, EmailStr, Field, BaseModel, field_validator
from typing import List, Dict, Annotated, Optional

class Patient(BaseModel):
    
    name:str
    age:Annotated[int, Field(gt=0,lt=100)]
    email:EmailStr
    weight:float
    married:bool
    allergies:Optional[List[str]] = None
    contact_details:Dict[str,str]
    
    @field_validator('email')
    @classmethod
    def email_vaidator(cls,value):
        valid_domains = ['hdfc.com','icic.com']
        domain_name = value.split('@')[-1]
        if domain_name not in valid_domains:
            raise ValueError('Not a valid domain')
        return value
    
    @field_validator('name', mode='before')
    @classmethod
    def capitalize_name(cls, value):
        return value.upper()
    
    @field_validator('age')
    @classmethod
    def age_validator(cls, value):
        if 0 < value < 100:
            return value
        return ValueError('Age must be between 0 and 100')
    
def update_patient_details(patient:Patient):
    print(patient.name)
    print(patient.age)
    print('Updated the DB')

patient1 = {'name':'Dhanush','age':'26','email':'dhanush@hdfc.com','weight':76.6,'married':True, 'contact_details':{'phone_number':'6025654666'} }

patient = Patient(**patient1)
    
update_patient_details(patient)