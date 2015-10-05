from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask.ext.sqlalchemy import SQLAlchemy
import datetime
import json


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
api = Api(app)
db = SQLAlchemy(app)

class Todos(db.Model):
    todo_id = db.Column(db.String(80), unique=True, primary_key=True)
    task = db.Column(db.String(500))


    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task
    
    def __repr__(self):
        return '<Task %r>' % self.todo_id

class Todos_timestamp(db.Model):
    timestamp_id = db.Column(db.Integer, primary_key=True,unique=True)
    timestamp    = db.Column(db.DateTime(timezone=False))

    def __init__(self):
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return self.timestamp



db.create_all()

def abort_if_todo_doesnt_exist(todo_id):
    if not Todos.query.filter_by(todo_id=todo_id).first():
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task', location='json')


# Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        res = Todos.query.filter_by(todo_id=todo_id).first()
        return {"todo_id":res.todo_id,"task":res.task},200

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        Todos.query.filter_by(todo_id=todo_id).delete()
        time = Todos_timestamp()
        db.session.add(time)
        db.session.commit()
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = Todos.query.filter_by(todo_id=todo_id).first()
        task.task = args['task']
        time = Todos_timestamp()
        db.session.add(time)
        db.session.commit()
        return {"todo_id":task.todo_id,"task":task.task}, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        resList = Todos.query.all()
        resultList = []
        for res in resList:
            resultList.append({"todo_id":res.todo_id,"task":res.task})

        timestamps = Todos_timestamp.query.all()

        resultList.append({"lastUpdated" : timestamps[-1].timestamp.isoformat()})
        return resultList,200

    def post(self):
        args = parser.parse_args()
        todo_id = "todo"+str(Todos.query.count()+1)
        t = Todos(todo_id,args['task'])
        db.session.add(t)
        time = Todos_timestamp()
        db.session.add(time)
        db.session.commit()
        res = Todos.query.filter_by(todo_id=todo_id).first()
        return {"todo_id":res.todo_id,"task":res.task},201
##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')