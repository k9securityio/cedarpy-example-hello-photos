# The authorizer module implements an AWS API Gateway Lambda Authorizer using the Cedar Policy Framework
# Introduction to Lambda Authorizers:
#   https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html
import logging
from typing import List

import cedarpy

import helpers

logger = logging.getLogger(__name__)


def _log_function_execution_metadata(event: dict, context: dict) -> None:
    helpers.log_function_execution_metadata(logger, event, context)


def is_authenticated(user_id, authorization_val):
    if 'Bearer open-sesame' == authorization_val:
        return True
    else:
        return False


def authorize(authz_e: dict, context: dict) -> dict:
    _log_function_execution_metadata(authz_e, context)

    if 'REQUEST' == authz_e.get('type', None):
        headers = authz_e.get('headers', {})
        path_params = authz_e.get('pathParameters', {})
    else:
        logger.info(f'authz_e type is not REQUEST')
        return _make_apig_authz_response('unsupported-request-type', 'Deny', '*')

    user_id = path_params.get("userId", None)
    photo_id = path_params.get("photoId", None)

    if user_id is None or photo_id is None:
        logger.info(f'authz_e missing userId or photoId path parameter')
        return _make_apig_authz_response('unknown-principal-or-resource', 'Deny', '*')

    if not is_authenticated(user_id, headers.get('Authorization', None)):
        logger.info(f'could not authenticate caller')
        return _make_apig_authz_response('unauthenticated-principal', 'Deny', '*')

    # ok, we've authenticated the principal.  are they authorized?
    
    principal = f'User::"{user_id}"'
    action = f'Action::"view"'
    resource = f'Photo::"{photo_id}"'

    request = {
        "principal": principal,
        "action": action,
        "resource": resource,
        "context": {}
    }
    logger.info(f"authorizing request: {request}")
    authz_result = cedarpy.is_authorized(request, _get_policies(), _get_entities())
    logger.info(f"authz_result decision: {authz_result.decision.value} metrics: {authz_result.metrics}")

    # Generate Lambda Authorizer response
    # https://docs.aws.amazon.com/apigateway/latest/developerguide/api-gateway-lambda-authorizer-output.html

    effect = "Deny"
    if cedarpy.Decision.Allow == authz_result.decision:
        effect = "Allow"

    response = {
        "principalId": user_id,
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": authz_e.get('methodArn', 'method-resource-missing')
                }
            ]
        }
    }

    return response


def _get_policies() -> str:
    common_policies = """
            permit(
                principal, 
                action == Action::"view", 
                resource
            )
            when {
               resource.account == principal
            };                
            permit(
                principal,
                action == Action::"delete",
                resource
            )
            when {
                context.authenticated == true
                &&
                resource has account && principal == resource.account.owner
            }
            ;

    """.strip()
    return common_policies


def _get_entities() -> List[dict]:
    entities: List[dict] = [
        {
            "uid": {
                "__expr": "User::\"alice\""
            },
            "attrs": {},
            "parents": []
        },
        {
            "uid": {
                "__expr": "User::\"bob\""
            },
            "attrs": {},
            "parents": []
        },
        {
            "uid": {
                "__expr": 'User::"skuenzli"'
            },
            "attrs": {},
            "parents": []
        },
        {
            "uid": {
                "__expr": "Photo::\"bobs-photo-1\""
            },
            "attrs": {
                "account": {"__expr": "User::\"bob\""}
            },
            "parents": []
        },
        {
            "uid": {
                "__expr": 'Photo::"kitt.png"'
            },
            "attrs": {
                "account": {"__expr": 'User::"skuenzli"'}
            },
            "parents": []
        },
        {
            "uid": {
                "__expr": "Action::\"view\""
            },
            "attrs": {},
            "parents": []
        },
        {
            "uid": {
                "__expr": "Action::\"edit\""
            },
            "attrs": {},
            "parents": []
        },
        {
            "uid": {
                "__expr": "Action::\"delete\""
            },
            "attrs": {},
            "parents": []
        }
    ]
    return entities


def _make_apig_authz_response(principal_id: str, effect: str, resource: str) -> dict:
    return {
            "principalId": principal_id,
            "policyDocument": {
                "Version": "2012-10-17",
                "Statement": [
                    {
                        "Action": "execute-api:Invoke",
                        "Effect": effect,
                        "Resource": resource
                    }
                ]
            }
        }
