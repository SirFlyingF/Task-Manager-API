from Tests.testconf import secure_client
from TaskMan.Database.models import User
from TaskMan.Database.database import database

session = database.session

def register_user(client, res_data = None):
    json_dict = res_data if res_data else {
                    "auth" : {
                        "name_first" : "John",
                        "email" : "john@mail.com",
                        "password": "johndoe"
                    }
                }

    response = client.post('/auth/signup', json=json_dict)

    return json_dict, response


def test_register_user(secure_client):
    _, response = register_user(secure_client)
    json = response.get_json()

    assert response.status_code == 200
    assert 'data' in json
    assert 'msg' in json
    assert 'id' in json['data']


def test_sign_in_user(secure_client):
    json_dict, _ = register_user(secure_client)

    response = secure_client.post('/auth/signin', json=json_dict)
    json = response.get_json()

    assert response.status_code == 200
    assert 'data' in json
    assert 'msg' in json
    assert 'token' in json['data']
    assert json['msg'] == ''

def test_sign_out_user(secure_client):
    response = secure_client.get('/auth/signout', headers={'Authorization':f"Bearer {secure_client.__token}"})
    json = response.get_json()

    assert response.status_code == 200
    assert 'data' in json
    assert 'msg' in json
    assert json['msg'] == 'Successful'
    assert json['data'] == None

def test_sign_out_user_when_token_is_not_present(secure_client):
    response = secure_client.get('/auth/signout')
    json = response.get_json()

    assert response.status_code == 403
    assert 'data' in json
    assert 'msg' in json
    assert json['msg'] == 'User not signed in'
    assert json['data'] == None