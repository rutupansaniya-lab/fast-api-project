from sqlalchemy import StaticPool, create_engine, text
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest
from .. models import Todos,User
from ..routers.auth import bcrypt_context

SQLALCHEMY_DATABASE_URL = "sqlite:///./testdb.db"
engine=create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool)
TestingSessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    # create a new session from the sessionmaker instead of returning the
    # factory itself.  the tests were hitting a `sessionmaker` object in the
    # router which doesn't have `query` or `close` methods.
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# the original function name contained typos; it still worked because
# the override was set explicitly, but it's clearer to spell it correctly.
def override_get_current_user():
    return {'username': 'Rutu', 'id': 1, 'user_role': 'admin'}

client=TestClient(app)


@pytest.fixture
def test_user():
    user = User(
        username="Rutu",
        email="rutu@seaflux.tech",
        first_name="rutu",
        last_name="pansaniya",
        hashed_password=bcrypt_context.hash("testpassword"),
        role="admin",
        phone_number="(111)-111-1111"
    )
    db = TestingSessionLocal()
    db.add(user)
    db.commit()
    yield user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()

@pytest.fixture
def test_todo():
    # create a todo record that tests can rely on
    todo = Todos(title='Test Todo!', description='This is a test todo', priority=1, complete=False, owner_id=1)
    db = TestingSessionLocal()
    db.add(todo)
    db.commit()
    yield todo
    # cleanup after the fixture runs
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos"))
        connection.commit()

