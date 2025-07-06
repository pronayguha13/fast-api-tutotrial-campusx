from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional


class Patient(BaseModel):
    id: Annotated[str, Field(..., description="ID of the patient")]
    name: Annotated[str, Field(..., description="Name of the patient", max_length=255)]
    city: Annotated[str, Field(..., description="City where the appointment is taken")]
    age: Annotated[
        int,
        Field(
            ...,
            description="Age of the patient",
            gt=0,
        ),
    ]
    gender: Annotated[str, Field(Literal["male", "female", "others"])]
    height: Annotated[
        float, Field(..., description="Height of the patient in metre", gt=0)
    ]
    weight: Annotated[
        float, Field(..., description="Weight of the patient in kg", gt=0)
    ]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round((self.weight) / (self.height**2), 2)

        return bmi

    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return "underweight"
        elif self.bmi < 25:
            return "normal"
        elif self.bmi < 30:
            return "normal"
        else:
            return "obese"


class PatientUpdate(BaseModel):
    name: Annotated[
        Optional[str],
        Field(max_length=255, default=None),
    ]
    city: Annotated[
        Optional[str],
        Field(default=None),
    ]
    age: Annotated[
        Optional[int],
        Field(gt=0, default=None),
    ]
    gender: Annotated[
        Optional[Literal["male", "female", "others"]], Field(default="male")
    ]
    height: Annotated[Optional[float], Field(gt=0, default=None)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]
