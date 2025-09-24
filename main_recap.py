from fastapi import FastAPI, Path, Query, HTTPException
import json

app = FastAPI()

def load_data():
    with open('patients.json','r') as file:
        data = json.load(file)
        return data

@app.get('/')
def home_page():
    return {'Home Page': 'Welcome to Patient Management System'}

@app.get('/view')
def view_patients():
    return load_data()

@app.get('/view/{patient_id}')
def get_specific_patient(patient_id:str = Path(..., description='Enter Patient Id to get details', example='P001')):
    data = load_data()
    return data[patient_id]

@app.get('/sort')
def sort_patients(sort_by:str = Query(...,description='Select from the fields height, weight and bmi to sort patients'), order:str = Query('asc',description='Optional Parameter to sort ASC or DESC')):
    valid_fields = ['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(detail='Select from height, weight or bmi only',status_code=400)
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400, detail='Select only asc or desc')
    
    data = load_data()
    sorted_data = sorted(data.values(), key= lambda x : x.get(sort_by, 0), reverse= True if order=='desc' else False)
    return sorted_data