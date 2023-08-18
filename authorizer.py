# The authorizer module implements an AWS API Gateway Lambda Authorizer using the Cedar Policy Framework
# Introduction to Lambda Authorizers:
#   https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html
import json
import logging

import cedarpy

import helpers

logger = logging.getLogger(__name__)


def _log_function_execution_metadata(event: dict, context: dict) -> None:
    helpers.log_function_execution_metadata(logger, event, context)


def authorize(event: dict, context: dict) -> dict:
    logger.info(f'authorizing access for event: {event}')

    _log_function_execution_metadata(event, context)
    req_body = json.loads(event["body"])
    user_id = req_body.get("userId", None)
    photo_id = req_body.get("photoId", None)

    principal = f'User::"{user_id}"'
    action = f'Action::"view"'
    resource = f'Photo::"{photo_id}"'

    request = {
        "principal": principal,
        "action": action,
        "resource": resource,
        "context": {}
    }
    authz_result = cedarpy.is_authorized(request, "", "")
    if cedarpy.Decision.Allow == authz_result.decision:
        response = {
            # build allow
        }
    else:
        response = {
            # deny
        }
    return response
