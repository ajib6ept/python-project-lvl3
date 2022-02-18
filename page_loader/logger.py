import logging


def create_logger(loglevel):
    logging.basicConfig(
        format="%(asctime)s - %(message)s", level=get_loglevel(loglevel)
    )


def get_loglevel(loglevel):
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARN": logging.WARN,
    }
    return log_levels[loglevel]
