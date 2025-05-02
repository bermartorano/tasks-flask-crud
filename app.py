from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_control = 1


@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    task = Task(
        id=task_id_control,
        title=data.get('title'),
        description=data.get('description'),
    )
    tasks.append(task)
    task_id_control += 1
    return jsonify('Task created successfully!'), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    output = {
        "tasks": task_list,
        "tasks_count": len(task_list)
    }
    return jsonify(output), 200


@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((task for task in tasks if task.id == task_id), None)
    if task:
        return jsonify(task.to_dict()), 200
    else:
        return jsonify('Task not found!'), 404


@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    task = next((task for task in tasks if task.id == task_id), None)
    if task:
        task.title = data.get('title', task.title)
        task.description = data.get('description', task.description)
        task.completed = data.get('completed', task.completed)
        return jsonify('Task updated successfully!'), 200
    else:
        return jsonify('Task not found!'), 404


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((task for task in tasks if task.id == task_id), None)
    if task:
        tasks = [task for task in tasks if task.id != task_id]
        return jsonify('Task deleted successfully!'), 200
    else:
        return jsonify('Task not found!'), 404


if __name__ == '__main__':
    app.run(debug=True)
