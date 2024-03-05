import os
from TaskMan import create_app
import pytest, json


@pytest.fixture(scope="session")
def secure_client(): 
    os.environ['ENVIRON'] ='TEST'    
    flask_app = create_app()

    with flask_app.test_client() as client:
        with flask_app.app_context():
            # Sign in using a test user. Use this for all other tests
            json_dict = {
                            "auth" :
                            {
                                "email" : "kabirsharma2905@gmail.com",
                                "password" : "bunny1234"
                            }
                        }
            response = client.post('/auth/signin', json=json_dict)
            json = response.get_json()
            setattr(client, '__token', json['data']['token'])
            yield client
