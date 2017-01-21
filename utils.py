import logging

def get_logger(name, log_level=logging.DEBUG):
    logging.basicConfig(format='%(levelname)s: <%(asctime)s> | %(message)s')
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger
