import click
import json
import sys
import io

from postman_cli_transformer.decipherer import line_decipherer
from postman_cli_transformer.parsers import parse_test
from postman_cli_transformer.parsers import parse_url
from postman_cli_transformer.unicode_constants import *


@click.command()
@click.argument("output", type=click.File("w"), default="-", required=False)
@click.option(
    "-uf",
    "--unicode-out-file",
    required=False,
    type=click.File("w"),
    help="""file location to output unicode codes of characters from STDIN.
              Each charachter is represented as (<original character> - <unicode of character>)
              Line breaks(10) are preserved but not given a representation""",
)
@click.version_option()
def cli(output, unicode_out_file):
    """This script will take as input the STDOUT from
    a Postman CLI collection run and transform the
    output text to a file containing the output data
    organized in a JSON format. This JSON data is then
    written into a specific file.

    \b
    Output to stdout:
        postman-cli-transformer

    \b
    Output to file foo.json:
        postman-cli-transformer foo.json

    """

    stdin_data = sys.stdin.read()

    parsed_stdin = parse(stdin_data)

    click.echo("Starting.........")
    click.echo(parsed_stdin)

    my_results = []

    for line in io.StringIO(stdin_data):
        my_results.append(line_decipherer(line))

    print(my_results)

    if unicode_out_file:
        process_as_unicode(io.StringIO(stdin_data), unicode_out_file)

    for line in io.StringIO(stdin_data):
        output.write(line)
    output.flush()


def process_as_unicode(file, output):
    for line in file:
        for char in line:
            unicodeInt = ord(char)
            if unicodeInt != 10:
                output.write(" (%c - %s) " % (char, unicodeInt))
            else:
                output.write(char)

    output.flush()


def parse(data):
    parsed = {"collectionName": "", "folders": []}

    data_as_file = io.StringIO(data)
    data_as_file.readline()  # postman
    # Empty line
    data_as_file.readline()

    collection_line = data_as_file.readline()
    collection_name = collection_line.strip()
    parsed["collectionName"] = collection_name

    # Empty line
    data_as_file.readline()

    # Start First Folder
    folder_line = data_as_file.readline()
    folder_name = folder_line.lstrip(BOX_ICON).strip()
    parsed["folders"].append({"name": folder_name, "requests": []})
    current_folder = parsed["folders"][0]

    # Start First Request
    request_line = data_as_file.readline()
    request_name = request_line.lstrip(ENTER_ICON).strip()
    data_as_file.readline()

    url_line = data_as_file.readline()
    url_result = parse_url(url_line, request_name)

    current_folder["requests"].append(url_result)
    current_request = current_folder["requests"][0]

    # Start First Test of First Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # Start Second Test of First Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # Start Third Test of First Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # Empty line
    data_as_file.readline()

    # Start Second Request
    request_line = data_as_file.readline()
    request_name = request_line.lstrip(ENTER_ICON).strip()
    data_as_file.readline()

    url_line = data_as_file.readline()
    url_result = parse_url(url_line, request_name)

    current_folder["requests"].append(url_result)
    current_request = current_folder["requests"][1]

    # Start First Test of Second Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # Start Second Test of Second Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # Start Third Test of Second Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # Empty line
    data_as_file.readline()

    # Start Third Request
    request_line = data_as_file.readline()
    request_name = request_line.lstrip(ENTER_ICON).strip()
    data_as_file.readline()

    url_line = data_as_file.readline()
    url_result = parse_url(url_line, request_name)

    current_folder["requests"].append(url_result)
    current_request = current_folder["requests"][2]

    # Start First Test of Third Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # Start Second Test of Third Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # Start Third Test of Third Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # Start Fourth Test of Third Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # Start Fifth Test of Third Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # Empty line
    data_as_file.readline()

    # Start Second Folder
    folder_line = data_as_file.readline()
    folder_name = folder_line.lstrip(BOX_ICON).strip()
    parsed["folders"].append({"name": folder_name, "requests": []})
    current_folder = parsed["folders"][1]

    # Start First Request of Second Folder
    request_line = data_as_file.readline()
    request_name = request_line.lstrip(ENTER_ICON).strip()
    data_as_file.readline()

    url_line = data_as_file.readline()
    url_result = parse_url(url_line, request_name)

    current_folder["requests"].append(url_result)
    current_request = current_folder["requests"][0]

    # Start First Test of First Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # Start Second Test of First Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # Start Third Test of First Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # Start Fourth Test of First Request
    test_line = data_as_file.readline()
    test_result = parse_test(test_line)
    current_request["tests"].append(test_result)

    # if line.startswith(ENTER_ICON):

    #     parsed["line%s" % line_number] = {}
    #     parsed["line%s" % line_number]["contents"] = line.strip()
    #     line_number += 1
    #     line = data_as_file.readline()

    # for line in data_as_file:
    #     if line.startswith("\n"):
    #         line_number += 1
    #         break

    #     if line.startswith("\u001b"):
    #         parsed["line%s" % line_number] = {}
    #         parsed["line%s" % line_number]["contents"] = (line
    #                                                       .replace("\u001b","")
    #                                                       .replace("\u2500","")
    #                                                       .replace("[90m","")
    #                                                       .replace("[39m","")
    #                                                       .replace("\u2502","")
    #                                                       .replace("\u253c","")
    #                                                       .replace("\u2524","")
    #                                                       .replace("\u2534","")
    #                                                       .replace("\u2514","")
    #                                                       .replace("\u2518","")
    #                                                       .replace("\u251c","")
    #                                                       .strip())
    #     line_number += 1

    json_str = json.dumps(parsed)

    return json_str
