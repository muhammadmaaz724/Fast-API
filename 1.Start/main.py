from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hello():
    return({'message':"Hello Welcome to my api"})

@app.get("/about")
def about():
    return({'message':'I am Muhammad Maaz AI Engineer'})