from flask import request
from TaskMan.utils import login_required
from .Tasks import TaskAPI
from flask import Blueprint

tasks = Blueprint('tasks', __name__,)


@tasks.route('/', methods=['GET'])
@login_required
def GetAllTasks(uzr_ctx):
    return TaskAPI(request, uzr_ctx).get_all_tasks()

@tasks.route('/<int:id>', methods=['GET'])
@login_required
def GetTask(uzr_ctx, id=None):
    return TaskAPI(request, uzr_ctx).get_task(id=id)

@tasks.route('/', methods=['POST'])
@login_required
def AddTask(uzr_ctx):
    return TaskAPI(request, uzr_ctx).add_task()

@tasks.route('/<int:id>', methods=['PUT'])
@login_required
def ModifyTask(uzr_ctx, id=None):
    return TaskAPI(request, uzr_ctx).modify_task(id=id)

@tasks.route('/<int:id>', methods=['DELETE'])
@login_required
def DeleteTask(uzr_ctx, id=None):
    return TaskAPI(request, uzr_ctx).delete_task(id=id)
