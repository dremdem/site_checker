"""The main site_checker module"""
import argparse
import importlib
import logging
import os

import db_service
import config
import kafka_service
import scheduler
import schemas
import url_checker

logger = logging.getLogger(__name__)


def process_website(db_website: schemas.DBWebsite):
    """
    Check the site and send results to the Kafka

    :param db_website: DBWebsite to process.
    """
    logger.info(f"Checking: {db_website}...")
    check_result = url_checker.check_url(
        db_website.url,
        regexp_pattern=db_website.regexp_pattern)
    db_check_result = schemas.DBCheckResult(
        **check_result.dict(),
        website_name=db_website.name)
    kafka_service.send_message(db_check_result.dict())
    logger.info(f"{db_website} queued for DB writing.")


def schedule_all_websites():
    """Schedule jobs to process all websites"""
    for website in db_service.read_websites():
        scheduler.add_job(
            process_website,
            kwargs={"db_website": website},
            cron=website.cron_period)
    scheduler.start()
    logger.info("All jobs for checking are scheduled.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Run site checker loop')
    parser.add_argument(
        "-l",
        "--log-level",
        default=logging.INFO,
        type=lambda x: getattr(logging, x),
        help="Configure the logging level.")
    parser.add_argument(
        "-s",
        "--schema_init",
        action='store_true',
        help="Pre-initialize the DB schema by the SQL-script. "
             "Default script located in the db/db_init.sql "
             "The path could be changed in the "
             "POSTGRES_INIT_SQL_SCRIPT env-variable.")
    parser.add_argument(
        "-e",
        "--env_file",
        required=False,
        type=str,
        help="Custom ENV file name. Example: .docker.env")
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level)
    if args.schema_init:
        logger.info("Pre-initialize the DB schema by the SQL-script.")
        db_service.init_schema()
    if args.env_file:
        logger.info(f"Get environment from the custom env-file: "
                    f"{args.env_file}")
        os.environ.setdefault("CHECKER_ENV_FILE", args.env_file)
        importlib.reload(config)

    schedule_all_websites()
    kafka_service.consume_messages(db_service.write_check_result)
