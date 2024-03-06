from Tests.testconf import secure_client
from TaskMan.Database.models import User, Task
from TaskMan.Database.database import database

session = database.session

def create_task(client, res_data = None):
    json_dict = res_data if res_data else {
                    "task" : {
                        "title" : "test_add_task",
                        "description" : "Do whatever you can 10"
                    }
                }

    response = client.post('/tasks/', json=json_dict, headers={'Authorization':f"Bearer {client.__token}"})

    return json_dict, response


def test_add_task(secure_client):
    _, response = create_task(secure_client)
    json = response.get_json()
    assert response.status_code == 200
    assert 'data' in json
    assert 'msg' in json
    assert 'id' in json['data']


def test_add_task_when_required_field_is_missing(secure_client):
    json_dict = {
                    "task" : {
                        "description" : "Do whatever you can 10"
                    }
                }
    _, response = create_task(secure_client, json_dict)
    json = response.get_json()

    assert response.status_code == 400
    assert 'data' in json
    assert 'msg' in json
    assert json['msg'] == 'Invalid Request'


def test_get_all_tasks(secure_client):
    create_task(secure_client)
    response = secure_client.get('/tasks/', headers={'Authorization':f"Bearer {secure_client.__token}"})
    json = response.get_json()

    assert response.status_code == 200
    assert 'data' in json
    assert isinstance(json['data'], list)
    assert len(json['data']) == 1

def test_get_all_tasks_when_no_task_is_present(secure_client):
    response = secure_client.get('/tasks/', headers={'Authorization':f"Bearer {secure_client.__token}"})
    json = response.get_json()

    assert response.status_code == 404
    assert json['data'] == None
    assert json['msg'] == 'Resource Not Found'

def test_get_all_tasks_when_pagination_is_applied(secure_client):
    for i in range(10):
        create_task(secure_client)

    response = secure_client.get('/tasks/?page=1&page_size=5', headers={'Authorization':f"Bearer {secure_client.__token}"})
    json = response.get_json()

    assert response.status_code == 200
    assert 'data' in json
    assert isinstance(json['data'], list)
    assert len(json['data']) == 5


def test_get_task(secure_client):
    json_dict, response = create_task(secure_client)
    json = response.get_json()

    response = secure_client.get(f"/tasks/{json['data']['id']}", headers={'Authorization':f"Bearer {secure_client.__token}"})
    json = response.get_json()

    assert response.status_code == 200
    assert 'data' in json
    assert isinstance(json['data'], dict)
    assert json['data']['title'] == json_dict['task']['title']
    assert json['data']['description'] == json_dict['task']['description']

def test_get_task_when_id_does_not_exist(secure_client):
    response = secure_client.get(f"/tasks/6", headers={'Authorization':f"Bearer {secure_client.__token}"})
    json = response.get_json()

    assert response.status_code == 404
    assert json['data'] == None
    assert json['msg'] == 'Resource Not Found'


def test_modify_task(secure_client):
    json_dict, response = create_task(secure_client)
    json = response.get_json()
    task_id = json['data']['id']

    json_dict = {
                    "task" : {
                        "description" : "Hello yo",
                        "completed" : False
                    }
                }
    response = secure_client.put(f"/tasks/{task_id}", json=json_dict, headers={'Authorization':f"Bearer {secure_client.__token}"})
    json = response.get_json()

    task_res = secure_client.get(f"/tasks/{task_id}", headers={'Authorization':f"Bearer {secure_client.__token}"})
    task_json = task_res.get_json()

    assert response.status_code == 200
    assert 'data' in json
    assert json['msg'] == 'Successful'
    assert task_json['data']['description'] == json_dict['task']['description']
    assert task_json['data']['completed'] == json_dict['task']['completed']

def test_modify_task_when_id_does_not_exist(secure_client):
    json_dict = {
                    "task" : {
                        "description" : "Hello yo",
                        "completed" : False
                    }
                }
    response = secure_client.put(f"/tasks/6", json=json_dict, headers={'Authorization':f"Bearer {secure_client.__token}"})
    json = response.get_json()

    assert response.status_code == 404
    assert json['data'] == None
    assert json['msg'] == 'Resource Not Found'

def test_delete_task(secure_client):
    json_dict, response = create_task(secure_client)
    json = response.get_json()
    task_id = json['data']['id']

    response = secure_client.delete(f'/tasks/{task_id}', headers={'Authorization':f"Bearer {secure_client.__token}"})
    json = response.get_json()
    assert response.status_code == 200
    assert 'data' in json
    assert 'msg' in json
    assert json['msg'] == "Success"

def test_delete_task(secure_client):
    response = secure_client.delete(f"/tasks/6", headers={'Authorization':f"Bearer {secure_client.__token}"})
    json = response.get_json()

    assert response.status_code == 404
    assert json['data'] == None
    assert json['msg'] == 'Resource Not Found'
