import pytest
import requests


BASE_URL = "http://127.0.0.1:5000"
tasks = []


def test_create_task():
    global tasks
    task_data = {
        "title": "Test Task",
        "description": "This is a test task."
    }

    response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    reponse_json = response.json()

    assert response.status_code == 201
    assert reponse_json['message'] == 'Task created successfully!'
    assert 'id' in reponse_json

    tasks.append(task_data)  # Add the created task to the tasks list
