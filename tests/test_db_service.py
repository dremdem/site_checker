"""Tests for DB writer"""

import db_service


def test_write_check_result(postgresql_my_with_schema, check_result1):
    """Test writing the check result"""
    db_service.write_check_result(check_result1, postgresql_my_with_schema)
    with postgresql_my_with_schema.cursor() as cur:
        cur.execute("select count(*) from checker.check_result")
        result_count = cur.fetchone()[0]
    assert result_count == 1


def test_read_websites(postgresql_my_with_schema):
    """Test the reading of all websites in the DB"""
    websites_list = db_service.read_websites(postgresql_my_with_schema)
    assert len(websites_list) == 2


def test_init_schema(postgresql_my_with_schema):
    """Test initializing DB schema"""
    db_service.init_schema(postgresql_my_with_schema)
    with postgresql_my_with_schema.cursor() as cur:
        cur.execute("select count(*) from checker.website")
        result_count = cur.fetchone()[0]
    assert result_count == 2


def test_add_website(postgresql_my_with_schema, website1):
    """Test to adding the new website to the DB"""
    db_service.write_check_result(website1, postgresql_my_with_schema)
    with postgresql_my_with_schema.cursor() as cur:
        cur.execute(f"select count(*) from checker.website "
                    f"where name='{website1.name}'")
        result_count = cur.fetchone()[0]
    assert result_count == 1
