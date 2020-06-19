import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'vamsichanakya.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'coffeeshop'


'''
AuthError Exception
A standardized way to communicate auth failure modes
'''


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


"""Auth Header"""


def get_token_auth_header():
    """get the header from the request"""
    """raise an AuthError if no header is present"""
    auth_header = request.headers.get('Authorization', None)
    if not auth_header:
        raise AuthError({
            'code': 'auth_header_missing',
            'description': 'Authorization header is required.'
        }, 401)

    auth_parts = auth_header.split()

    """raise an AuthError if the header is malformed"""
    if auth_parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'header_invalid',
            'description': 'Bearer Token not found in Auth Header'
        }, 401)

    elif len(auth_parts) == 1:
        raise AuthError({
            'code': 'header_invalid',
            'description': 'Token not found.'
        }, 401)

    elif len(auth_parts) > 2:
        raise AuthError({
            'code': 'header_invalid',
            'description': 'Authorization header must be bearer token.'
        }, 401)

    token = auth_parts[1]
    return token


'''
    INPUTS :
        permission: string permission 
        payload   : decoded jwt payload
'''


def check_permissions(permission, payload):
    """raise an AuthError if permissions are not included in the payload"""
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'permissions_not_in_payload',
            'description': 'Permissions expected in payload'
        }, 400)
    """raise an AuthError if the requested permission string is not in the payload permissions array"""
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'not_authorized',
            'description': 'Permission not found.'
        }, 401)
    return True


'''
    INPUTS
        token: a json web token (string)
'''


def verify_decode_jwt(token):
    jsonurl = urlopen("https://" + AUTH0_DOMAIN + "/.well-known/jwks.json")
    jw_keys = json.loads(jsonurl.read())
    unverified_hdr = jwt.get_unverified_header(token)
    rsa_key = {}
    for key in jw_keys["keys"]:
        if key["kid"] == unverified_hdr["kid"]:
            rsa_key = {"kty": key["kty"], "kid": key["kid"], "use": key["use"], "n": key["n"], "e": key["e"]}
    if rsa_key:
        try:
            payload = jwt.decode(token, rsa_key, algorithms=ALGORITHMS, audience=API_AUDIENCE,
                                 issuer="https://" + AUTH0_DOMAIN + "/")
            return payload
        except jwt.ExpiredSignatureError:
            raise AuthError({"code": "expired_token",
                             "description": "token is expired"}, 401)
        except jwt.JWTClaimsError:
            raise AuthError({"code": "incorrect_claims",
                             "description":
                                 "incorrect claims,"
                                 "please check the audience and issuer"}, 401)
        except Exception:
            raise AuthError({"code": "header_invalid",
                             "description":
                                 "Unable to parse authentication"
                                 " token."}, 401)

        _request_ctx_stack.top.current_user = payload
    raise AuthError({"code": "invalid_header",
                     "description": "Unable to find appropriate key"}, 401)


'''
    INPUTS
        permission: string permission
    return the decorator which passes the decoded payload to the decorated method
'''


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            """get_token_auth_header method to get the token"""
            token = get_token_auth_header()
            """verify_decode_jwt method to decode the jwt"""
            payload = verify_decode_jwt(token)
            """the check_permissions method validate claims and check the requested permission"""
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
