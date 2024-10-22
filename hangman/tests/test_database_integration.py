import pytest
from hangman.db_api import HangmanDB_Integration

@pytest.fixture
def db_integration():
    return HangmanDB_Integration()

@pytest.mark.integration
def test_example_integration(db_integration):
    api = db_integration
    assert api.random().status_code == 200