"""The main site_checker module"""
import argparse
import logging

import db_service
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
    args = parser.parse_args()
    logging.basicConfig(level=args.log_level)
    schedule_all_websites()
    kafka_service.consume_messages(db_service.write_check_result)
