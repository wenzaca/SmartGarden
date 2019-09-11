import os
import logging
import logging.config

this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(os.path.dirname(this_dir), "conf", "logger.ini")

logging.config.fileConfig(fname=DATA_PATH, disable_existing_loggers=False)
logging.FileHandler('./log/SmartGarden.log')


def log_info(name, log):
    # Get the logger specified in the file
    logger = logging.getLogger(name)
    logger.info(log)


def log_debug(name, log):
    # Get the logger specified in the file
    logger = logging.getLogger(name)
    logger.debug(log)


def log_error(name, log):
    # Get the logger specified in the file
    logger = logging.getLogger(name)
    logger.error(log)
