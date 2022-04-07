# Websites checker with the Kafka implementation

## Description

Monitoring the given amount of web-sites, produces metrics and pass it through Kafka to the PostgreSQL DB.

Metrics: 

- status code
- response time
- regex pattern match (if needed)

The every site we need to define the period of checking as a cron string.

All this info should to be inserted to the checker.website PostrgreSQL DB table.

**See db/db_init.sql:20**

After the every website will be checked, the app send results to the Kafka queue. 
Then the Kafka consumer will retrieve next message and write it to the checker.check_result PostrgreSQL DB table.

## Setup

### Clone and install dependencies 

```shell
pipenv install
```

### Local setup

Take time and set up the kafka locally as in the following link:

https://kafka.apache.org/quickstart

#### Start the ZooKeeper service

```shell
bin/zookeeper-server-start.sh config/zookeeper.properties
```

#### Start the Kafka broker service

```shell
bin/kafka-server-start.sh config/server.properties
```

#### Create "checker" topic

```shell
bin/kafka-topics.sh --create --topic quickstart-events --bootstrap-server localhost:9092
```

#### Start PostgreSQL locally

```shell
docker-compose up -d db
```

#### Make .env file

```text
POSTGRES_HOST=localhost
POSTGRES_USER=admin
POSTGRES_PASSWORD=admin
POSTGRES_DB=postgres
POSTGRES_SCHEMA=checker

KAFKA_HOST=localhost
KAFKA_PORT=9092
KAFKA_CHECKER_TOPIC=webchecker
```

### Remote setup

### Usage 

#### Run the app

```shell
python app.py
```

## Project structure

```
site_checker
|   
|   db_init.sql: SQL-script for DB initialization 
|___db
|   
|   app.py: The main module to run the loop
|   config.py: Define variables that shared across all app
|   db.py: Database sigleton for sharing one DB connection
|   db_service.py: Low-lewel DB operations
|   docker-compose.yml: Just for PostgreSQL local DB config
|   kafka_service.py: Simple Kafka procuders and cosumers services
|   pytest.ini: Some pytest configs
|   scheduler.py: APScheduler helpers
|   schemas.py: pydantic schemas for the data validation
|   url_checker.py: Site checker itself
```


## Contributing 

All comments, PR's and issues are welcome!
Feel free to make fork and improve the solution. 

## Links

https://www.digitalocean.com/community/tutorials/how-to-install-apache-kafka-on-ubuntu-20-04
https://medium.com/@Ankitthakur/apache-kafka-installation-on-mac-using-homebrew-a367cdefd273
https://habr.com/ru/post/587592/
https://nicholasgribanov.name/apache-kafka-bystryj-start-na-macos/
https://kafka.apache.org/quickstart
https://timber.io/blog/hello-world-in-kafka-using-python/
https://medium.com/@django.course/7-ways-to-execute-scheduled-jobs-with-python-47d481d22b91
https://github.com/agronholm/apscheduler
https://www.psycopg.org/docs/
https://pydantic-docs.helpmanual.io/#using-pydantic
https://pypi.org/project/pytest-postgresql/
https://crontab.guru/#*_*_*_*_*
https://apscheduler.readthedocs.io/en/3.x/modules/triggers/cron.html
https://kaspars.net/blog/regex-extract-headings-h1-h2-h3-from-html
https://regex101.com/
https://requests-mock.readthedocs.io/en/latest/mocker.html
https://dev.to/bowmanjd/two-methods-for-testing-https-api-calls-with-python-and-pytest-and-also-communicating-with-the-in-laws-388n
https://github.com/getsentry/responses
https://github.com/csernazs/pytest-httpserver/blob/master/doc/index.rst
https://github.com/getsentry/responses#responses-as-a-pytest-fixture
https://pydantic-docs.helpmanual.io/usage/schema/#typingannotated-fields
https://peps.python.org/pep-0593/
https://stackabuse.com/the-singleton-design-pattern-in-python/
https://softwareengineering.stackexchange.com/questions/200522/how-to-deal-with-database-connections-in-a-python-library-module
https://12factor.net/
https://webdevblog.ru/realizaciya-shablona-singleton-v-python/
https://doubles.readthedocs.io/en/latest/usage.html
https://pypi.org/project/pytest-mock/
https://github.com/dwyl/learn-postgresql/issues/60
