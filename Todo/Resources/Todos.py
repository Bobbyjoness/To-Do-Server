from flask_restful import reqparse, abort, Api, Resource
from Models.todoModel import db, Todos, Timestamp


parser = reqparse.RequestParser()
parser.add_argument('task', location='json')

def abort_if_todo_doesnt_exist(todo_id):
    if not Todos.query.filter_by(todo_id=todo_id).first():
        abort(404, message="Todo {} doesn't exist".format(todo_id))


class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        task = Todos.query.filter_by(todo_id=todo_id).first()

        resultList = []
        resultList.append({"todo_id":task.todo_id,"task":task.task} )

        timestamps = Timestamp.query.all()
        
        if (len(timestamps)>0): 
            resultList.append({"lastUpdated" : timestamps[-1].timestamp.isoformat()})
        else:
            time = Todos_timestamp()
            db.session.add(time)
            db.session.commit()
            timestamps = Timestamp.query.all()
            resultList.append({"lastUpdated" : timestamps[-1].timestamp.isoformat()})

        return resultList, 200


    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        Todos.query.filter_by(todo_id=todo_id).delete()
        time = Timestamp()
        db.session.add(time)
        db.session.commit()
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = Todos.query.filter_by(todo_id=todo_id).first()
        task.task = args['task']
        time = Timestamp()
        db.session.add(time)
        db.session.commit()

        resultList = []
        resultList.append({"todo_id":task.todo_id,"task":task.task} )

        timestamps = Timestamp.query.all()
        
        if (len(timestamps)>0): 
            resultList.append({"lastUpdated" : timestamps[-1].timestamp.isoformat()})
        else:
            time = Todos_timestamp()
            db.session.add(time)
            db.session.commit()
            timestamps = Timestamp.query.all()
            resultList.append({"lastUpdated" : timestamps[-1].timestamp.isoformat()})

        return resultList, 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        resList = Todos.query.all()
        resultList = []
        for res in resList:
            resultList.append({"todo_id":res.todo_id,"task":res.task})

        timestamps = Timestamp.query.all()
        
        if (len(timestamps)>0): 
            resultList.append({"lastUpdated" : timestamps[-1].timestamp.isoformat()})
        else:
            time = Todos_timestamp()
            db.session.add(time)
            db.session.commit()
            timestamps = Timestamp.query.all()
            resultList.append({"lastUpdated" : timestamps[-1].timestamp.isoformat()})


        return resultList,200

    def post(self):
        args = parser.parse_args()
        todo_id = "todo"+str(Todos.query.count()+1)
        t = Todos(todo_id,args['task'])
        db.session.add(t)
        time = Timestamp()
        db.session.add(time)
        db.session.commit()
        task = Todos.query.filter_by(todo_id=todo_id).first()

        resultList = []
        resultList.append({"todo_id":task.todo_id,"task":task.task} )

        timestamps = Timestamp.query.all()
        
        if (len(timestamps)>0): 
            resultList.append({"lastUpdated" : timestamps[-1].timestamp.isoformat()})
        else:
            time = Todos_timestamp()
            db.session.add(time)
            db.session.commit()
            timestamps = Timestamp.query.all()
            resultList.append({"lastUpdated" : timestamps[-1].timestamp.isoformat()})

        return resultList, 201