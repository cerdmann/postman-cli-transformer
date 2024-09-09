from postman_cli_transformer.cli import parse 
import json


def test_finished_product():
  #This seems like a lot of conversions to make, but it works
    expected_result = open("tests/test_data/expected-results.txt")
    expected_data = expected_result.read()
    expected_json = json.loads(expected_data)
    expected_json_str = json.dumps(expected_json, sort_keys=True)

    raw_output_from_postman_cli = open("tests/test_data/postman-cli-run.txt")
    raw_data = raw_output_from_postman_cli.read()
    parsed_data = parse(raw_data)
    parsed_json = json.loads(parsed_data)
    parsed_json_str = json.dumps(parsed_json, sort_keys=True)

    assert (parsed_json_str == expected_json_str)