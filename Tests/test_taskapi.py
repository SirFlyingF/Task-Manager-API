from testconf import secure_client
from TaskMan.Database.models import User
from TaskMan.Database.database import database
session = database.session


def test_add_task(secure_client):
    json_dict = {
                    "task" : {
                        "title" : "test_add_task",
                        "description" : "Do whatever you can 10"
                    }
                }
    print(secure_client.__token)
    response = secure_client.post('/tasks/', json=json_dict, headers={'Authorization':secure_client.__token})
    json = response.get_json()
    assert response.status_code == 200
    assert 'data' in json
    assert 'msg' in json
    assert 'id' in json['data']


def test_get_all_tasks(secure_client):
    response = secure_client.get('/tasks/?page=1&page_size=3', headers={'Authorization':secure_client.__token})
    json = response.get_json()
    assert response.status_code == 200
    assert 'data' in json
    assert isinstance(json['data'], list)
    assert len(json['data']) == 3


def test_get_task(secure_client):
    response = secure_client.get('/tasks/2', headers={'Authorization':secure_client.__token})
    json = response.get_json()
    assert response.status_code == 200
    assert 'data' in json
    assert isinstance(json['data'], list)
    assert len(json['data']) == 1


def test_modify_task(secure_client):
    json_dict = {
                    "task" : {
                        "description" : "Hello yo",
                        "completed" : False
                    }
                }
    response = secure_client.put('/tasks/2', json=json_dict, headers={'Authorization':secure_client.__token})
    json = response.get_json()
    assert response.status_code == 200
    assert 'data' in json
    assert isinstance(json['data'], list)
    assert len(json['data']) == 1



def test_delete_task(secure_client):
    response = secure_client.delete('/tasks/2', headers={'Authorization':secure_client.__token})
    json = response.get_json()
    assert response.status_code == 200
    assert 'data' in json
    assert 'msg' in json
    assert json['msg'] == "Successful"
