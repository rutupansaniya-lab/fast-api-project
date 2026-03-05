from .utils import *
from ..routers.admin import get_db as admin_get_db
from ..routers.auth import get_current_user
from starlette import status
from ..main import app

app.dependency_overrides[get_current_user] = override_get_current_user
app.dependency_overrides[admin_get_db] = override_get_db

def test_read_all_todos_admin(test_todo):
    response = client.get('/admin/todo')
    print(response.json())
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [{
        'complete': False,
        'title': 'Test Todo!',
        'description': 'This is a test todo',
        'id': 1,
        'priority': 1,
        'owner_id': 1
    }]


def test_delete_todo_admin(test_todo):
    response = client.delete('/admin/todo/1')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    db=TestingSessionLocal()
    todo_in_db = db.query(Todos).filter(Todos.id == 1).first()
    assert todo_in_db is None

def test_delete_todo_admin_not_found():
    response = client.delete('/admin/todo/999')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {'detail': 'Todo not found.'}

