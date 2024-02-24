from typing import Optional, List
from fastapi import APIRouter, Request, Body, status, HTTPException
from fastapi.responses import Response
from fastapi.encoders import jsonable_encoder
from models import CarModel, UpdateCarModel, CarCollection
from bson import ObjectId
from pymongo import ReturnDocument

router = APIRouter()

@router.get(
    "/", 
    response_description="List all cars",
    response_model=CarCollection,
    response_model_by_alias=False,)
async def list_cars(
    request: Request,
    min_price: int=0,
    max_price: int=100000,
    brand: Optional[str] = None,
    page: int=1
    ):
    """
    List all of the student data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    RESULTS_PER_PAGE = 25
    skip = (page - 1)*RESULTS_PER_PAGE
    query = {"price": {"$lt": max_price, "$gt": min_price}}
    if brand:
        query["brand"] = brand
    
    full_query = request.app.mongodb["cars"].find(query).sort("_id", -1).skip(skip).limit(RESULTS_PER_PAGE)
    return CarCollection(cars=await full_query.to_list(RESULTS_PER_PAGE))

@router.post(
    "/", 
    response_description="Add new car",
    response_model=CarModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,)
async def create_car(request: Request, car: CarModel = Body(...)):
    print(car)
    new_car = await request.app.mongodb["cars"].insert_one(car.model_dump(by_alias=True, exclude=["id"]))
    created_car = await request.app.mongodb["cars"].find_one({"_id": new_car.inserted_id})
    return created_car

@router.get(
    "/{id}",
    response_description="Get a single car",
    response_model=CarModel,
    response_model_by_alias=False,
)
async def show_car(id: str, request: Request):
    """
    Get the record for a specific car, looked up by `id`.
    """
    if (
        car := await request.app.mongodb["cars"].find_one({"_id": ObjectId(id)})
    ) is not None:
        return car

    raise HTTPException(status_code=404, detail=f"Car {id} not found")


@router.put(
    "/{id}",
    response_description="Update a car",
    response_model=CarModel,
    response_model_by_alias=False,
)
async def update_car(id: str, request: Request, car: UpdateCarModel = Body(...)):
    """
    Update individual fields of an existing car record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    car = {
        k: v for k, v in car.model_dump(by_alias=True).items() if v is not None
    }

    if len(car) >= 1:
        update_result = await request.app.mongodb["cars"].find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": car},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"car {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_car := await request.app.mongodb["cars"].find_one({"_id": id})) is not None:
        return existing_car

    raise HTTPException(status_code=404, detail=f"car {id} not found")


@router.delete("/{id}", response_description="Delete a car")
async def delete_car(id: str, request: Request):
    """
    Remove a single car record from the database.
    """
    delete_result = await request.app.mongodb["cars"].delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"car {id} not found")
