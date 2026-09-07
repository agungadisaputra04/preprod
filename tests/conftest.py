import os
import pytest
from fastapi.testclient import TestClient
from main import app
from database import get_connection
from main import get_connection_factory


TEST_DB_CONFIG = {
    "host": os.getenv("TEST_DB_HOST", "localhost"),
    "port": int(os.getenv("TEST_DB_PORT", "5432")),
    "dbname": os.getenv("TEST_DB_NAME", "api_lab_test"),
    "user": os.getenv("TEST_DB_USER", "api_lab_app"),
    "password": os.getenv("TEST_DB_PASSWORD"),
}


def get_test_connection():
    import psycopg
    return psycopg.connect(**TEST_DB_CONFIG)


@pytest.fixture
def client():
    app.dependency_overrides[get_connection_factory] = lambda: get_test_connection

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()
