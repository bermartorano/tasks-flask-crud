import pytest
import requests


BASE_URL = "http://127.0.0.1:5000"
tasks_ids = []


def test_create_task():
    global tasks_ids
    task_data = {
        "title": "Test Task",
        "description": "This is a test task."
    }

    response = requests.post(f"{BASE_URL}/tasks", json=task_data)
    response_json = response.json()

    assert response.status_code == 201
    assert response_json['message'] == 'Task created successfully!'
    assert 'id' in response_json

    tasks_ids.append(response_json['id'])


def test_get_tasks():
    response = requests.get(f"{BASE_URL}/tasks")
    response_json = response.json()

    assert response.status_code == 200
    assert 'tasks' in response_json
    assert 'tasks_count' in response_json
    assert isinstance(response_json['tasks'], list)
    assert isinstance(response_json['tasks_count'], int)
    assert response_json['tasks_count'] == len(response_json['tasks'])


def test_get_task():
    global tasks_ids
    if not tasks_ids:
        pytest.skip("No tasks available to test.")

    task_id = tasks_ids[0]
    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    response_json = response.json()

    assert response.status_code == 200
    assert 'id' in response_json
    assert 'title' in response_json
    assert 'description' in response_json
    assert 'completed' in response_json
    assert response_json['id'] == task_id


def test_update_task():
    global tasks_ids
    if not tasks_ids:
        pytest.skip("No tasks available to test.")

    task_id = tasks_ids[0]
    updated_data = {
        "title": "Updated Task",
        "description": "This is an updated test task.",
        "completed": True
    }

    response = requests.put(f"{BASE_URL}/tasks/{task_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json() == 'Task updated successfully!'

    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    response_json = response.json()
    assert response_json['title'] == updated_data['title']
    assert response_json['description'] == updated_data['description']
    assert response_json['completed'] == updated_data['completed']


def test_delete_task():
    global tasks_ids
    if not tasks_ids:
        pytest.skip("No tasks available to test.")

    task_id = tasks_ids[0]
    response = requests.delete(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 200
    assert response.json() == 'Task deleted successfully!'

    response = requests.get(f"{BASE_URL}/tasks/{task_id}")
    assert response.status_code == 404
