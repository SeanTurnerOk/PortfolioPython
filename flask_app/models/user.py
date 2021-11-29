from flask_app.config.SQLconnector import MySQLConnection
import re
from flask import flash
class User:
    def __init__(self,data):
        self.id=data['id']
        self.firstName=data['firstName']
        self.lastName=data['lastName']
        self.email=data['email']
        self.password=data['password']
        self.updated_at=data['updated_at']
        self.created_at=data['created_at']
    @classmethod
    def get_all(cls):
        query="SELECT * FROM users"
        results=MySQLConnection.connectToMySQL('python_project').query_db(query)
        users=[]
        for each in results:
            users.append(cls(each))
        return users
    @classmethod
    def getByEmail(cls,email):
        query='SELECT * FROM users WHERE email=%(email)s'
        data=MySQLConnection.connectToMySQL('python_project').query_db(query, email)
        return data[0]
    @classmethod
    def getNameById(cls,id):
        query='SELECT * FROM users WHERE id = %(id)s'
        data=MySQLConnection.connectToMySQL('python_project').query_db(query)
        return data[0]['firstName']+' '+data[0]['lastName']
    @classmethod
    def save(cls, data):
        data['id']=len(cls.get_all())+1
        query="INSERT INTO users (id, firstName, lastName, password, email) VALUES (%(id)s,%(firstName)s,%(lastName)s,%(password)s,%(email)s)"
        return MySQLConnection.connectToMySQL('python_project').query_db(query,data)
    @staticmethod
    def validateUser(user):
        is_valid=True
        if user['password']!= user['passwordconf']:
            flash("Passwords did not match")
            is_valid=False
        if len(user['firstName'])<3:
            flash('First name must be at least three characters.')
            is_valid=False
        if len(user['lastName'])<3:
            flash('Last name must be at least three characters.')
            is_valid=False
        if len(user['email'])<3:
            flash('Email must be at least three characters.')
            is_valid=False
        if len(user['password'])<3:
            flash('Password must be at least three characters.')
            is_valid=False
        if not re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+[.]+[a-zA-Z0-9._-]+$').match(user['email']):
            flash('Invalid email address!')
            is_valid=False
        return is_valid