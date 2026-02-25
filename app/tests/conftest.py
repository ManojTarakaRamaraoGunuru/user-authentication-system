import pytest

from fastapi import testclient

from app.database.db_setup import get_session
from unittest.mock import Mock
from app.main import app

mock_session = Mock()
user_service = Mock()
test_service = Mock()

def get_mock_session():
    yield mock_session

app.dependency_overrides[get_session] = get_mock_session

@pytest.fixture
def fake_session():
    return mock_session

@pytest.fixture
def user_service():
    return user_service

@pytest.fixture
def test_client():
    return test_client(app)