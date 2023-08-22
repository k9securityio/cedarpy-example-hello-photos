import json
import logging
from textwrap import dedent

import cedarpy

from config import get_stage

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
    logger.info(f"successfully formatted policies using cedarpy (stage={get_stage()}):\n{output_policies}")
    body = {
        "message": "Go hello-photos! cedarpy is at your service!",
        "input": event
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }

    return response

