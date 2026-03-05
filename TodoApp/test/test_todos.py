from ..routers.todos import get_db, get_current_user
from ..database import Base
from ..main import app
from .. models import Todos
from .utils import *
from fastapi import status

app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user

def test_read_all_authenticated(test_todo):
    # include the fixture so that a todo exists in the test database
    response = client.get('/')
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'complete': False,
        'title': 'Test Todo!',
        'description': 'This is a test todo',
        'id': 1,
        'priority': 1,
        'owner_id': 1
    }]

def test_read_one_authenticated(test_todo):
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {'complete': False, 'title': 'Test Todo!',
                                'description': 'This is a test todo', 'id': 1,
                               'priority': 1, 'owner_id': 1}

def test_read_one_authenticated_not_found():
    response = client.get("/todo/999")
    assert response.status_code == 404
    assert response.json() == {'detail': 'Todo not found.'}


def test_create_todo(test_todo):
    request_data={
        'title': 'New Todo',
        'description': 'This is a description',
        'priority': 5,
        'complete': False
    }
    response = client.post("/todo/add_data", json=request_data)
    assert response.status_code == status.HTTP_201_CREATED
    db=TestingSessionLocal()
    todo_in_db = db.query(Todos).filter(Todos.title == 'New Todo').first()
    assert todo_in_db.description == request_data.get('description')
    assert todo_in_db.priority == request_data.get('priority')
    assert todo_in_db.complete == request_data.get('complete')
    assert todo_in_db.owner_id == 1

def test_update_todo(test_todo):
    request_data={
        'title': 'Updated Todo',
        'description': 'This is an updated description',
        'priority': 3,
        'complete': True
    }
    response = client.put("/todo/update?todo_id=1", json=request_data)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db=TestingSessionLocal()
    todo_in_db = db.query(Todos).filter(Todos.id == 1).first()
    assert todo_in_db.title == request_data.get('title')
    assert todo_in_db.description == request_data.get('description')
    assert todo_in_db.priority == request_data.get('priority')
    assert todo_in_db.complete == request_data.get('complete')

def test_update_todo_not_found(test_todo):
    request_data={
        'title': 'Updated Todo',
        'description': 'This is an updated description',
        'priority': 3,
        'complete': True
    }
    response = client.put("/todo/update?todo_id=999", json=request_data)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}
   

def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db=TestingSessionLocal()
    todo_in_db = db.query(Todos).filter(Todos.id == 1).first()
    assert todo_in_db is None

def test_delete_todo_not_found(test_todo):
    response = client.delete("/todo/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}