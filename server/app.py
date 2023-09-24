#!/usr/bin/env python3

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    done = db.Column(db.Boolean, default=False)

@app.route('/tasks', methods=['GET', 'POST'])
def tasks():
    if request.method == 'GET':
        tasks = Task.query.all()
        task_list = [{'id': task.id, 'title': task.title, 'description': task.description, 'done': task.done} for task in tasks]
        return jsonify(task_list)
    
    if request.method == 'POST':
        data = request.json
        title = data.get('title')
        description = data.get('description')
        new_task = Task(title=title, description=description)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task created successfully'}), 201

@app.route('/tasks/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def task(id):
    task = Task.query.get_or_404(id)

    if request.method == 'GET':
        return jsonify({'id': task.id, 'title': task.title, 'description': task.description, 'done': task.done})
    
    if request.method == 'PUT':
        data = request.json
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.done = data.get('done', task.done)
        db.session.commit()
        return jsonify({'message': 'Task updated successfully'})
    
    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted successfully'})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
