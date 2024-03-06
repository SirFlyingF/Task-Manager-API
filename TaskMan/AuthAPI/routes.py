''' 
Use routrs to dispatch to TaskAPI class

'''

from flask import request
from .Auth import AuthAPI
from TaskMan.utils import login_required
from .Auth import AuthAPI
from flask import Blueprint

auth = Blueprint('auth', __name__,)

@auth.route('/signup', methods=['POST'])
def SignUp():
    return AuthAPI(request).sign_up()

@auth.route('/signin', methods=['POST'])
def SignIn():
    return AuthAPI(request).sign_in()

@auth.route('/signout', methods=['GET'])
@login_required
def SignOut(uzr_ctx):
    return AuthAPI(request).sign_out(uzr_ctx)




