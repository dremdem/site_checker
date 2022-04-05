"""
Services for DB operations.

Import as:
import db_service
"""
from typing import List

import schemas


def write_check_result(
        connection,
        check_result: schemas.DBCheckResult) -> bool:
    """
    Write check result to the DB.

    :param connection: PostgreSQL connection.
    :param check_result: Schema model with the check result values.
    :return: Success result ot not.
    """
    cur = connection.cursor()
    cur.execute(check_result.get_insert_query())
    return True


def read_websites(connection) -> List[schemas.DBWebsite]:
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
