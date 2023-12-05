# pylint: disable=no-self-argument
"""Validation module for ZillowListingModel"""
from pydantic import BaseModel, validator


class ZillowListingModel(BaseModel):
    address: str
    price: float
    sqft: int
    bedrooms: int
    bathrooms: int
    house_hash: str
    street: str = None
    city: str = None
    state: str = None
    zipcode: str = None

    def __init__(__pydantic_self__, **data):
        super().__init__(**data)
        # Parse address and update the model fields
        street, city, state_zip = __pydantic_self__.address.split(",")
        __pydantic_self__.street = street.strip()
        __pydantic_self__.city = city.strip()
        state, zipcode = state_zip.strip().split(" ")
        __pydantic_self__.state = state
        __pydantic_self__.zipcode = zipcode

    @validator("sqft", "bedrooms", "bathrooms", pre=True)
    def parse_int(cls, value):
        """Convert string values to int"""
        return int(value.replace(",", ""))

    @validator("price", pre=True)
    def parse_price(cls, value):
        """Convert string price to float"""
        return float(value.replace(",", "").replace("$", ""))
