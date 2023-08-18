import os

from config import get_stage


def log_function_execution_metadata(logger, event, context):
    logger.info(f"function execution context: {context}")
    logger.info(f"function execution stage: {get_stage()}")
    logger.info(f"function environment vars: {os.environ}")
    logger.info(f"event ({type(event)}): {event}")
