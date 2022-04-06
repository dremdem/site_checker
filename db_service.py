"""
Services for DB operations.

Import as:
import db_service
"""
from typing import List, Union

import db
import schemas


def write_check_result(
        check_result: Union[schemas.DBCheckResult, dict],
        connection=db.DBConn.get_conn()) -> bool:
    """
    Write check result to the DB.

    :param connection: PostgreSQL connection.
    :param check_result: Schema model with the check result values.
    :return: Success result ot not.
    """
    if isinstance(check_result, dict):
        check_result = schemas.DBCheckResult(**check_result)

    with connection.cursor() as cur:
        cur.execute(check_result.get_insert_query())
    connection.commit()

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
