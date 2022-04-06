"""
Schemas for the data models

Import as:
import schemas
"""
from abc import abstractmethod
import http
from typing import Optional, Pattern, List
from typing_extensions import Annotated

import pydantic


class CheckResult(pydantic.BaseModel):
    """Schema for the check result returned from web-site."""

    response_time: Annotated[
        int,
        pydantic.Field(description="The site response time in milliseconds")
    ]
    status_code: int
    regex_ok: Annotated[
        Optional[bool],
        pydantic.Field(
            description="Result of the regex pattern check if needed to."
        )
    ]

    @pydantic.validator('status_code')
    def http_valid_status_code(cls, value: int): # noqa
        """
        Simple status code validator.

        :param v: Status code to validate.
        :return:  Parsed value of the status code.
        """
        value = http.HTTPStatus(v)
        return value.value


class CheckerBaseModel(pydantic.BaseModel):
    """Base schema with some DB helpers"""

    @property
    @abstractmethod
    def __tablename__(self):
        """
        Mandatory attribute for the children classes
        Should be a string with the table name for the model.
        """
        pass

    def _get_string_values(self) -> List[str]:
        """Return list string field values"""
        return [
            f"'{str(value)}'" if not isinstance(value, type(None)) else "null"
            for value in self.dict().values()
        ]

    def get_insert_query(self) -> str:
        """
        Builds the INSERT query based on the field values.

        :return: String with the Insert query.
        """
        return (
            f"INSERT INTO {self.__tablename__} "
            f"({', '.join(self.dict().keys())}) " 
            f"VALUES ({', '.join(self._get_string_values())})"
        )


class DBWebsite(CheckerBaseModel):
    """Schema for the DB website definition"""

    __tablename__ = "checker.website"

    name: str
    url: pydantic.AnyUrl
    cron_period: Annotated[
        str,
        pydantic.Field(
            description="String representing the cron-like schedule definition."
        )
    ]
    regexp_pattern: Optional[Pattern]


class DBCheckResult(CheckResult, CheckerBaseModel):
    """Schema for the DB check result"""

    __tablename__ = "checker.check_result"

    website_name: str
