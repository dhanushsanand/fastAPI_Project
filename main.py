from fastapi import FastAPI, Path, HTTPException
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