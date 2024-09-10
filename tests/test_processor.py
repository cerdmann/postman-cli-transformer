from postman_cli_transformer.processor import Processor


def test_should_be_able_to_initialize_and_return_json_with_collection_name():
    lines = []

    lines.append("postman\n")
    lines.append("\n")
    lines.append("Private Pinball Map Collection\n")
    lines.append("\n")
    lines.append("❏ Regions\n")

    processor = Processor(lines)
    results = processor.parsed

    assert results["collectionName"] == "Private Pinball Map Collection"


def test_should_be_able_to_process_folders():
    lines = []

    lines.append("postman\n")
    lines.append("\n")
    lines.append("Private Pinball Map Collection\n")
    lines.append("\n")
    lines.append("❏ Regions\n")
    lines.append("\n")
    lines.append("❏ Machines\n")
    lines.append("\n")
    lines.append("❏ Operators\n")

    processor = Processor(lines)
    results = processor.parsed

    folders_node = results["folders"]
    assert len(folders_node) == 3
    assert folders_node[0]["name"] == "Regions"
    assert folders_node[1]["name"] == "Machines"
    assert folders_node[2]["name"] == "Operators"


def test_should_be_able_to_process_urls():
    lines = []

    lines.append("postman\n")
    lines.append("\n")
    lines.append("Private Pinball Map Collection\n")
    lines.append("\n")
    lines.append("❏ Regions\n")
    lines.append("↳ Get location and machine counts\n")
    lines.append("\n")
    lines.append(
        "  GET https://pinballmap.com//api/v1/regions/location_and_machine_counts.json [200 OK, 1.32kB, 264ms]\n"
    )
    lines.append("\n")
    lines.append("↳ Fetch all regions\n")
    lines.append("\n")
    lines.append(
        "  GET https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 98ms]\n"
    )
    lines.append("\n")
    lines.append("❏ Machines\n")
    lines.append("↳ Fetch all machines\n")
    lines.append("\n")
    lines.append(
        "  GET https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern [200 OK, 65.14kB, 220ms]\n"
    )
    lines.append("\n")

    processor = Processor(lines)
    results = processor.parsed

    folders_node = results["folders"]
    assert len(folders_node) == 2

    first_folder = folders_node[0]
    first_request = first_folder["requests"][0]
    assert first_request["name"] == "Get location and machine counts"
    assert (
        first_request["url"]
        == "https://pinballmap.com//api/v1/regions/location_and_machine_counts.json"
    )
    assert first_request["httpVerb"] == "GET"
    assert first_request["response"]["code"] == "200 OK"
    assert first_request["response"]["size"] == "1.32kB"
    assert first_request["response"]["time"] == "264ms"
    second_request = first_folder["requests"][1]
    assert second_request["name"] == "Fetch all regions"
    assert second_request["url"] == "https://pinballmap.com//api/v1/regions.json"
    assert second_request["httpVerb"] == "GET"
    assert second_request["response"]["code"] == "200 OK"
    assert second_request["response"]["size"] == "29.2kB"
    assert second_request["response"]["time"] == "98ms"

    second_folder = folders_node[1]
    first_request = second_folder["requests"][0]
    assert first_request["name"] == "Fetch all machines"
    assert (
        first_request["url"]
        == "https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern"
    )
    assert first_request["httpVerb"] == "GET"
    assert first_request["response"]["code"] == "200 OK"
    assert first_request["response"]["size"] == "65.14kB"
    assert first_request["response"]["time"] == "220ms"


