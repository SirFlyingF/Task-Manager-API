from functools import wraps
from datetime import datetime
from .Database.models import Token
from .Database.database import database
from flask import current_app as app
from flask import request, jsonify
import jwt

def get_resp_struct(data=None, msg=''):
    return {'data':data, 'msg':msg}

def login_required(f):
    # Decorator for login required
    @wraps(f)
    def is_signedin(*args, **kwargs):
        token = str(request.authorization).split(' ')[1] if request.authorization else ''

        tkn = database.session.query(Token).filter(Token.token==token).first()
 
        if not tkn or not tkn.login_ind:
            return jsonify(get_resp_struct(msg='User not signed in')), 403
        
        try:
            ctx = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        except (jwt.exceptions.ExpiredSignatureError,jwt.exceptions.InvalidSignatureError):
            return jsonify(get_resp_struct(msg='User not signed in')), 403
        
        # Handle invalid ctx
        if ctx['position'] not in ["USER", "ADMIN"]:
            return jsonify(get_resp_struct(msg='User Position not in ["USER", "ADMIN"]')), 403
        
        return f(ctx, *args, **kwargs)
    return is_signedin