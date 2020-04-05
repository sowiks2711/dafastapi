from fastapi.testclient import TestClient
from main import app
import pytest
import json

client = TestClient(app)


def test_hello_world():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World during the coronavirus pandemic!"}


def test_method_get():
    response = client.get('/method')
    assert response.status_code == 200
    assert response.json() == {"method": "GET"}


def test_method_post():
    response = client.post('/method')
    assert response.status_code == 200
    assert response.json() == {"method": "POST"}


def test_method_put():
    response = client.put('/method')
    assert response.status_code == 200
    assert response.json() == {"method": "PUT"}


def test_method_delete():
    response = client.delete('/method')
    assert response.status_code == 200
    assert response.json() == {"method": "DELETE"}


@pytest.mark.parametrize(
    "name",
    ["Ala", "Zażółć gęślą jaźń", "Grzegorz Brzęczyszczykiewicz"]
)
def test_hello_name(name):
    response = client.get(f'/hello/{name}')
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello {name}!"}


@pytest.mark.parametrize(
    "name,surname,expected",
    [("Ala", "lala", 0), ("Edward", "Zażółć gęślą jaźń", 1),
     ("Grzegorz", "Brzęczyszczykiewicz", 2)]
)
def test_patient(name, surname, expected):
    response = client.post(
        f'/patient',
        json.dumps({"name": name, "surname": surname})
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": expected, "patient": {"name": name, "surname": surname}
    }


@pytest.mark.parametrize(
    "name,surname,id",
    [("Ala", "lala", 0), ("Edward", "Zażółć gęślą jaźń", 1),
     ("Grzegorz", "Brzęczyszczykiewicz", 2)]
)
def test_get_patient_exist(name, surname, id):
    response = client.get(f'/patient/{id}')
    assert response.status_code == 200
    assert response.json() == {"name": name, "surname": surname}


@pytest.mark.parametrize(
    "id",
    [100, 101, -2]
)
def test_get_patient_not_exists(id):
    response = client.get(f'/patient/{id}')
    assert response.status_code == 404
