from flask.ext.sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

class Todos(db.Model):
    todo_id = db.Column(db.String(80), unique=True, primary_key=True)
    task = db.Column(db.String(500))


    def __init__(self, todo_id, task):
        self.todo_id = todo_id
        self.task = task
    
    def __repr__(self):
        return '<Task %r>' % self.todo_id

class Timestamp(db.Model):
    timestamp_id = db.Column(db.Integer, primary_key=True,unique=True)
    timestamp    = db.Column(db.DateTime(timezone=False))

    def __init__(self):
        self.timestamp = datetime.datetime.now()

    def __repr__(self):
        return self.timestamp

    