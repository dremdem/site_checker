"""Fixtures for the tests"""

import os

import pytest
from pytest_postgresql import factories
import responses

import config
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

WEBSITE1 = {
    "name": "google",
    "url": "https://www.google.com",
    "cron_period": '*/3 * * * *',
    "regexp_pattern": None
}

postgresql_my_with_schema = factories.postgresql(
    'postgresql_proc',
    load=[os.path.join(config.BASE_DIR, 'db/db_init.sql')]
)


@pytest.fixture
def check_result1():
    """Fixture for the one check result"""
    return schemas.DBCheckResult(**CHECK_RESULT1)


@pytest.fixture
def website1():
    """Fixture for the one website"""
    return schemas.DBWebsite(**WEBSITE1)


@pytest.fixture
def mocked_responses():
    """Initialize mocked response"""
    with responses.RequestsMock() as mock_response:
        yield mock_response
