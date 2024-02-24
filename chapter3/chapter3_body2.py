from fastapi import FastAPI, Body
from pydantic import BaseModel
from typing import Dict

class InsertCar(BaseModel):
    brand: str
    model: str
    year: int

class InsertUser(BaseModel):
    username: str
    name: str
        
app = FastAPI()

@app.post("/cars")
async def new_car(data: Dict=Body(...)):
    print(data)
    return {
        "message": data
    }

@app.post("/car/user")
async def new_car_model(
car: InsertCar,
user: InsertUser,
code: int=Body(None) ):
    return {
        "car":car,
        "user":user,
        "code":code
    }