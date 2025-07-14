from fastapi import FastAPI
import json

app = FastAPI()

def load():
    with open("data.json",'r') as f:
        data = json.load(f)
    return data

@app.get("/")
def home():
    return({'Message':"This is a learning website"})

@app.get("/about")
def about():
    return({"Message":"I am a Software Engineer"})

@app.get("/view")
def view_records():
    data = load()
    
    return data