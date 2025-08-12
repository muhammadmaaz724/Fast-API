from fastapi import FastAPI, Path, HTTPException, Query
import json

app = FastAPI()

def load_data():
    with open('data.json','r') as f:
        data = json.load(f)
        
    return data

@app.get('/')
def home():
    return({'message':'This is my homepage'})

@app.get('/patient/{patient_id}')
def view_patient(patient_id:str=Path(...,description="ID of the patient",example='P001')):
    data = load_data()
    
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="patient not found")

@app.get("/sort")
def sort(sort_by:str=Query(...,description="sort by the value height, weight or bmi"), order_by:str = Query("asc",description="Order of the sorting Asc or Desc")):
    
    valid_fields = ['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail= f"Bad Request from the client select from {valid_fields}")
    if order_by not in ['asc','desc']:
        raise HTTPException(status_code=400,detail='Bad request select from asc or desc')
    
    data = load_data()
    
    sort_flag = True if order_by=='desc' else False
    sorted_data = sorted(data.values(),key=lambda x:x.get(sort_by,0), reverse=sort_flag)
    
    return sorted_data