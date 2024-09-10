from postman_cli_transformer.processor import Processor

import json


def create_array_from_text(text):
    return text.split("\n")


def test_should_be_able_to_initialize_and_return_json_with_collection_name():
    lines = create_array_from_text("""postman

Pinball Map Collection
""")

    processor = Processor(lines)
    results = processor.parsed

    expected_results = {
        "collectionName": "Pinball Map Collection",
        "folders": [],
    }

    assert json.dumps(results) == json.dumps(expected_results)


def test_should_be_able_to_process_folders2():
    lines = create_array_from_text("""postman

Pinball Map Collection

❏ Regions

❏ Machines

❏ Operators""")

    processor = Processor(lines)
    results = processor.parsed

    expected_results = {
        "collectionName": "Pinball Map Collection",
        "folders": [
            {"name": "Regions", "requests": []},
            {"name": "Machines", "requests": []},
            {"name": "Operators", "requests": []},
        ],
    }

    assert json.dumps(results) == json.dumps(expected_results)


def test_should_be_able_to_process_urls():
    lines = create_array_from_text("""postman

Pinball Map Collection

❏ Regions
↳ Get location and machine counts

  GET https://pinballmap.com//api/v1/regions/location_and_machine_counts.json [200 OK, 1.32kB, 264ms]

↳ Fetch all regions

  GET https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 98ms]
  PATCH https://api.getpostman.com/scim/v2/Users/{{userId}} [401 Unauthorized, 485B, 62ms]

❏ Machines
↳ Fetch all machines

  GET https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern [200 OK, 65.14kB, 220ms]
""")

    processor = Processor(lines)
    results = processor.parsed

    expected_results = {
        "collectionName": "Pinball Map Collection",
        "folders": [
            {
                "name": "Regions",
                "requests": [
                    {
                        "name": "Get location and machine counts",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions/location_and_machine_counts.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "1.32kB",
                                    "time": "264ms",
                                },
                            }
                        ],
                        "tests": [],
                    },
                    {
                        "name": "Fetch all regions",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "29.2kB",
                                    "time": "98ms",
                                },
                            },
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users/{{userId}}",
                                "httpVerb": "PATCH",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "62ms",
                                },
                            },
                        ],
                        "tests": [],
                    },
                ],
            },
            {
                "name": "Machines",
                "requests": [
                    {
                        "name": "Fetch all machines",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "65.14kB",
                                    "time": "220ms",
                                },
                            }
                        ],
                        "tests": [],
                    }
                ],
            },
        ],
    }

    assert json.dumps(results) == json.dumps(expected_results)


def test_should_be_able_to_process_tests():
    lines = create_array_from_text("""postman

Pinball Map Collection

❏ Regions
↳ Get location and machine counts

  GET https://pinballmap.com//api/v1/regions/location_and_machine_counts.json [200 OK, 1.32kB, 264ms]
  ✓  Response status code is 200
  ✓  Response time is less than 500ms
  ✓  Response has the required fields

↳ Fetch all regions

  GET https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 98ms]
  PATCH https://api.getpostman.com/scim/v2/Users/{{userId}} [401 Unauthorized, 485B, 64ms]
  ✓  Response status code is 200
  ✓  Response time is within an acceptable range
  1. Region object structure is as expected
  ✓  All required fields in the 'region' object are present and not empty
  ✓  Region object has correct data types for fields

❏ Machines
↳ Fetch all machines

  GET https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern [200 OK, 65.14kB, 220ms]
  ✓  Response status code is 200
  ✓  Response time is less than 500ms
  ✓  Response has the required fields
  ✓  Response content type is application/json
""")

    processor = Processor(lines)
    results = processor.parsed

    expected_results = {
        "collectionName": "Pinball Map Collection",
        "folders": [
            {
                "name": "Regions",
                "requests": [
                    {
                        "name": "Get location and machine counts",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions/location_and_machine_counts.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "1.32kB",
                                    "time": "264ms",
                                },
                            }
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Response time is less than 500ms",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Response has the required fields",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                        ],
                    },
                    {
                        "name": "Fetch all regions",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "29.2kB",
                                    "time": "98ms",
                                },
                            },
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users/{{userId}}",
                                "httpVerb": "PATCH",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "64ms",
                                },
                            },
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Response time is within an acceptable range",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Region object structure is as expected",
                                "status": {"result": "FAILED", "details": "1"},
                            },
                            {
                                "desc": "All required fields in the 'region' object are present and not empty",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Region object has correct data types for fields",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                        ],
                    },
                ],
            },
            {
                "name": "Machines",
                "requests": [
                    {
                        "name": "Fetch all machines",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "65.14kB",
                                    "time": "220ms",
                                },
                            }
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Response time is less than 500ms",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Response has the required fields",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Response content type is application/json",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                        ],
                    }
                ],
            },
        ],
    }

    assert json.dumps(results) == json.dumps(expected_results)


