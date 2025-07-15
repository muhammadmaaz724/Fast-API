from fastapi import FastAPI,Path,HTTPException,Query
import json

app = FastAPI()

def load():
    with open("data.json",'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def home():
    return({"message":"This is home page"})

@app.get('/patient/{patient_id}')
def PatientById(patient_id: str = Path(...,description="Put the patient ID here",example="P001")):
    data = load()
    if patient_id in data:
        return(data[patient_id])
    raise HTTPException(status_code=404,detail="Item not found")

@app.get('/sort')
def sort(sort_by:str=Query(...,description="sort by height, weight or bmi"),
         order:str=Query('asc',description="Asc or Desc order")):
    
    valid_fields = ['height','weight','bmi']
    
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail="Invalid input choose height, weight or bmi")
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Invalide input please enter asc or desc")
    
    data = load()
    
    sort_order = True if order == 'desc' else False
    
    sorted_data = sorted(data.values(),key=lambda x: x.get(sort_by,0),reverse=sort_order)
    
    return sorted_data