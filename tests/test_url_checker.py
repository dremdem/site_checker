"""Testing the url checker"""

import responses

import url_checker
import schemas

URL_LIST = [
    {
        "url": "https://www.qweqwe.qwe/qwe?qwe=123",
        "regex_pattern": r"(?<=<h1>).*(?=<\/h1>)",
        "body": "<div><h1>The pattern is found!</h1><h2>awe qwe</h2></div>",
        "status": 200
    },
]


def test_check_url(mocked_responses):
    mocked_responses.add(
        responses.GET, URL_LIST[0]["url"],
        body=URL_LIST[0]["body"],
        # elapsed=20/1000, # TODO(Vlad): responses didn't support it. See at 31.
        status=URL_LIST[0]["status"],
        content_type='text/html; charset=utf-8')
    result = url_checker.check_url(
        URL_LIST[0]["url"],
        URL_LIST[0]["regex_pattern"]
    )

    assert isinstance(result, schemas.CheckResult)
    # TODO(Vlad): Refactor it, have to mock elapsed attribute
    # assert result == schemas.CheckResult(
    #     status_code=URL_LIST[0]["status"],
    #     response_time=20,
    #     regexp_ok=True
    # )
