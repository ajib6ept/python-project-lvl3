from page_loader.cli import arg_parse
from page_loader.engine import download


def main():
    args = arg_parse(standalone_mode=False)
    download(*args)
