import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database.session import get_db
from app.database.base import Base
from app.auth.jwt_auth import create_access_token

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_db.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")                     # scope="module" it means the fixture which is instantiated here can be shared by every fuction of this module and will be destroyed automatically when test ends. 'function' likhne se each test will get a fresh DB, preventing leak of data between tests.
def db():

    Base.metadata.create_all(bind=engine)           # table create ho jayegi
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    # Dependency override: Use the test DB instead of the production DB
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c

@pytest.fixture
def auth_headers(db):

    from app.models.users import Users

    test_user = Users(
        email="mytest@example.com",
        hashed_password="mytestpassword"
    )
    db.add(test_user)
    db.commit()
    db.refresh(test_user)

    token = create_access_token(
        data={"sub":test_user.email}
    )

    return {
        "Authorization": f"Bearer {token}"
    }


