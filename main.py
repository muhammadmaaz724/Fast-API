from fastapi import FastAPI

app = FastAPI()

@app.get('/')

def Hello():
    return({'message':"Hello World"})

@app.get("/about")
def about():
    return({"message":"I am Muhammad Maaz"})