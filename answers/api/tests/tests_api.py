import pytest
from api.app import app
import json

def test_get_all_books():
    response = app.test_client().get('/api/weather')
    res = json.loads(response.data.decode('utf-8'))
    assert type(res[0]) is list
    assert type(res[1]) is list
    assert response.status_code == 200
    assert type(res) is list

