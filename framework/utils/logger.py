"""Logger (Framework step 13). Messages go to the console and logs/test_run.log."""
import logging


def get_logger(name):
    return logging.getLogger(name)
