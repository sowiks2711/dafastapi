from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)


def test_hello_world():
    response = client.get('/')
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World during the coronavirus pandemic!"}


@pytest.mark.parametrize(
    "name",
    ["Ala", "Zażółć gęślą jaźń", "Grzegorz Brzęczyszczykiewicz"]
)
def test_hello_name(name):
    response = client.get(f'/hello/{name}')
    assert response.status_code == 200
    assert response.json() == {"message": f"Hello {name}!"}