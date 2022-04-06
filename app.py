"""The main site_checker module"""
import db_service
import kafka_service
import scheduler
import schemas
import url_checker


def process_website(db_website: schemas.DBWebsite):
    """
    Check the site and send results to the Kafka

    :param db_website: DBWebsite to process.
    """
    check_result = url_checker.check_url(
        db_website.url,
        regexp_pattern=db_website.regexp_pattern)
    db_check_result = schemas.DBCheckResult(
        **check_result.dict(),
        website_name=db_website.name)
    kafka_service.send_message(db_check_result.dict())


def schedule_all_websites():
    """Schedule jobs to process all websites"""
    for website in db_service.read_websites():
        scheduler.add_job(
            process_website,
            kwargs={"db_website": website},
            cron=website.cron_period)
    scheduler.start()


if __name__ == "__main__":
    schedule_all_websites()
    kafka_service.consume_messages(db_service.write_check_result)
