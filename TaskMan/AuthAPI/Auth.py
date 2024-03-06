from TaskMan.utils import get_resp_struct
from flask import jsonify, request
from ..Database.models import User, Token
from ..Database.database import database
from flask import current_app as app

from werkzeug.security import check_password_hash, generate_password_hash
import jwt
import re
from datetime import datetime, timedelta

session = database.session
email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"

class AuthAPI:
    endpoints = ['SignUp', 'SignIn', 'SignOut']
    
    def __init__(self, request):
        self.request = request


    def _validate_request(self, endpoint):
        match endpoint:
            case 'SignIn':
                json = self.request.json
                if 'auth' not in json:
                    return False, "Invalid Request", 400
                if not {'email', 'password'}.issubset(json['auth'].keys()):
                    return False, "Invalid Request", 400
                return True, "", 200
            
            case 'SignUp':
                json = self.request.json
                if 'auth' not in json:
                    return False, "Invalid Request", 400
                if not {'email', 'password', 'name_first'}.issubset(json['auth'].keys()):
                    return False, "Invalid Request", 400
                if not re.fullmatch(email_regex, json['auth']['email']):
                    return False, "Invalid email", 401
                return True, "", 200
            
            case 'SignOut':
                # login_required decorator handles token validity
                # Nothing to Validate
                return True, "", 200
        return False


    def sign_in(self):
        endpoint = 'SignIn'
        valid, msg, http_code = self._validate_request(endpoint)
        if not valid:
            return jsonify(get_resp_struct(msg=msg)), http_code

        json = self.request.json['auth']

        q = session.query(User)\
                    .filter(
                            User.email==json['email']
                    )
        uzr = q.first()
        if not uzr:
            return jsonify(get_resp_struct(msg='User Not Found')), 404

        try:
            # If username and password is not correct
            pwmatch = check_password_hash(uzr.pw_hash, json['password'])
            if not pwmatch:
                return jsonify(get_resp_struct(msg='Invalid email or password')), 401

            # Generate token
            claimset = {
                        'email' : json['email'],
                        'user_id' : uzr.id,
                        'position' : uzr.position,
                        'exp' : datetime.utcnow()+timedelta(minutes=30),
                        }
            token = jwt.encode(claimset, app.config['SECRET_KEY'], algorithm="HS256")

            # Insert token in Token table
            tkn = Token()
            tkn.user_id = uzr.id
            tkn.token = token
            tkn.login_ind = True
                    
            session.add(tkn)
            session.commit()
        except Exception as e:
            session.rollback()
            return jsonify(get_resp_struct(msg='Internal Server Error')), 500
        else:
            # Return Token
            return jsonify(get_resp_struct(data={'token':token})), 200



    def sign_up(self):
        endpoint = 'SignUp'
        valid, msg, http_code = self._validate_request(endpoint)
        if not valid:
            return jsonify(get_resp_struct(msg=msg)), http_code
        '''
            request={
                auth {
                    name first,
                    name last, [Optional]
                    email,
                    password
                }
            }
        '''
        json = (self.request.json)['auth']
        try:
            duplicate = session.query(User).filter(User.email==json['email']).all()
            if duplicate:
                return jsonify(get_resp_struct(msg='Email already exists')), 409

            uzr = User()
            uzr.name_first = json['name_first']
            uzr.name_last = None if 'name_last' not in json else json['name_last']
            uzr.email = json['email']
            uzr.pw_hash = generate_password_hash(json['password'])
            
            session.add(uzr)
            session.commit()
        except Exception:
            session.rollback()
            return jsonify(get_resp_struct(msg='Internal Server Error')), 500
        return jsonify(get_resp_struct(data={'id':uzr.id},msg='Successful')), 200
    

    def sign_out(self, uzr_ctx):
        endpoint = 'SignOut'
        valid, msg, http_code = self._validate_request(endpoint)
        if not valid:
            return jsonify(get_resp_struct(msg=msg)), http_code

        try:
            token = str(self.request.authorization).split(' ')[1]
            _ = session.query(Token)\
                        .filter(
                            Token.user_id==uzr_ctx['user_id'],
                            Token.token==token,
                        )\
                        .update(
                            {'login_ind' : False},
                            synchronize_session='fetch'
                        )
            session.commit()
        except Exception:
            session.rollback()
            return jsonify(get_resp_struct(msg='Internal Server Error')), 500
        return jsonify(get_resp_struct(msg='Successful')), 200