def test_should_be_able_to_process_root_level_requests():
    lines = create_array_from_text("""postman

Pinball Map Collection

❏ Regions
↳ Get location and machine counts

  GET https://pinballmap.com//api/v1/regions/location_and_machine_counts.json [200 OK, 1.32kB, 264ms]
  ✓  Response status code is 200
  ✓  Response time is less than 500ms
  ✓  Response has the required fields

↳ Fetch all regions

  GET https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 98ms]
  GET https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 98ms]
  ✓  Response status code is 200
  ✓  Response time is within an acceptable range
  1. Region object structure is as expected
  ✓  All required fields in the region object are present and not empty
  ✓  Region object has correct data types for fields

❏ Machines
↳ Fetch all machines

  GET https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern [200 OK, 65.14kB, 220ms]
  ✓  Response status code is 200
  ✓  Response time is less than 500ms
  ✓  Response has the required fields
  ✓  Response content type is application/json

→ Deactivate a user

  GET https://api.getpostman.com/scim/v2/Users?count=10000 [401 Unauthorized, 485B, 261ms]
  PATCH https://api.getpostman.com/scim/v2/Users/{{userId}} [401 Unauthorized, 485B, 64ms]                                   

→ Change a user

  GET https://api.getpostman.com/scim/v2/Users?count=10000 [401 Unauthorized, 485B, 261ms]
  PATCH https://api.getpostman.com/scim/v2/Users/{{userId}} [401 Unauthorized, 485B, 64ms]                                   
""")

    processor = Processor(lines)
    results = processor.parsed
    print(results)

    folders_node = results["folders"]

    expected_results = {
        "collectionName": "Pinball Map Collection",
        "folders": [
            {
                "name": "Regions",
                "requests": [
                    {
                        "name": "Get location and machine counts",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions/location_and_machine_counts.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "1.32kB",
                                    "time": "264ms",
                                },
                            }
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Response time is less than 500ms",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Response has the required fields",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                        ],
                    },
                    {
                        "name": "Fetch all regions",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/regions.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "29.2kB",
                                    "time": "98ms",
                                },
                            },
                            {
                                "url": "https://pinballmap.com//api/v1/regions.json",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "29.2kB",
                                    "time": "98ms",
                                },
                            },
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Response time is within an acceptable range",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Region object structure is as expected",
                                "status": {"result": "FAILED", "details": "1"},
                            },
                            {
                                "desc": "All required fields in the region object are present and not empty",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Region object has correct data types for fields",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                        ],
                    },
                ],
            },
            {
                "name": "Machines",
                "requests": [
                    {
                        "name": "Fetch all machines",
                        "urls": [
                            {
                                "url": "https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "200 OK",
                                    "size": "65.14kB",
                                    "time": "220ms",
                                },
                            }
                        ],
                        "tests": [
                            {
                                "desc": "Response status code is 200",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Response time is less than 500ms",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Response has the required fields",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                            {
                                "desc": "Response content type is application/json",
                                "status": {"result": "SUCCESS", "details": ""},
                            },
                        ],
                    },
                ],
            },
            {
                "name": "<REQUESTS_WITHOUT_FOLDER>",
                "requests": [
                    {
                        "name": "Deactivate a user",
                        "urls": [
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users?count=10000",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "261ms",
                                },
                            },
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users/{{userId}}",
                                "httpVerb": "PATCH",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "64ms",
                                },
                            },
                        ],
                        "tests": [],
                    },
                    {
                        "name": "Change a user",
                        "urls": [
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users?count=10000",
                                "httpVerb": "GET",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "261ms",
                                },
                            },
                            {
                                "url": "https://api.getpostman.com/scim/v2/Users/{{userId}}",
                                "httpVerb": "PATCH",
                                "response": {
                                    "code": "401 Unauthorized",
                                    "size": "485B",
                                    "time": "64ms",
                                },
                            },
                        ],
                        "tests": [],
                    },
                ],
            },
        ],
    }

    assert json.dumps(results) == json.dumps(expected_results)
