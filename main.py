from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
import json
from typing import Annotated, Literal, Optional

app = FastAPI()

class Patient(BaseModel):
  id:Annotated[str, Field(..., description='Id of Patient', examples=['P001'])]
  name:Annotated[str, Field(..., description='Name of the Patient')]
  city:Annotated[str, Field(..., description='City of Patient')]
  age:Annotated[int, Field(..., gt=0, lt=120)]
  gender:Annotated[Literal['male','female'], Field(..., description='Gender of the patient')]
  height:Annotated[float, Field(...,gt=0, description='Height of the patient in mtrs')]
  weight:Annotated[float, Field(..., gt=0, description='Weight of the patient in Kgs')]
  
  @computed_field
  @property
  def bmi(self)->float:
    bmi = round(self.weight/(self.height**2),2)
    return bmi
  
  @computed_field
  @property
  def verdict(self)->str:
    if self.bmi < 18.5:
      return 'Underweight'
    elif 18.5 <self.bmi < 30:
      return 'Normal'
    else:
      return 'Obese'
  

class PatientUpdate(BaseModel):
  name:Annotated[Optional[str], Field(default=None)]
  city:Annotated[Optional[str], Field(default=None)]
  age:Annotated[Optional[int], Field(default=None, gt=0, lt=120)]
  gender:Annotated[Optional[Literal['male', 'female']], Field(default=None)]
  height:Annotated[Optional[float], Field(default=None, gt=0)]
  weight:Annotated[Optional[float], Field(default=None)]


@app.post('/create')
def create_patient(patient:Patient):
  # load existing data
  data = load_data()
  
  #check if patient exists
  if patient.id in data:
    raise HTTPException(status_code=400, detail='Patient exists')
  
  #new patient added to db
  data[patient.id] = patient.model_dump(exclude={'id'})
  save_data(data)
  
  return JSONResponse(status_code=201, content={'message':'Patient creation success'})
  
    

def save_data(data):
  with open('patients.json', 'w') as file:
    json.dump(data, file)

def load_data():
  with open('patients.json', 'r') as file:
    data = json.load(file)
  return data

@app.get("/")
def hello():
  return {'message':'Patient Management System API'}

@app.get("/about")
def about():
  return {'message':'Fully Functional API to manage Patient records'}


@app.get("/view")
def view():
  return load_data()

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str = Path(..., description='ID of the patient in the DB', example='P001')):
  data = load_data()
  
  if patient_id in data:
    return data[patient_id]
  raise HTTPException(detail='Patient not found', status_code=404)

@app.get('/sort')
def sort_patients(sort_by:str = Query(...,description='Sort on the basis of height, Weight, BMI'), order:str = Query('asc',description='Sort in ascending or descending order')):
  valid_fields = ['height', 'weight', 'bmi']
  
  if sort_by not in valid_fields:
    raise HTTPException(status_code=400, detail=f'Invalid Sort field, select from {valid_fields}')
  
  if order not in ['asc','desc']:
    raise HTTPException(status_code=400, detail='Invalid Order field, select from asc or desc')
  
  data = load_data()
  
  sorted_data = sorted(data.values(),key=lambda x: x.get(sort_by,0), reverse= True if order=='desc' else False)
  
  return sorted_data
  
@app.put('/edit/{patient_id}')
def edit_patient_details(patient_id:str, patient_update:PatientUpdate):
  data = load_data()
  if patient_id not in data:
    raise HTTPException(status_code=404, detail='Patient not found')
  
  patient_details = data[patient_id]
  
  patient_update_details = patient_update.model_dump(exclude_unset=True)
  
  for key, value in patient_update_details.items():
    patient_details[key] = value
  
  patient_details['id'] = patient_id
  patient_pydantic_object = Patient(**patient_details)
  
  patient_details = patient_pydantic_object.model_dump(exclude={'id'})
  
  data[patient_id] = patient_details
  
  save_data(data)
  
  return JSONResponse(status_code=200, content={'message':'Patient updated'})
  
@app.delete('/delete/{patient_id}')
def delete_patient_details(patient_id:str = Path(...)):
  data = load_data()
  
  if patient_id not in data:
    raise HTTPException(status_code=400, detail='Patient does not exist')
  
  del data[patient_id]
  
  save_data(data)
  
  return JSONResponse(status_code=200, content={'message':'Patient deleted'})
  
  
  