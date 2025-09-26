from fastapi import FastAPI
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import pickle
import pandas as pd

with open('model.pkl', 'rb') as file:
    model = pickle.load(file)
    
tier_1_cities = [
    "Mumbai", "Delhi", "Bangalore", "Chennai", 
    "Kolkata", "Hyderabad", "Pune"
]

tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

class UserInput(BaseModel):
    age:Annotated[int, Field(..., gt=0,le=120, description='Age of the user')]
    weight:Annotated[float, Field(..., gt =0, description='Weight of the patient')]
    height:Annotated[float, Field(..., gt=0, lt=2.5, description='Height of user')]
    income_lpa:Annotated[float, Field(..., gt=0, description='Annual Salary in lpa')]
    smoker:Annotated[bool, Field(default=False)]
    city:Annotated[str, Field(...)]
    occupation:Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'], Field(...)]
    
    @computed_field
    @property
    def bmi(self)->float:
        return self.weight/(self.height**2)
    
    @computed_field
    @property
    def age_group(self)->str:
        if self.age < 25:
            return 'young'
        if self.age < 45:
            return 'adult'
        if self.age < 60:
            return 'middle_aged'
        return 'senior'
    
    @computed_field
    @property
    def lifestyle_risk(self)->str:
        if self.smoker and self.bmi > 30:
            return 'high'
        if self.smoker or self.bmi > 27:
            return 'medium'
        return 'low'
    
    @computed_field
    @property
    def city_tier(self)->int:
        if self.city in tier_1_cities:
            return 1
        if self.city in tier_2_cities:
            return 2
        return 3
    
    
    
    

app = FastAPI()

@app.post('/predict')
def predict_premium(data:UserInput):
    input = pd.DataFrame([
        {
            'bmi':data.bmi,
            'age_group':data.age_group,
            'lifestyle_risk':data.lifestyle_risk,
            'city_tier':data.city_tier,
            'income_lpa':data.income_lpa,
            'occupation':data.occupation
        }
    ])
    
    prediction = model.predict(input)[0]
    
    return JSONResponse(status_code=200, content={'predicted_category':prediction})
    
    