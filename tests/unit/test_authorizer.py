import unittest

from authorizer import authorize


class AuthorizerTestCase(unittest.TestCase):

    def test_authorize_denies_invalid_requests(self):
        for critical_member in ['type', 'headers', 'pathParameters']:
            authz_e = self.make_valid_authz_request()
            del authz_e[critical_member]

            response = authorize(authz_e, {})
            self.assertEqual("Deny", response["policyDocument"]["Statement"][0]["Effect"])

    def test_authorizes_a_valid_request_for_authorized_resource(self):
        authz_e = self.make_valid_authz_request()

        response = authorize(authz_e, {})
        self.assertEqual("Allow", response["policyDocument"]["Statement"][0]["Effect"])
        self.assertEqual(authz_e['methodArn'],
                         response["policyDocument"]["Statement"][0]["Resource"])

    # noinspection PyMethodMayBeStatic
    def make_valid_authz_request(self):
        return {
            'type': 'REQUEST',
            'methodArn': 'arn:aws:execute-api:us-east-1:139710491120:vr3d61pcqe/dev-main/GET/users/skuenzli/photos/kitt.png',
            'resource': '/users/{userId}/photos/{photoId}',
            'path': '/users/skuenzli/photos/kitt.png',
            'httpMethod': 'GET',
            'headers': {'Accept': 'image/png',
                        'Authorization': 'Bearer open-sesame-1234',
                        'CloudFront-Forwarded-Proto': 'https',
                        'CloudFront-Is-Desktop-Viewer': 'true',
                        'CloudFront-Is-Mobile-Viewer': 'false',
                        'CloudFront-Is-SmartTV-Viewer': 'false',
                        'CloudFront-Is-Tablet-Viewer': 'false',
                        'CloudFront-Viewer-ASN': '22773', 'CloudFront-Viewer-Country': 'US',
                        'Host': 'vr3d61pcqe.execute-api.us-east-1.amazonaws.com',
                        'User-Agent': 'curl/7.88.1',
                        'Via': '2.0 efdd98c65d70c59c49dba4d718c25274.cloudfront.net (CloudFront)',
                        'X-Amz-Cf-Id': 'ODZuEV6Oj-B_9tP7LZqqawV0bV2KWuALJiCclHnAVyyQjXnF-gAfTA==',
                        'X-Amzn-Trace-Id': 'Root=1-64e0039e-25a58e2f21498a1812ae6839',
                        'X-Forwarded-For': '98.177.1.4, 52.46.35.86',
                        'X-Forwarded-Port': '443', 'X-Forwarded-Proto': 'https'},
            'multiValueHeaders': {
                'Accept': ['image/png'],
                'Authorization': ['Bearer open-sesame'],
                'CloudFront-Forwarded-Proto': ['https'], 'CloudFront-Is-Desktop-Viewer': ['true'],
                'CloudFront-Is-Mobile-Viewer': ['false'],
                'CloudFront-Is-SmartTV-Viewer': ['false'],
                'CloudFront-Is-Tablet-Viewer': ['false'], 'CloudFront-Viewer-ASN': ['22773'],
                'CloudFront-Viewer-Country': ['US'],
                'Host': ['vr3d61pcqe.execute-api.us-east-1.amazonaws.com'],
                'User-Agent': ['curl/7.88.1'],
                'Via': ['2.0 efdd98c65d70c59c49dba4d718c25274.cloudfront.net (CloudFront)'],
                'X-Amz-Cf-Id': ['ODZuEV6Oj-B_9tP7LZqqawV0bV2KWuALJiCclHnAVyyQjXnF-gAfTA=='],
                'X-Amzn-Trace-Id': ['Root=1-64e0039e-25a58e2f21498a1812ae6839'],
                'X-Forwarded-For': ['98.177.1.4, 52.46.35.86'], 'X-Forwarded-Port': ['443'],
                'X-Forwarded-Proto': ['https']},
            'queryStringParameters': {},
            'multiValueQueryStringParameters': {},
            'pathParameters': {'photoId': 'kitt.png', 'userId': 'skuenzli'},
            'stageVariables': {},
            'requestContext': {
                'resourceId': '2g7hdj',
                'resourcePath': '/users/{userId}/photos/{photoId}',
                'httpMethod': 'GET', 'extendedRequestId': 'J4WAxEudIAMFX3Q=',
                'requestTime': '18/Aug/2023:23:49:50 +0000',
                'path': '/dev-main/users/skuenzli/photos/kitt.png', 'accountId': '139710491120',
                'protocol': 'HTTP/1.1', 'stage': 'dev-main', 'domainPrefix': 'vr3d61pcqe',
                'requestTimeEpoch': 1692402590285,
                'requestId': 'e4e9d76f-8d5a-49dd-9083-f5015318c292',
                'identity': {'cognitoIdentityPoolId': None, 'accountId': None,
                             'cognitoIdentityId': None, 'caller': None, 'sourceIp': '98.177.1.4',
                             'principalOrgId': None, 'accessKey': None,
                             'cognitoAuthenticationType': None,
                             'cognitoAuthenticationProvider': None, 'userArn': None,
                             'userAgent': 'curl/7.88.1', 'user': None},
                'domainName': 'vr3d61pcqe.execute-api.us-east-1.amazonaws.com',
                'apiId': 'vr3d61pcqe'
            }
        }
