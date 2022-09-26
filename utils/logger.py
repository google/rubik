import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(name)s | %(levelname)s | %(message)s')


def logger(class_name=""):
    logger = logging.getLogger('rubik:'+class_name)
    return logger
    