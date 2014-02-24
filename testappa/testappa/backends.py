#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from requests import HTTPError

from social.backends.oauth import BaseOAuth2
from social.exceptions import AuthMissingParameter, AuthCanceled

class GluuOidc(BaseOAuth2):
    """Gluu authentication backend"""
    name = 'gluu-oidc'
    REDIRECT_STATE = False
    AUTHORIZATION_URL = 'https://idp.logintex.me/oxauth/seam/resource/restv1/oxauth/authorize'
    ACCESS_TOKEN_URL = 'https://idp.logintex.me/oxauth/seam/resource/restv1/oxauth/token'
    ACCESS_TOKEN_METHOD = 'POST'
    REVOKE_TOKEN_URL = 'https://idp.logintex.me/oxauth/seam/resource/restv1/oxauth/revoke'
    REVOKE_TOKEN_METHOD = 'GET'
    DEFAULT_SCOPE = ['openid',
                     'profile',
                     'email',
                     'teainfo']
    STATE_PARAMETER = False
    EXTRA_DATA = [
        ('refresh_token', 'refresh_token', True),
        ('expires_in', 'expires'),
        ('token_type', 'token_type', True)
    ]
    def get_user_id(self, details, response):
        if self.setting('USE_UNIQUE_USER_ID', False):
            return response['username']
        else:
            return details['email']

    def get_user_details(self, response):
        email = response.get('email', '')
        return { # 'username': email.split('@', 1)[0],
                'email': email,
                'organization': response.get(b'teaOrganizationID', ''),
                'school': response.get(b'teaSchoolID', ''),
                'username': response.get(b'sub', ''),
                'state_id': response.get(b'teaStateUniqueID', ''),
                'sis_id': response.get(b'teaSISid', ''),
                'grade': response.get(b'teaGrade', ''),
                'first_name': response.get(b'given_name', ''),
                'last_name': response.get(b'family_name', ''),
                'common_name': response.get(b'cn', ''),
                'date_of_birth': response.get(b'teaDateOfBirth', ''),
                'role': response.get(b'teaRole', ''),
                'manager': response.get(b'teaAppManager', ''),
                'fullname': response.get('name', ''),}
                # 'first_name': response.get('given_name', ''),
                # 'last_name': response.get('family_name', '')}

    def user_data(self, access_token, *args, **kwargs):
        """Return user data """
        return self.get_json(
            'https://idp.logintex.me/oxauth/seam/resource/restv1/oxauth/userinfo',
            params={'access_token': access_token, 'scope': 'openid teainfo profile'}
        )


    def revoke_token_params(self, token, uid):
        return {'token': token}

    def revoke_token_headers(self, token, uid):
        return {'Content-type': 'application/json'}






