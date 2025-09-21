from fastapi import FastAPI
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