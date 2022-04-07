"""
Store configurations

Import as:
import config
"""
import os
import pathlib

import dotenv

if os.environ.get("CHECKER_TESTING"):
    dotenv.load_dotenv(
        os.path.join(pathlib.Path(__file__).parent, ".test.env"))
else:
    dotenv.load_dotenv()


POSTGRES_HOST = os.environ.get("POSTGRES_HOST")
POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_PORT = os.environ.get("POSTGRES_PORT", 5432)

KAFKA_HOST = os.environ.get("KAFKA_HOST")
KAFKA_PORT = os.environ.get("KAFKA_PORT")
KAFKA_CHECKER_TOPIC = os.environ.get("KAFKA_CHECKER_TOPIC")
