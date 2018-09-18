import sys
import json


try:
    conf_file = open("conf.json", "r")
    conf = json.load(conf_file)
except FileNotFoundError:
    print_c("Configuration file 'conf.json' not found.", "bad")
    sys.exit()


COMMANDS = {
    # Lables
    "info": (33, "[!] "),
    "que": (34, "[?] "),
    "bad": (31, "[-] "),
    "good": (32, "[+] "),
    "run": (97, "[~] "),
}


def print_c(string, message_type="info", endline=True):
    """print_colored
    """
    print(
        "\033[{}m{}\033[0m{}".format(
            COMMANDS[message_type][0], COMMANDS[message_type][1], string
        ),
        end=("\n" if endline else ""),
    )
