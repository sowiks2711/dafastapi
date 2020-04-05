from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.exceptions import HTTPException
app = FastAPI()


class PatientIdCounter():
    def __init__(self, idCounter):
        self.idCounter = idCounter
        self.patients = dict()


patientIdCounter = PatientIdCounter(idCounter=0)


class HelloNameResp(BaseModel):
    message: str


class MethodResp(BaseModel):
    method: str


class PatientRequest(BaseModel):
    name: str
    surname: str


class PatientResponse(BaseModel):
    id: int
    patient: PatientRequest


@app.get('/')
def hello_world():
    return {"message": "Hello World during the coronavirus pandemic!"}


@app.get('/hello/{name}', response_model=HelloNameResp)
def hello_name(name: str):
    return HelloNameResp(message=f"Hello {name}!")


@app.get('/method', response_model=MethodResp)
def method_get():
    return MethodResp(method="GET")


@app.put('/method', response_model=MethodResp)
def method_put():
    return MethodResp(method="PUT")


@app.post('/method', response_model=MethodResp)
def method_post():
    return MethodResp(method="POST")


@app.delete('/method', response_model=MethodResp)
def method_delete():
    return MethodResp(method="DELETE")


@app.post('/patient', response_model=PatientResponse)
def patient(patient: PatientRequest):
    id = patientIdCounter.idCounter
    patientIdCounter.idCounter += 1
    patientIdCounter.patients.update({id: patient})
    return PatientResponse(id=id, patient=patient)


@app.get('/patient/{id}')
def get_patient(id: int):
    if id not in patientIdCounter.patients:
        raise HTTPException(status_code=404, detail="Item not found")
    return patientIdCounter.patients[id]
