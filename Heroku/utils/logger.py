import sys
import logging
from logging import Logger, Formatter, StreamHandler

LOG_LEVEL = logging.INFO


def setup_logger(name: str) -> Logger:
    logger: Logger = logging.getLogger(name)

    if not logger.hasHandlers():
        logger.setLevel(LOG_LEVEL)
        logger_format : Formatter = logging.Formatter(
            '[ %(asctime)s - %(name)s ] %(levelname)s: %(message)s'
        )

        stream_handler: StreamHandler = logging.StreamHandler(sys.stdout)
        stream_handler.setFormatter(logger_format)
        # don't keep in buffer, push to terminal asap
        stream_handler.flush = sys.stdout.flush 
        logger.addHandler(stream_handler)
        logger.propagate = False # don't propagate to parent
    else:
        logger = logging.getLogger()
        logger.setLevel(LOG_LEVEL)
        logger_format : Formatter = logging.Formatter(
            '_[ %(asctime)s - %(name)s ] %(levelname)s: %(message)s'
        )
        handler = logger.handlers[0]
        handler.setFormatter(logger_format)
    
    return logger
    