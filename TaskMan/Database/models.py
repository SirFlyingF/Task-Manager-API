from sqlalchemy import Column, String, Integer, Boolean, DateTime, Text, ForeignKey
from sqlalchemy.schema import  UniqueConstraint
from sqlalchemy.orm import  relationship
from .database import database
from datetime import datetime

'''

'''
Base = database.Base

class Task(Base):
    '''
    # Class to store Tasks
    '''
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    title = Column(String(256), nullable=False)
    description = Column(Text) 
    completed = Column(Boolean, nullable=False, default=True) 
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow) 
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow) 
    active_ind = Column(Boolean, nullable=False, default=True)

    user = relationship('user', foreign_keys='Task.user_id')

    def __init__(self, data):
        super().__init__()
        self.user_id = data['user_id']
        self.title = data['title']
        self.description = data['description']
        self.completed = data['completed']
        
    def _serial(self):
        dict = {
            'task_id' : self.id,
            'title' : self.title,
            'description' : self.description, 
            'completed' : self.completed,
            'created_at' : self.created_at,
            'updated_at' : self.updated_at,
            'active_ind' : self.active_ind
        }
        return dict


class Token(Base):
    '''
    # Class to store 'logged out' tokens
    '''
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    token = Column(String(128), nullable=False)
    login_ind = Column(Boolean, nullable=False) #indicate if expired
    
class User(Base):
    '''
    # Will Use Username for public_id.
    '''
    __tablename__ = 'user'
    __tableargs__ = (
        UniqueConstraint('email', name='uk_email')
    )
    id = Column(Integer, primary_key=True)
    name_first = Column(String(64), nullable=False)
    name_last = Column(String(64), nullable=True)
    # May implement name keys for searching, and name middle
    position = Column(String(8), default='USER') # Role based IAM [User, Admin]
    email = Column(String(128), nullable=False)
    pw_hash = Column(String(128), nullable=False) # SHA512

    def __init__(self):
        super().__init__()

    def _serial(self):
        dict = {
            'user_id' : self.id,
            'name_first' : self.name_first,
            'name_last' : self.name_last,
            'name_first_key' : self.name_first_key,
            'name_last_key' : self.name_last_key,
            'position': self.position,
            'active_ind' : self.active_ind,
            'updated_at' : self.updated_at
        }
        return dict