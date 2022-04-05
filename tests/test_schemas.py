"""Testing schemas """
import pydantic.error_wrappers as pydantic_errors
import pytest

import schemas

CHECK_RESULT_WRONG_STATUS_CODE = {
    "response_time": 224,
    "status_code": "123",
    "regex_ok": None
}


def test_get_insert_query(check_result1: schemas.DBCheckResult):
    """
    Dumb check an insert statement

    :param check_result1: DBCheckResult fixture for testing.
    """
    assert 'insert' in check_result1.get_insert_query().lower()


def test_http_valid_status_code():
    """Test status_code_validation"""
    with pytest.raises(pydantic_errors.ValidationError):
        schemas.CheckResult(**CHECK_RESULT_WRONG_STATUS_CODE)
