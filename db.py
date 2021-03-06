"""Serving DB connection"""
import logging

import psycopg2
import psycopg2.extensions as psql_ext

import config

logger = logging.getLogger(__name__)


class DBConn:
    """Singleton implementation for sharing DB connection"""

    __conn__ = None

    @classmethod
    def get_conn(cls) -> psql_ext.connection:
        """
        Class method for obtaining Postgres connection
        from anywhere in the application.

        :return: Postgres connection.
        """
        if not cls.__conn__:
            try:
                logger.info('connecting to PostgreSQL database...')
                conn = DBConn.__conn__ = psycopg2.connect(
                    host=config.POSTGRES_HOST,
                    port=config.POSTGRES_PORT,
                    database=config.POSTGRES_DB,
                    user=config.POSTGRES_USER,
                    password=config.POSTGRES_PASSWORD
                )
                cursor = conn.cursor()
                cursor.execute('SELECT VERSION()')
                db_version = cursor.fetchone()
            except Exception as error:
                logger.error('Error: connection not established {}'.format(error))
                DBConn.__conn__ = None
            else:
                logger.info('connection established\n{}'.format(db_version[0]))
        return cls.__conn__
