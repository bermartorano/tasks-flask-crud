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


if __name__ == '__main__':
    app.run(debug=True)
