# Author:       Scott Philip (sp@scottphilip.com)
# Version:      0.2 (10 July 2017)
# Source:       https://github.com/scottphilip/google-token/
# Licence:      GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007)

from GoogleToken import GoogleTokenGenerator, GoogleTokenParameters


def create_cookie_file(oauth_client_id,
                       oauth_redirect_uri,
                       oauth_scope,
                       account_email,
                       account_password,
                       account_otp_secret=None,
                       config=None):

    generator = GoogleTokenGenerator(
        GoogleTokenParameters(oauth_client_id=oauth_client_id,
                              oauth_redirect_uri=oauth_redirect_uri,
                              oauth_scope=oauth_scope,
                              account_email=account_email,
                              account_password=account_password,
                              account_otp_secret=account_otp_secret),
        config=config)
    token = generator.generate()
    if token is None:
        raise Exception("LOGIN_FAILED")


def get_access_token(oauth_client_id,
                     oauth_redirect_uri,
                     oauth_scope,
                     account_email,
                       config=None):
    generator = GoogleTokenGenerator(
        GoogleTokenParameters(oauth_client_id=oauth_client_id,
                              oauth_redirect_uri=oauth_redirect_uri,
                              oauth_scope=oauth_scope,
                              account_email=account_email),
        config=config)
    return generator.generate()
