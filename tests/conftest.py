"""Fixtures for the tests"""

import pytest
from pytest_postgresql import factories
import responses

import schemas


CHECK_RESULT1 = {
    "website_name": "aiven_homepage",
    "response_time": 224,
    "status_code": "200",
    "regex_ok": None
}


CHECK_RESULT2 = {
    "website_name": "aiven_homepage",
    "response_time": 224,
    "status_code": "200",
    "regex_ok": None
}


postgresql_my_with_schema = factories.postgresql(
    'postgresql_proc',
    load=['../db/db_init.sql']
)


@pytest.fixture
def check_result1():
    """Fixture for the one check result"""
    return schemas.DBCheckResult(**CHECK_RESULT1)


@pytest.fixture
def mocked_responses():
    """Initialize mocked response"""
    with responses.RequestsMock() as mock_response:
        yield mock_response
