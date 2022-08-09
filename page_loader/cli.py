import click


@click.command()
@click.help_option("-h", "--help")
@click.version_option(
    "0.1.0", "-V", "--version", help="output the version number"
)
@click.option(
    "-o",
    "--output",
    help='output dir (default: "/tmp")',
    metavar="[dir]",
    type=click.Path(exists=True),
    default="/tmp",
)
@click.option(
    "-l",
    "--loglevel",
    default="INFO",
    help="tool loglevel: DEBUG, INFO or WARN (default: INFO)",
    type=click.Choice(["DEBUG", "INFO", "WARN"], case_sensitive=False),
)
@click.argument("url", metavar="<url>")
def arg_parse(url, output, loglevel):
    return url, output, loglevel
