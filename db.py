"""Serving DB connection"""
import psycopg2

import config


class DBConn:
    """Singleton implementation for sharing DB connection"""

    __conn__ = None

    @classmethod
    def get_conn(cls):
        if not cls.__conn__:
            try:
                print('connecting to PostgreSQL database...')
                conn = DBConn.__conn__ = psycopg2.connect(
                    host=config.POSTGRES_HOST,
                    database=config.POSTGRES_DB,
                    user=config.POSTGRES_USER,
                    password=config.POSTGRES_PASSWORD
                )
                cursor = conn.cursor()
                cursor.execute('SELECT VERSION()')
                db_version = cursor.fetchone()
            except Exception as error:
                print('Error: connection not established {}'.format(error))
                DBConn.__conn__ = None
            else:
                print('connection established\n{}'.format(db_version[0]))
        return cls.__conn__
