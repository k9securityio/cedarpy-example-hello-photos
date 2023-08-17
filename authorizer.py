# The authorizer module implements an AWS API Gateway Lambda Authorizer using the Cedar Policy Framework
# Introduction to Lambda Authorizers:
#   https://docs.aws.amazon.com/apigateway/latest/developerguide/apigateway-use-lambda-authorizer.html

import cedarpy


def authorize(event: dict, context: dict) -> dict:
    pass
