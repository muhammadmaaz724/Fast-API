from fastapi import FastAPI
import json

app = FastAPI()

def load_data():
    with open('data.json','r') as f:
        data = json.load(f)
        
    return data

@app.get("/")
def home():
    return ({'message':"This is my api learning journey"})

@app.get("/about")
def about():
    return({'message':'My name is Muhammad Maaz and I am a software Engineer'})

@app.get("/view")
def view():
    data = load_data()
    
    return data