import logging.handlers
import os

import Ops
from Miscellaneous import exe_vers, find_exe

LONG_LINE = 120
TAF_VER = ".".join([str(i) for i in exe_vers(find_exe())])

if not os.path.exists('Logs'):
    os.mkdir('Logs')

log_file = "TafnitClientLog.log"
logging.basicConfig(filename=f'Logs\\{log_file}',
                    level=logging.DEBUG,
                    filemode='w',
                    format='%(asctime)s.%(msecs)03d - %(process)d:[%(levelname)7s]:[%(levelno)s]  %(message)s',
                    datefmt="%d-%m-%Y %H:%M:%S")
# root_looger = logging.getLogger()
# root_looger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(f'Logs\\{log_file}', 'w', 'utf-8')
# handler.setFormatter(
#     logging.Formatter('%(asctime)s.%(msecs)03d - %(process)d:[%(levelname)7s]:[%(levelno)s]  %(message)s'))
# root_looger.addHandler(handler)


def init():
    logging.info("Initializing end user client configuration tool for eTafnit usage")
    logging.info("Updated as of May 2019")
    # logging.info("Tested on InterSystems Cache version 2018.1.2.309.0.18861")
    logging.info(f"Current eTafnit client version installed: {TAF_VER}")


def log_section(msg):
    char = '>'
    line = char * 10
    print_line = f'{line} {msg} {line}'
    print_line_len = len(print_line)
    logging.debug("")
    logging.debug(print_line_len * char)
    logging.debug(print_line)
    logging.debug(print_line_len * char)


def start_title(msg):
    char = '>'
    line = char * 10
    print_line = f'{line} {msg} {line}'
    logging.debug('')
    logging.debug(print_line)
    return len(print_line)


def end_title(num):
    char = '>'
    logging.debug(char * num)
    logging.debug('')


def end_log():
    from math import ceil
    import traceback
    HALF_LINE = ceil(LONG_LINE / 2)
    logging.info(f'\n{LONG_LINE * "_"}\n{HALF_LINE * ".-"}')
    if not Ops.operations:
        logging.info(f"The client is ready.")
        logging.info("Done.")
        return False

    # Errors found
    err_len = 0
    logging.info(">" * LONG_LINE)
    logging.info(f"THE CLIENT IS NOT READY FOR ETAFNIT")
    errors = []
    for i, e in enumerate(Ops.operations):
        line = f">> {i + 1}) {str(Ops.operations[i])} "
        errors.append(line)
        if err_len < len(line):
            err_len = len(line)

    err_len += 2
    logging.info(">" * err_len)
    for err in errors:
        times = err_len - len(err) - 2
        logging.info(f"{err}{times * ' '}>>")
    logging.info(">" * err_len)
    return True


def error_file():
    try:
        os.remove("Logs\\TafnitErrors.log")
    except FileNotFoundError:
        pass
    if Ops.operations:
        f = open("Logs\\TafnitErrors.log", "w", encoding='utf8')
        f.write('Error File\n')
        err_len = 0  # longest error line
        errors = []  # errors list
        for i, e in enumerate(Ops.operations):
            line = f'>> {i + 1}) {str(Ops.operations[i])} '
            errors.append(line)
            if err_len < len(line):
                err_len = len(line)
        if err_len == 0:
            f.write('No errors were found.\nA bug or a feature?')
            return
        err_len += 2
        f.write(f"{'>' * err_len}\n")
        for err in errors:
            times = err_len - len(err) - 2
            f.write(f'{err}{times * " "}>>\n')
        f.write(f"{'>' * err_len}\n")
        f.close()
    return


if __name__ == '__main__':
    pass
