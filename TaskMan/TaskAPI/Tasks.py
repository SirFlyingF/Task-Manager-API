'''
TODO
implement filtering
'''


from TaskMan.utils import get_resp_struct
from flask import jsonify

from ..Database.models import Task
from ..Database.database import database

session = database.session

class TaskAPI:
    endpoints = ['GetAllTasks', 'GetTask', 'AddTask', 'ModifyTask', 'DeleteTask']
    
    def __init__(self, request, uzr_ctx):
        self.request = request
        self.uzr_ctx = uzr_ctx


    def _validate_request(self, endpoint):
        match endpoint:
            case 'GetAllTasks':
                # There is not body or params.
                # Nothing to validate
                return True, "", 200
            
            case 'GetTask':
                # There is no body. Nothing to validate
                return True, "", 200
            
            case 'AddTask':
                json = self.request.json
                if 'task' not in json:
                    return False, "Invalid Request", 400
                if 'title' not in json['task']:
                    return False, "Invalid Request", 400
                return True, "", 200
            
            case 'ModifyTask':
                json = self.request.json
                if 'task' not in json:
                    return False, "Invalid Request", 400
                return True, "", 200
            
            case 'DeleteTask':
                # Nothign to validate
                return True, "", 200
        return False

    

    def get_all_tasks(self):
        endpoint = 'GetAllTasks'

        q = session.query(Task).filter(Task.active_ind==True)
        if self.uzr_ctx['position'] == 'USER':
            q = q.filter(Task.user.has(id=self.uzr_ctx['user_id']))
        
        # PAginate using query params
        page = 1 if 'page' not in self.request.args else self.request.args.get('page')
        page_size = 20 if 'page_size' not in self.request.args else self.request.args.get('page_size')
        tasks = q.offset((int(page) - 1) * int(page_size)).limit(int(page_size)).all()

        response = get_resp_struct()
        response['data'] = []
        if not tasks:
            return jsonify(get_resp_struct(msg='Resource Not Found')), 404
        
        for task in tasks:
            response['data'].append(task._serial())
        return jsonify(response), 200




    def get_task(self, id):
        endpoint = 'GetTask'
        try:
            q = session.query(Task).filter(
                                        Task.id==id,
                                        Task.active_ind==True,
                                    )
            if self.uzr_ctx['position'] == 'USER':
                q = q.filter(Task.user.has(id=self.uzr_ctx['user_id']))
            
            task = q.first()
            response = get_resp_struct()
            if not task:
                return jsonify(get_resp_struct(msg='Resource Not Found')), 404
            
            response['data'] = task._serial()
        except Exception as e:
            return jsonify(get_resp_struct(msg='Internal Server Error')), 500
        
        return jsonify(response), 200
    


    def add_task(self):
        endpoint = 'AddTask'
        valid, msg, http_code = self._validate_request(endpoint)
        if not valid:
            return jsonify(get_resp_struct(msg=msg)), http_code
        '''
        request = {
            task: {
                title,
                description,
            }
        }
        '''
        json = (self.request.json)['task']
        try:
            task = Task()
            task.title = json['title']
            task.user_id = self.uzr_ctx['user_id']
            task.completed = None if 'completed' not in json else json['completed']
            task.description = None if 'description' not in json else json['description']

            session.add(task)
            session.commit()
        except Exception:
            session.rollback()
            return jsonify(get_resp_struct(msg='Internal Server Error')), 500
        return jsonify(get_resp_struct(data={'id':task.id})), 200 
    
    def modify_task(self, id):
        endpoint = 'ModifyTask'
        valid, msg, http_code = self._validate_request(endpoint)
        if not valid:
            return jsonify(get_resp_struct(msg=msg)), http_code
        '''
        request = {
            task = {
                description,
                completed 
            }
        }
        '''
        json = (self.request.json)['task']
        try:
            q = session.query(Task).filter(Task.id==id)
            if self.uzr_ctx['position'] == 'USER':
                print(self.uzr_ctx)
                q = q.filter(Task.user.has(id=self.uzr_ctx['user_id']))
            
            print(q.statement.compile(compile_kwargs={"literal_binds": True}))
            task = q.first()
            if not task:
                return jsonify(get_resp_struct(msg='Resource Not Found')), 404
            
            if 'description' in json:
                task.description = json['description']
            if 'completed' in json:
                task.completed = json['completed']

            session.commit()               
        except Exception as e:
            session.rollback()
            return jsonify(get_resp_struct(msg='Internal Server Error')), 500
        return jsonify(get_resp_struct(msg='Successful')), 200
    



    def delete_task(self, id):
        endpoint = 'DeleteTask'
        valid, msg, http_code = self._validate_request(endpoint)
        if not valid:
            return jsonify(get_resp_struct(msg=msg)), http_code

        try:
            q = session.query(Task).filter(Task.id==id, Task.active_ind==True)
            if self.uzr_ctx['position'] == 'USER':
                q = q.filter(Task.user.has(id=self.uzr_ctx['user_id']))
            task = q.first()

            if not task:
                return jsonify(get_resp_struct(msg='Resource Not Found')), 404

            # Reset active_ind for soft delete
            task.active_ind = False
            session.commit()               
        except Exception as e:
            session.rollback()
            return jsonify(get_resp_struct(msg='Internal Server Error')), 500
        return jsonify(get_resp_struct(msg='Success')), 200