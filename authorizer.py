# The authorizer module implements an AWS API Gateway Lambda Authorizer using the Cedar Policy Framework
# Introduction to Lambda Authorizers:
#   https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html
import logging

import cedarpy

logger = logging.getLogger(__name__)


def authorize(event: dict, context: dict) -> dict:
    logger.info(f'authorizing access for event: {event}')
    return {}
