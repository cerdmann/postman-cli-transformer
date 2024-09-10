from postman_cli_transformer.parsers import parse_test
from postman_cli_transformer.parsers import parse_url
from postman_cli_transformer.parsers import parse_folder
from postman_cli_transformer.parsers import parse_request


def test_successful_test_parsing():
    test_line = "  \u2713  Response status code is 200\n"
    assert parse_test(test_line) == {
        "desc": "Response status code is 200",
        "status": {"result": "SUCCESS", "details": ""},
    }


def test_failed_test_parsing():
    test_line = "  1. Region object structure is as expected\n"
    assert parse_test(test_line) == {
        "desc": "Region object structure is as expected",
        "status": {"result": "FAILED", "details": "1"},
    }


def test_url_parsing():
    url_line = "  GET https://pinballmap.com//api/v1/regions/does_region_exist.json?name=minnesota [200 OK, 1.82kB, 83ms]\n"
    assert parse_url(url_line, "Find if name corresponds to a known region") == {
        "name": "Find if name corresponds to a known region",
        "url": "https://pinballmap.com//api/v1/regions/does_region_exist.json?name=minnesota",
        "httpVerb": "GET",
        "response": {"code": "200 OK", "size": "1.82kB", "time": "83ms"},
        "tests": [],
    }


def test_folder_parsing():
    folder_line = "❏ Repeats / Regions Copy\n"
    assert parse_folder(folder_line) == {
        "name": "Repeats / Regions Copy",
        "requests": [],
    }


def test_request_parsing():
    request_line = "↳ Get location and machine counts\n"
    assert parse_request(request_line) == "Get location and machine counts"
