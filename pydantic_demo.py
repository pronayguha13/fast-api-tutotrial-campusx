from pydantic import (
    AnyUrl,
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
    computed_field,
)
from typing import List, Dict, Optional, Annotated


class Address(BaseModel):
    city: str
    state: str
    pincode: int


class Patient(BaseModel):
    name: Annotated[
        str,
        Field(
            max_length=255,
            title="Name of the patient",
            description="Give the name of the patient in less than 255 character",
        ),
    ]
    email: EmailStr
    linkedin_url: AnyUrl
    age: Annotated[int, Field(gt=0, le=80)]
    weight: Annotated[float, Field(gt=0, strict=True)]
    height: Annotated[float, Field(gt=0)]
    married: Annotated[
        bool, Field(default=False, description="Marital status of the patient")
    ]
    allergies: Annotated[Optional[List[str]], Field(default=None, max_length=5)]
    contact_details: Dict[str, str]
    address: Address

    @field_validator("email")
    @classmethod
    def email_validator(cls, value):
        valid_domains = ["hdfc.com", "icici.com"]
        domain_name = value.split("@")[1]
        if domain_name not in valid_domains:
            raise ValueError("Not a valid domain")
        return value

    @field_validator("name")
    @classmethod
    def transform_name(cls, value):
        return value.upper()

    """
        mode = [before/after]
        default value of mode is after
        mode = before <=> before the input value is coerced to the model type
        mode = after <=> after the input value is coerced to the model type
    """

    @field_validator("age", mode="before")
    @classmethod
    def validate_age(cls, value):
        if 0 < value < 100:
            return value
        else:
            raise ValueError("Age must be between and 100")

    """_summary_
        validate multiple fields
        have access to all the field in the model
        
        """

    @model_validator(mode="after")
    def validate_emergency_contact(cls, model):
        if model.age > 60 and "emergency" not in model.contact_details:
            raise ValueError(
                "Patient above the age of 60 should have an emergency contact number"
            )
        else:
            return model

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight / (self.height**2))
        return bmi


patient_info = {
    "name": "Pronay",
    "email": "abc@hdfc.com",
    "linkedin_url": "http://linkedin.com/pronayguha",
    "age": 66,
    "weight": 75.2,
    "height": 1.72,
    "married": True,
    "allergies": ["Pollen", "Dust"],
    "contact_details": {"emergency": "1234567890", "phone": "2344556"},
}

patient1 = Patient(**patient_info)


def insert_patient_data(patient: Patient):
    print(patient.name)
    print(patient.age)
    print(patient.married)
    print(patient.allergies)
    print(patient.bmi)
    print("Inserted successfully")


insert_patient_data(patient1)
