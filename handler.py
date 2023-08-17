import json
import logging
import os
from textwrap import dedent

import cedarpy

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


logger = logging.getLogger(__name__)


def hello_cedarpy(event: dict, context: dict) -> dict:
    """The hello_cedarpy function just verifies cedarpy can be loaded and executed correctly by formatting a policy"""
    input_policies: str = dedent("""
                permit(
                    principal,
                    action == Action::"edit",
                    resource
                )
                when {
                    resource.owner == principal
                };
            """)
    output_policies = cedarpy.format_policies(input_policies)
    logger.info(f"successfully formatted policies using cedarpy:\n{output_policies}")
    body = {
        "message": "Go hello-photos! cedarpy is at your service!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response


def view_photo(event: dict, context: dict) -> dict:
    pass

