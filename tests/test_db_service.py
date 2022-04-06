"""Tests for DB writer"""

import db_service


def test_write_check_result(postgresql_my_with_schema, check_result1):
    db_service.write_check_result(check_result1, postgresql_my_with_schema)
    cur = postgresql_my_with_schema.cursor()
    cur.execute("select count(*) from checker.check_result")
    result_count = cur.fetchone()[0]
    assert result_count == 1


def test_read_websites(postgresql_my_with_schema):
    """Test the reading of all websites in the DB"""
    websites_list = db_service.read_websites(postgresql_my_with_schema)
    assert len(websites_list) == 2
