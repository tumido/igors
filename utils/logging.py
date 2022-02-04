import logging

FORMAT = "[%(asctime)s] %(message)s"
logging.basicConfig(format=FORMAT)


def get_logger(name: str):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    return logger
