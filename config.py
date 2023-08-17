import logging
import os

root_logger = logging.getLogger()
LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO').upper()
root_logger.setLevel(level=LOG_LEVEL)

# avoid double-logging by only configuring stdout stream handler when executing outside AWS
# why: https://stackoverflow.com/questions/50909824/getting-logs-twice-in-aws-lambda-function
aws_exec_env = os.environ.get('AWS_EXECUTION_ENV', None)
if not aws_exec_env:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)


def get_stage(environ: dict = os.environ) -> str:
    """
    Get the delivery stage for this deployment, calculated from the `STAGE` environment variable.

    :return the delivery stage, default 'dev'
    """
    stage = environ.get('STAGE')
    if not stage:
        stage = "dev"
    return stage
