from typing import Optional, List
from typing_extensions import Annotated
from bson import ObjectId
from pydantic import ConfigDict, BaseModel, Field
from pydantic.functional_validators import BeforeValidator
from pymongo import ReturnDocument

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

class CarModel(BaseModel):
    """
    Container for a single car record.
    """

    # The primary key for the CarModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias='_id', default=None)
    brand: str = Field(..., min_length=1)
    make: str = Field(..., min_length=1)
    year: int = Field(...)
    price: int = Field(...)
    km: int = Field(...)
    cm3: int = Field(...)
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "brand": "Mercedes",
                "make": "BMW",
                "year": 1976,
                "price": 40000,
                "km": 18000,
                "cm3": 1500
            }
        }
    )

class UpdateCarModel(BaseModel):
    """
    A set of optional updates to be made to a document in the database.
    """

    brand: Optional[str] = None
    make: Optional[str] = None
    year: Optional[int] = 1970
    price: Optional[int] = 0
    km: Optional[int] = 0
    cm3: Optional[int] = 0
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "brand": "Mercedes",
                "make": "BMW",
                "year": 1976,
                "price": 40000,
                "km": 18000,
                "cm3": 1500
            }
        }
    )

class CarCollection(BaseModel):
    """
    A container holding a list of `CarModel` instances.

    This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    cars: List[CarModel]