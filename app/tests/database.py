import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from ..main import app
from .. import models, database
from config import settings

DATABASE_URL = settings.sqlalchemy_database_url
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
                        
# This fixture sets up a clean database for each test.
@pytest.fixture
def session():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine) 
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# This fixture provides a TestClient for making HTTP requests to the FastAPI app during tests.
@pytest.fixture
def client(session): 
    def override_get_db(): 
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[database.get_db] = override_get_db  #replaces the database dependency in the app with the test session.
    yield TestClient(app)