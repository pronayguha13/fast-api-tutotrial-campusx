from fastapi import FastAPI, Path, HTTPException, Query
import json
from fastapi.responses import JSONResponse
from models.patients_model import Patient, PatientUpdate


app = FastAPI()


def load_data():
    with open("Patients.json", "r") as f:
        data = json.load(f)
        return data


def save_data(data):
    with open("Patients.json", "w") as f:
        json.dump(data, f)


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


@app.post("/create-patient")
def create_patient(patient: Patient):
    # load existing data
    data = load_data()
    # check whether the patient already exists
    if patient.id in data:
        raise HTTPException(status_code=400, detail="Patient already exist")
    # new patient added to the DB
    data[patient.id] = patient.model_dump(exclude={"id"})
    # save into the JSON file
    save_data(data)
    # return json response
    return JSONResponse(
        status_code=201, content={"message": "Patients created successfully"}
    )


@app.put("/edit-patient/{patient_id}")
def update_patient(patient_id: str, patient_update: PatientUpdate):
    data = load_data()
    # if patient_id exists or not
    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient does not exist")
    else:
        existing_patient_info = data[patient_id]

        updated_info = patient_update.model_dump(exclude_unset=True)

        for key, value in updated_info.items():
            existing_patient_info[key] = value

        existing_patient_info["id"] = patient_id

        new_patient = Patient(**existing_patient_info)

        data[patient_id] = new_patient.model_dump(exclude={"id"})

        save_data(data)

        return JSONResponse(
            status_code=204, content={"message": "Patient updated successfully"}
        )


@app.delete("/delete/{patient_id}")
def delete_patient(patient_id: str):
    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404, detail="Patient not found")

    del data[patient_id]

    save_data(data=data)

    return JSONResponse(
        status_code=200, content={"message": "Patient Deleted successfully"}
    )
