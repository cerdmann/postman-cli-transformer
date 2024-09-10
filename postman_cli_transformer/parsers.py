from postman_cli_transformer.unicode_constants import CHECKMARK_ICON
from postman_cli_transformer.unicode_constants import BOX_ICON
from postman_cli_transformer.unicode_constants import ENTER_ICON


def parse_test(test):
    test_result = test.strip()
    test_desc = ""
    test_status = ""
    if test_result.startswith(CHECKMARK_ICON):
        test_status = {"result": "SUCCESS", "details": ""}
        test_desc = test_result.lstrip(CHECKMARK_ICON).strip()
    else:
        failed_test = test_result.split(".")
        test_status = {"result": "FAILED", "details": failed_test[0]}
        test_desc = failed_test[1].strip()

    return {"desc": test_desc, "status": test_status}


def parse_url(url, request_name):
    url_parts = url.split("[")
    url_data = url_parts[0].strip().split()
    http_verb = url_data[0]
    url = url_data[1]
    response_data = url_parts[1].strip().rstrip("]").split(", ")
    response_code = response_data[0]
    response_size = response_data[1]
    response_time = response_data[2]

    return {
        "name": request_name,
        "url": url,
        "httpVerb": http_verb,
        "response": {
            "code": response_code,
            "size": response_size,
            "time": response_time,
        },
        "tests": [],
    }


def parse_folder(folder):
    folder_name = folder.lstrip(BOX_ICON).strip()
    return {
        "name": folder_name,
        "requests": [],
    }


def parse_request(request):
    return request.lstrip(ENTER_ICON).strip()
