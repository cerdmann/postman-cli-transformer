from postman_cli_transformer.decipherer import line_decipherer
from postman_cli_transformer.decipherer import FOLDER_LINE


def process_line(line):
    match line_decipherer(line):
        case FOLDER_LINE:
            pass
