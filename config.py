"""
Store configurations

Import as:
import config
"""
import os
import pathlib

import dotenv

BASE_DIR = pathlib.Path(__file__).parent

CHECKER_ENV_FILE = os.environ.get("CHECKER_ENV_FILE", '.env')
dotenv.load_dotenv(os.path.join(BASE_DIR, CHECKER_ENV_FILE))

POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)
POSTGRES_INIT_SQL_SCRIPT = os.environ.get(
    "POSTGRES_INIT_SQL_SCRIPT", 'db/db_init.sql')

KAFKA_HOST = os.environ.get("KAFKA_HOST")
KAFKA_PORT = os.environ.get("KAFKA_PORT")
KAFKA_CHECKER_TOPIC = os.environ.get("KAFKA_CHECKER_TOPIC")

KAFKA_CREDS = {}

if os.environ.get("KAFKA_SSL_CAFILE"):
    KAFKA_CREDS = {
        "security_protocol": "SSL",
        "ssl_cafile": os.environ.get("KAFKA_SSL_CAFILE"),
        "ssl_certfile": os.environ.get("KAFKA_SSL_CERTFILE"),
        "ssl_keyfile": os.environ.get("KAFKA_SSL_KEYFILE"),
    }
