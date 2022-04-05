"""
Service for writing results of the site check to the Postgres database.

Import as:
import db_writer
"""

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
