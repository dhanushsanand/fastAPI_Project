from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

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
  