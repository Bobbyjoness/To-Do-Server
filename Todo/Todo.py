from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.ext.sqlalchemy import SQLAlchemy
import json
from Models.todoModel import db
from Resources.Todos  import Todo, TodoList


#app set up
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
api = Api(app)

#DB init
db.app = app
db.init_app(app)
db.create_all()

##Routes 
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')

#Start The Damn Server
if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')