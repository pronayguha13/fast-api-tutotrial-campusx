from pydantic import BaseModel, Field
from typing import Annotated, Optional


class Address(BaseModel):
    city: str
    state: str
    pincode: int


class Patient(BaseModel):
    name: str = Field(max_length=255)
    gender: str = Field(default="Male")
    address: Address


addr = {"city": "Kolkata", "state": "West Bengal", "pincode": 700122}

addr_obj = Address(**addr)


p = {
    "name": "Pronay",
    # "gender": "Male",
    "address": addr_obj,
}

patient1 = Patient(**p)

print(patient1.address.city)

temp = patient1.model_dump()
print(temp, type(temp))

temp_json = patient1.model_dump_json()

print(temp_json, type(temp_json))
