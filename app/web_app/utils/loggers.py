import logging

def setup_logger(logger_name, log_file, level=logging.INFO):
    """Set up a basic logger.

    Args:
        logger_name (str): Name of the logger.
        log_file (str): Path to the log file.
        level (int): Logging level (default: logging.INFO).

    Returns:
        logging.Logger: Configured logger.
    """
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.setLevel(level)
    logger.addHandler(file_handler)
    return logger