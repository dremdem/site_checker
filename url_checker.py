"""Services for check urls"""

from typing import Optional
import re
import requests

import schemas


def check_url(
        url: str,
        regexp_pattern: Optional[str] = None) -> schemas.CheckResult:
    """
    Check Url with the optional pattern.

    Gather:
    - response time
    - status code
    - match regex pattern

    :param url:
    :param regexp_pattern:
    :return: Values in the CheckResult model
    """

    result = requests.get(url)
    regexp_ok = (
        bool(re.search(regexp_pattern, result.text))
        if regexp_pattern else None
    )
    return schemas.CheckResult(
        status_code=result.status_code,
        response_time=result.elapsed.total_seconds()*1000,
        regexp_ok=regexp_ok
    )
