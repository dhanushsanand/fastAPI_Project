import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import classification_report, accuracy_score
import numpy as mp
import pickle

df = pd.read_csv('insurance.csv')

df_feature = df.copy()

df_feature['bmi'] = df_feature['weight']/(df_feature['height']**2)

def age_group(age):
    if age< 25:
        return 'young'
    if age < 45:
        return 'adult'
    if age < 60:
        return 'middle_aged'
    else:
        return 'senior'
    
df_feature['age_group'] = df_feature['age'].apply(age_group)

def lifestyle_risk(row):
    if row['smoker'] and row['bmi'] > 30:
        return 'high'
    if row['smoker'] and row['bmi'] > 27:
        return 'medium'
    else:
        return 'low'

df_feature['lifestyle_risk'] = df_feature.apply(lifestyle_risk,axis=1)

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

def city_tier(city):
    if city in tier_1_cities:
        return 1
    if city in tier_2_cities:
        return 2
    else:
        return 3

df_feature['city_tier'] = df['city'].apply(city_tier)

df_feature.drop(columns=['age','weight','height','smoker','city'])[['income_lpa','occupation','bmi','age_group','lifestyle_risk','city_tier','insurance_premium_category']]
    
X = df_feature[['income_lpa','occupation','bmi','age_group','lifestyle_risk','city_tier']]
y = df_feature[['insurance_premium_category']]

categorical_features = ['age_group','lifestyle_risk','city_tier','occupation']
numerical_features = ['income_lpa','bmi']

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(), categorical_features),
    ('num','passthrough',numerical_features)
    ]
)

pipeline = Pipeline(steps=[
    ('preprocessor',preprocessor),
    ('classifier',RandomForestClassifier(random_state=42))
])


X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.2, random_state=1)
pipeline.fit(X_train, y_train)

y_pred = pipeline.predict(X_test)
accuracy_score(y_test, y_pred)

pickle_model_path = 'model.pkl'
with open(pickle_model_path,'wb') as file:
    pickle.dump(pipeline,file)