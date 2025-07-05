from fastapi import FastAPI, Path, HTTPException, Query
import json


app = FastAPI()


def load_data():
    with open("Patients.json", "r") as f:
        data = json.load(f)
        return data


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/about")
def about():
    return {"message": "This is the about route"}


@app.get(path="/get-all-patient", description="Fetch all the patient data from the DB")
def get_all_patients():
    data = load_data()
    return data


@app.get("/patient/{patient_id}")
def get_patient(
    patient_id: str = Path(
        ..., description="ID of the patient in the DB", example="POO1"
    )
):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="Patient not found")


@app.get("/sort")
def sort_patients(
    sort_by: str = Query(
        ..., description="Sort on the basis of height , weight and BMI"
    ),
    order: str = Query("asc", description="Order of sorting"),
):
    valid_fields = ["height", "weight", "bmi"]
    if sort_by not in valid_fields:
        raise HTTPException(
            status_code=400, detail=f"Invalid field select from {valid_fields}"
        )

    valid_order = ["asc", "desc"]
    if order not in valid_order:
        raise HTTPException(
            status_code=400, detail=f"invalid value , select from {valid_order}"
        )

    data = load_data()

    sort_order = True if order == "desc" else False

    sorted_data = sorted(
        data.values(), key=lambda x: x.get(sort_by, 0), reverse=sort_order
    )

    return sorted_data
