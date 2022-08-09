from page_loader.cli import arg_parse
from page_loader.engine import download


def main():
    url, output, loglevel = arg_parse()
    download(url, output, loglevel)
