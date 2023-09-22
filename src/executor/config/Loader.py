import os
import configparser


def load(file: str, section: str):
    parser = configparser.ConfigParser()
    parser.read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "{}.ini".format(file)))

    return dict(parser[section].items())
