import click
import json
import sys
import io

from postman_cli_transformer.decipherer import line_decipherer
from postman_cli_transformer.parsers import parse_test
from postman_cli_transformer.parsers import parse_url
from postman_cli_transformer.unicode_constants import *
from postman_cli_transformer.processor import Processor


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
    raw_lines = []
    data_as_file = io.StringIO(data)
    for line in data_as_file:
        raw_lines.append(line)

    processor = Processor(raw_lines)
    results = processor.parsed

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

    json_str = json.dumps(results)

    return json_str
