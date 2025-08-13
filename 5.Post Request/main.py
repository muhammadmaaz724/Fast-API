from fastapi import FastAPI,HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal
import json

class patient(BaseModel):
    patient_id: Annotated[str,Field(...,description="Id of the patient",examples=['P001'])]
    name: Annotated[str,Field(...,description="Name of the patient")]
    city: Annotated[str,Field(...,description="City where the patient lives")]
    age: Annotated[int,Field(...,gt=0,description="Age of the patient in years")]
    gender: Annotated[Literal['male','female','other'],Field(...,description="Gender of the patient")]
    height: Annotated[float,Field(...,gt=0,description="Height of the patient in meters")]
    weight: Annotated[float,Field(...,gt=0,description="Weight of the patient in Kgs")]
    
    @computed_field
    @property
    def bmi(self) -> float:
        return round(self.weight/(self.height**2),2)
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'Underweight'
        
        elif self.bmi >= 18.5 and self.bmi <= 24.9:
            return 'Normal'
        
        elif self.bmi >=25 and self.bmi <= 29.9:
            return 'Overweight'
        
        elif self.bmi >=30:
            return 'Obese'

def load_data():
    with open('data.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('data.json','w') as f:
        json.dump(data,f)

app = FastAPI()

@app.get('/')
def home():
    return({'message':'Welcome to My API'})

@app.post("/create")
def create(patient: patient):
    data = load_data()
    
    if patient.patient_id in data:
        raise HTTPException(status_code=400, detail="The patient already exists")
    
    data[patient.patient_id] = patient.model_dump(exclude=['patient_id'])
    
    save_data(data)
    
    return JSONResponse(status_code=201, content={'message':'The patient record is created'})
    


    