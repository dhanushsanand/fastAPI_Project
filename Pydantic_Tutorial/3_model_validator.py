from pydantic import BaseModel, EmailStr, AnyUrl, field_validator, model_validator, computed_field
from typing import List, Dict, Annotated

class Patient(BaseModel):
    name:str
    age:int
    email:EmailStr
    contact_details:Dict[str, str]
    allergies:List[str]
    weight:float
    married:bool
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency_contact' not in model.contact_details:
            raise ValueError('Emergency Contact of Patient older than 60 is mandatory')
        
        if model.weight > 70 and 'obesity_contact' not in model.contact_details:
            raise ValueError('Obesity contact must be given for patients weighing over 70kgs')
        
        return model
    

patient1 = {
    'name':'Dhanush',
    'age':61,
    'email':'dhansh@gmail.com',
    'contact_details':{
        'phone_no':'6025654666',
        'emergency_contact':'9980950515',
        'obesity_contact':'Go for a run mofo'
        },
    'weight':76.2,
    'married':True,
    'allergies':['lactose','obese']
}

patient = Patient(**patient1)

def insert_patient_details(patient:Patient):
    print(patient.name)
    print(patient.allergies)
    print('Inserted Patient Details into DB')
    
insert_patient_details(patient)