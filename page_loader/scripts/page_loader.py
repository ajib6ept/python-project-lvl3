import sys

import click
import requests

from page_loader.cli import arg_parse
from page_loader.engine import download
from page_loader.storage import StorageErrorException


def eprint(*args, **kwargs):
    "print message to stderr"
    print(*args, file=sys.stderr, **kwargs)


def main():
    try:
        args = arg_parse(standalone_mode=False)
        if args:  # if not only -h options
            url, output = args[0], args[1]
            download(*args)
    except click.exceptions.BadParameter as e:
        eprint(f"Bad parameter parametr: {e}")
    except requests.exceptions.ConnectTimeout:
        eprint(f"The request timed out while trying to connect to {url}")
    except requests.exceptions.HTTPError:
        eprint("{url} return error HTTP status code")
    except StorageErrorException:
        eprint(f"Error creating a directory {output}")
    else:
        exit(0)  # exit without error code, if the exception did not occur
    exit(1)
