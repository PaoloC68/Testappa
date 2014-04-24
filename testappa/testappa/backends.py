#-*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.conf import settings
from social.backends.oauth import BaseOAuth2
import requests

class GluuOidc(BaseOAuth2):
    """Gluu authentication backend
    It uses OIC discover but if discover fails tries to guess the endpoints
    """
    name = 'gluu-oidc'
    REDIRECT_STATE = False
    BASE_OIC_URL = getattr(settings, 'BASE_OIC_URL', 'https://localhost')
    discover_dict = {}
    try:
        headers = {'content-type': 'application/json'}
        discover = requests.get('{0}/.well-known/openid-configuration'.format(BASE_OIC_URL), headers=headers)
        if discover.status_code == 200:
            discover_dict = discover.json()
    except Exception:
        pass

    AUTHORIZATION_URL = discover_dict.get('authorization_endpoint',
                                          BASE_OIC_URL + '/oxauth/seam/resource/restv1/oxauth/authorize')
    ACCESS_TOKEN_URL = discover_dict.get('token_endpoint',
                                         BASE_OIC_URL + '/oxauth/seam/resource/restv1/oxauth/token')
    USERINFO_URL = discover_dict.get('userinfo_endpoint',
                                      BASE_OIC_URL + '/oxauth/seam/resource/restv1/oxauth/userinfo')
    ACCESS_TOKEN_METHOD = getattr(settings, 'ACCESS_TOKEN_METHOD', 'POST')
    REVOKE_TOKEN_URL = BASE_OIC_URL + '/oxauth/seam/resource/restv1/oxauth/revoke'
    REVOKE_TOKEN_METHOD = getattr(settings, 'REVOKE_TOKEN_METHOD', 'GET')
    if getattr(settings, 'DEFAULT_SCOPE', ''):
        DEFAULT_SCOPE = getattr(settings, 'DEFAULT_SCOPE')
    else:
        DEFAULT_SCOPE = discover_dict.get('scopes_supported', ['openid', 'profile', 'email'])
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
        details = {'email': email}
        for f, c in getattr(settings, 'USER_FIELDS_CLAIMS_MAP', []):
            details.update({f: response.get(str(c), '')})
        return details

    def user_data(self, access_token, *args, **kwargs):
        """Return user data """
        return self.get_json(
            self.USERINFO_URL,
            params={'access_token': access_token, 'scope': ' '.join(self.DEFAULT_SCOPE)}
        )


    def revoke_token_params(self, token, uid):
        return {'token': token}

    def revoke_token_headers(self, token, uid):
        return {'Content-type': 'application/json'}