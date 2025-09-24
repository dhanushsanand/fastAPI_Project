from pydantic import BaseModel, computed_field, field_validator,model_validator, Field, EmailStr
from typing import List, Dict, Annotated

class Patient(BaseModel):
    name:Annotated[str, Field(max_length=50)]
    email:Annotated[EmailStr, Field(max_length=50)]
    age:Annotated[int, Field(gt=0, lt=100)]
    married:Annotated[bool, Field(False)]
    allergies:Annotated[List[str], Field(None,max_length=5)]
    contact_details:Annotated[Dict[str,str], Field(None)]
    weight:Annotated[float, Field(gt=20,lt=100)]
    height:Annotated[float, Field(gt=1, lt=2)]
    
    
    @field_validator('email', mode='before')
    @classmethod
    def validate_email(cls, value):
        valid_domains = ['hdfc.com','icic.com']
        domain = value.split('@')[-1]
        if domain not in valid_domains:
            raise ValueError('Only Employees of HDFC and ICICI get discount')
        return value
    
    
    @model_validator(mode='after')
    def validate_emergency_contact(cls, model):
        if model.age > 60 and 'emergency_contact' not in model.contact_details:
            raise ValueError('Emergency Contact is mandatory for Patients above age 60')
        return model
    
    @computed_field
    def bmi(self)->float:
        bmi = round(self.weight/(self.height**2),2)
        return bmi
    

patient1 = {
    'name':'Dhanush',
    'age':61,
    'weight':76.2,
    'height':1.77,
    'contact_details':{
        'emergency_contact':'One and only piece'
    },
    'email':'dhanush@hdfc.com'
}

patient = Patient(**patient1)

def insert_patient_details(patient:Patient):
    print(patient.name)
    print(patient.contact_details)
    print('BMI', patient.bmi)
    print('Inserted Patient Details into DB')
 
insert_patient_details(patient)       