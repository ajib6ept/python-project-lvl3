import click
import requests

from page_loader.cli import arg_parse
from page_loader.engine import download
from page_loader.exceptions import (BadStatusCodeException,
                                    StorageErrorException)


def main():
    exception_happened = True
    try:
        args = arg_parse(standalone_mode=False)
        url, output = args[0], args[1]
        download(*args)
    except click.exceptions.BadParameter as e:
        print(f"Bad parameter parametr: {e}")
    except requests.exceptions.ConnectTimeout:
        print(f"The request timed out while trying to connect to {url}")
    except BadStatusCodeException:
        print("{url} return error HTTP status code")
    except StorageErrorException:
        print(f"Error creating a directory {output}")
    except Exception:
        print(f"An error occurred while trying to download {url}")
    else:
        exception_happened = False
    finally:
        if exception_happened:
            exit(1)
