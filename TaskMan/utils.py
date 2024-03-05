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
    def is_signedin():
        token = request.authorization.split()[1] 

        login_ind = database.session.query(Token).filter(token=token).login_ind
        if not login_ind:
            return jsonify(get_resp_struct(msg='User not signed in')), 403
        
        ctx = jwt.decode(token, app.config['SECRET_KEY'])
        if ctx['expiring'] < datetime.utcnow():
            return jsonify(get_resp_struct(msg='User not signed in')), 403
        
        # Handle invalid ctx
        if ctx['position'] not in ["USER", "ADMIN"]:
            return jsonify(get_resp_struct(msg='User Position not in ["USER", "ADMIN"]'))
        
        return f(ctx)
    return is_signedin