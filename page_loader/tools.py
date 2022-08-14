import logging
import os
import sys

from page_loader.exceptions import StorageErrorException


def mk_dir(dir_path):
    if not os.path.exists(dir_path):
        parent_path = os.path.abspath(os.path.join(dir_path, os.pardir))
        if os.path.exists(parent_path):
            os.mkdir(dir_path)
            logging.debug(f"Successfully created directory {dir_path}")
        else:
            raise StorageErrorException


def save_page(html, path):
    with open(path, "w") as text_file:
        text_file.write(html)
    logging.debug(f"Successfully saved page in {path}")


def remove_double_from_the_list(items):
    new_item = []
    for item in items:
        if item not in new_item:
            new_item.append(item)
    return new_item


def eprint(*args, **kwargs):
    "print message to stderr"
    print(*args, file=sys.stderr, **kwargs)
