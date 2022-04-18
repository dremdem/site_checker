"""
Services for DB operations.

Import as:
import db_service
"""
from typing import List, Union
import os

import psycopg2.extensions as psql_ext

import db
import config
import schemas


def add_website(
        website: Union[schemas.DBWebsite, dict],
        connection: psql_ext.connection = db.DBConn.get_conn()
) -> bool:
    """
    Add website to the DB

    :param website: Schemas model or dict to add.
    :param connection: PostgreSQL connection.
    :return: Success result or not.
    """

    if isinstance(website, dict):
        website = schemas.DBWebsite(**website)

    with connection.cursor() as cur:
        cur.execute(website.get_insert_query())
    connection.commit()

    return True


def write_check_result(
        check_result: Union[schemas.DBCheckResult, dict],
        connection: psql_ext.connection = db.DBConn.get_conn()
) -> bool:
    """
    Write check result to the DB.

    :param check_result: Schema model with the check result values.
    :param connection: PostgreSQL connection.
    :return: Success result or not.
    """
    if isinstance(check_result, dict):
        check_result = schemas.DBCheckResult(**check_result)

    with connection.cursor() as cur:
        cur.execute(check_result.get_insert_query())
    connection.commit()

    return True


def read_websites(
        connection: psql_ext.connection = db.DBConn.get_conn()
) -> List[schemas.DBWebsite]:
    """
    Read all websites from the DB

    :param connection: PostgreSQL connection.
    :return: List of DBWebsite objects.
    """
    cur = connection.cursor()
    cur.execute("select name, url, cron_period, regexp_pattern "
                "from checker.website")
    website_list = []
    for name, url, cron_period, regexp_pattern in cur:
        website_list.append(
            schemas.DBWebsite(
                name=name,
                url=url,
                cron_period=cron_period,
                regexp_pattern=regexp_pattern
            ))
    return website_list


def init_schema(
        connection: psql_ext.connection = db.DBConn.get_conn()
) -> None:
    """
    Initialize the schema by SQL-script

    :param connection: PostgreSQL connection
    """
    with connection.cursor() as cursor:
        cursor.execute(
            open(
                os.path.join(
                    config.BASE_DIR, config.POSTGRES_INIT_SQL_SCRIPT,
                ), "r"
            ).read()
        )
