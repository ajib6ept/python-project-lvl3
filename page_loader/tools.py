import os
import logging


def mk_dir(dir_path):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)


def save_page(html, path):
    with open(path, "w") as text_file:
        text_file.write(html)


def get_loglevel(loglevel):
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARN": logging.WARN,
    }
    return log_levels[loglevel]
