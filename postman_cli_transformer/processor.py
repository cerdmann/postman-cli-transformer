from postman_cli_transformer.decipherer import line_decipherer
from postman_cli_transformer.parsers import parse_folder
from postman_cli_transformer.parsers import parse_request
from postman_cli_transformer.parsers import parse_url
from postman_cli_transformer.parsers import parse_test
from postman_cli_transformer.decipherer import LINE_TYPES


class Processor:
    def __init__(self, lines_to_process):
        """Initialize the class with a document already
        converted into an array of the lines in the doc.
        This initializer will parse lines and build out
        the json representation of the input. This will
        be stored in the parsed field. Retrieve the
        results with:
            processor = Processor(lines)
            results = processor.parsed
        """

        # Class property definiing
        self.processing_helper = ProcessingHelper()
        self.parsed = {"collectionName": "", "folders": []}
        self.lines_to_process = lines_to_process

        # Get header info out of the way
        self._process_first_rows()
        self._process_rest_of_lines()

    def _process_first_rows(self):
        # First line is 'postman' followed by empty line
        self.lines_to_process.pop(0)
        self.lines_to_process.pop(0)
        # Next line is the collection name followed by enpty line
        self.parsed["collectionName"] = self.lines_to_process[0].strip()
        self.lines_to_process.pop(0)
        # Next line is empty, so skip
        self.lines_to_process.pop(0)
        self.processing_helper.previous_line_type = LINE_TYPES.EMPTY_LINE

    def _process_rest_of_lines(self):
        for line in self.lines_to_process:
            match line_decipherer(line):
                case LINE_TYPES.EMPTY_LINE:
                    self.processing_helper.update_current_line_type(
                        LINE_TYPES.EMPTY_LINE
                    )
                case LINE_TYPES.FOLDER_LINE:
                    self.processing_helper.update_current_line_type(
                        LINE_TYPES.FOLDER_LINE
                    )
                    folder_json = parse_folder(line)
                    self.parsed["folders"].append(folder_json)
                    self.processing_helper.current_folder += 1
                    self.processing_helper.current_request = -1
                case LINE_TYPES.ROOT_REQUEST_LINE:
                    self.processing_helper.update_current_line_type(
                        LINE_TYPES.ROOT_REQUEST_LINE
                    )
                    if self.processing_helper.root_request_folder == -1:
                        folder_json = parse_folder("❏ <REQUESTS_WITHOUT_FOLDER>")
                        self.parsed["folders"].append(folder_json)
                        self.processing_helper.current_folder += 1
                        self.processing_helper.root_request_folder = (
                            self.processing_helper.current_folder
                        )
                        self.processing_helper.current_request = -1

                    request_json = parse_request(line)
                    self.parsed["folders"][self.processing_helper.root_request_folder][
                        "requests"
                    ].append(request_json)
                    self.processing_helper.current_request += 1
                case LINE_TYPES.REQUEST_LINE:
                    self.processing_helper.update_current_line_type(
                        LINE_TYPES.REQUEST_LINE
                    )
                    request_json = parse_request(line)
                    self.parsed["folders"][self.processing_helper.current_folder][
                        "requests"
                    ].append(request_json)
                    self.processing_helper.current_request += 1
                case LINE_TYPES.URL_LINE:
                    self.processing_helper.update_current_line_type(LINE_TYPES.URL_LINE)
                    url_json = parse_url(line)
                    self.parsed["folders"][self.processing_helper.current_folder][
                        "requests"
                    ][self.processing_helper.current_request]["urls"].append(url_json)
                case LINE_TYPES.TEST_LINE:
                    self.processing_helper.update_current_line_type(
                        LINE_TYPES.TEST_LINE
                    )
                    test_json = parse_test(line)
                    self.parsed["folders"][self.processing_helper.current_folder][
                        "requests"
                    ][self.processing_helper.current_request]["tests"].append(test_json)


class ProcessingHelper:
    previous_line_type = ""
    current_line_type = ""
    current_folder = -1
    current_request = -1
    root_request_folder = -1

    def update_current_line_type(self, new_line_type):
        self.previous_line_type = self.current_line_type
        self.current_line_type = new_line_type