def test_should_be_able_to_process_tests():
    lines = []

    lines.append("postman\n")
    lines.append("\n")
    lines.append("Private Pinball Map Collection\n")
    lines.append("\n")
    lines.append("❏ Regions\n")
    lines.append("↳ Get location and machine counts\n")
    lines.append("\n")
    lines.append(
        "  GET https://pinballmap.com//api/v1/regions/location_and_machine_counts.json [200 OK, 1.32kB, 264ms]\n"
    )
    lines.append("  ✓  Response status code is 200\n")
    lines.append("  ✓  Response time is less than 500ms\n")
    lines.append(
        "  ✓  Response has the required fields - num_locations and num_lmxes\n"
    )
    lines.append("\n")
    lines.append("↳ Fetch all regions\n")
    lines.append("\n")
    lines.append(
        "  GET https://pinballmap.com//api/v1/regions.json [200 OK, 29.2kB, 98ms]\n"
    )
    lines.append("  ✓  Response status code is 200\n")
    lines.append("  ✓  Response time is within an acceptable range\n")
    lines.append("  1. Region object structure is as expected\n")
    lines.append(
        "  ✓  All required fields in the 'region' object are present and not empty\n"
    )
    lines.append("  ✓  Region object has correct data types for fields\n")
    lines.append("\n")
    lines.append("❏ Machines\n")
    lines.append("↳ Fetch all machines\n")
    lines.append("\n")
    lines.append(
        "  GET https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern [200 OK, 65.14kB, 220ms]\n"
    )
    lines.append("  ✓  Response status code is 200\n")
    lines.append("  ✓  Response time is less than 500ms\n")
    lines.append("  ✓  Response has the required fields\n")
    lines.append("\n")

    processor = Processor(lines)
    results = processor.parsed

    folders_node = results["folders"]
    assert len(folders_node) == 2

    first_folder = folders_node[0]
    first_request = first_folder["requests"][0]
    assert first_request["name"] == "Get location and machine counts"
    assert (
        first_request["url"]
        == "https://pinballmap.com//api/v1/regions/location_and_machine_counts.json"
    )
    assert first_request["httpVerb"] == "GET"
    assert first_request["response"]["code"] == "200 OK"
    assert first_request["response"]["size"] == "1.32kB"
    assert first_request["response"]["time"] == "264ms"
    assert first_request["tests"][0]["desc"] == "Response status code is 200"
    assert first_request["tests"][0]["status"]["result"] == "SUCCESS"
    assert first_request["tests"][0]["status"]["details"] == ""
    assert first_request["tests"][1]["desc"] == "Response time is less than 500ms"
    assert first_request["tests"][1]["status"]["result"] == "SUCCESS"
    assert first_request["tests"][1]["status"]["details"] == ""
    assert (
        first_request["tests"][2]["desc"]
        == "Response has the required fields - num_locations and num_lmxes"
    )
    assert first_request["tests"][2]["status"]["result"] == "SUCCESS"
    assert first_request["tests"][2]["status"]["details"] == ""

    second_request = first_folder["requests"][1]
    assert second_request["name"] == "Fetch all regions"
    assert second_request["url"] == "https://pinballmap.com//api/v1/regions.json"
    assert second_request["httpVerb"] == "GET"
    assert second_request["response"]["code"] == "200 OK"
    assert second_request["response"]["size"] == "29.2kB"
    assert second_request["response"]["time"] == "98ms"
    assert second_request["tests"][0]["desc"] == "Response status code is 200"
    assert second_request["tests"][0]["status"]["result"] == "SUCCESS"
    assert second_request["tests"][0]["status"]["details"] == ""
    assert (
        second_request["tests"][1]["desc"]
        == "Response time is within an acceptable range"
    )
    assert second_request["tests"][1]["status"]["result"] == "SUCCESS"
    assert second_request["tests"][1]["status"]["details"] == ""
    assert (
        second_request["tests"][2]["desc"] == "Region object structure is as expected"
    )
    assert second_request["tests"][2]["status"]["result"] == "FAILED"
    assert second_request["tests"][2]["status"]["details"] == "1"
    assert (
        second_request["tests"][3]["desc"]
        == "All required fields in the 'region' object are present and not empty"
    )
    assert second_request["tests"][3]["status"]["result"] == "SUCCESS"
    assert second_request["tests"][3]["status"]["details"] == ""
    assert (
        second_request["tests"][4]["desc"]
        == "Region object has correct data types for fields"
    )
    assert second_request["tests"][4]["status"]["result"] == "SUCCESS"
    assert second_request["tests"][4]["status"]["details"] == ""

    second_folder = folders_node[1]
    first_request = second_folder["requests"][0]
    assert first_request["name"] == "Fetch all machines"
    assert (
        first_request["url"]
        == "https://pinballmap.com//api/v1/machines.json?region_id=119&manufacturer=Stern"
    )
    assert first_request["httpVerb"] == "GET"
    assert first_request["response"]["code"] == "200 OK"
    assert first_request["response"]["size"] == "65.14kB"
    assert first_request["response"]["time"] == "220ms"
    assert first_request["tests"][0]["desc"] == "Response status code is 200"
    assert first_request["tests"][0]["status"]["result"] == "SUCCESS"
    assert first_request["tests"][0]["status"]["details"] == ""
    assert first_request["tests"][1]["desc"] == "Response time is less than 500ms"
    assert first_request["tests"][1]["status"]["result"] == "SUCCESS"
    assert first_request["tests"][1]["status"]["details"] == ""
    assert first_request["tests"][2]["desc"] == "Response has the required fields"
    assert first_request["tests"][2]["status"]["result"] == "SUCCESS"
    assert first_request["tests"][2]["status"]["details"] == ""
