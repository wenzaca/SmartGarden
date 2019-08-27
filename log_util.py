import logging
import logging.config

logging.config.fileConfig(fname='logger.ini', disable_existing_loggers=False)
logging.FileHandler('log/SmartGarden.log')


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
