import os
from TaskMan import create_app
import pytest, json
from TaskMan.Database.models import User, Task, Token
from TaskMan.Database.database import database

session = database.session
os.environ['ENVIRON'] ='TEST'    
flask_app = create_app()

def clear_database():
    session.query(Task).delete()
    session.query(User).delete()
    session.query(Token).delete()

@pytest.fixture(autouse=True)
def secure_client(): 
    with flask_app.test_client() as client:
        with flask_app.app_context():
            clear_database()

            # Sign in using a test user. Use this for all other tests
            json_dict = {
                            "auth" :
                            {
                                "name_first": "Kabir",
                                "email" : "kabirsharma2905@gmail.com",
                                "password" : "bunny1234"
                            }
                        }
            response = client.post('/auth/signup', json=json_dict)
            response = client.post('/auth/signin', json=json_dict)
            json = response.get_json()
            setattr(client, '__token', json['data']['token'])
            yield client
