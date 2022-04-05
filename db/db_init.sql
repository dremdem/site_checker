-- DROP schema IF EXISTS checker cascade;
create schema checker;
CREATE TABLE checker.website (
name varchar(50),
url varchar(2000) NOT NULL,
cron_period varchar(20) NOT NULL,
regexp_pattern varchar(20),
CONSTRAINT pk_website PRIMARY KEY(name)
);
CREATE TABLE checker.check_result (
id bigserial primary key,
website_name varchar(50) NOT NULL,
response_time integer NOT NULL,
status_code varchar(20) NOT NULL,
regex_ok bool,
CONSTRAINT fk_website
  FOREIGN KEY(website_name)
  REFERENCES checker.website(name)
);
INSERT INTO
    checker.website (name, url, cron_period, regexp_pattern)
VALUES
    ('aiven_homepage','https://aiven.io/', '* * * * *', null),
    ('aiven_price','https://aiven.io/pricing', '*/2 * * * *', 'right Aiven plan');
