"""Tests for DB writer"""

import db_writer


def test_write_check_result(postgresql_my_with_schema, check_result1):
    db_writer.write_check_result(postgresql_my_with_schema, check_result1)
    cur = postgresql_my_with_schema.cursor()
    cur.execute("select count(*) from checker.check_result")
    result_count = cur.fetchone()[0]
    assert result_count == 1
