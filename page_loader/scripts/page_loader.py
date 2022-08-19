import click
import requests

from page_loader.cli import arg_parse
from page_loader.engine import download
from page_loader.exceptions import StorageErrorException
from page_loader.tools import eprint


def main():
    exception_happened = True
    try:
        args = arg_parse(standalone_mode=False)
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
        exception_happened = False
    finally:
        if exception_happened:
            exit(1)
