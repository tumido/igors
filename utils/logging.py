import os
import logging

FORMAT = "[%(asctime)s] %(message)s"
logging.basicConfig(format=FORMAT)


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    return logger


def assert_mode(logger: logging.Logger):
    if os.getenv("ENV") == "production":
        logger.info("Running in production mode")
    else:
        logger.info("Running in dev mode")
