"""Testing DB singleton"""
import pytest
import psycopg2.extensions as psql_ext

import db


@pytest.mark.usefixtures("postgresql_my_with_schema")
def test_get_conn():
    connection = db.DBConn.get_conn()
    assert type(connection) == psql_ext.connection
    another_connection = db.DBConn.get_conn()
    assert connection == another_connection
