# Author:       Scott Philip (sp@scottphilip.com)
# Version:      0.7 (30 July 2017)
# Source:       https://github.com/scottphilip/google-token/
# Licence:      GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007)
from GoogleToken.Generator import GoogleTokenGenerator


def get_google_token(account_email,
                     oauth_client_id,
                     oauth_redirect_uri,
                     oauth_scope,
                     account_password=None,
                     account_otp_secret=None,
                     **kwargs):
    """
    :param account_email: (REQUIRED)
    :param oauth_client_id: (REQUIRED)
    :param oauth_redirect_uri: (REQUIRED)
    :param oauth_scope: (REQUIRED)
    :param account_password: Necessary for first use.
    :param account_otp_secret: Necessary for first use if enabled on account
    :return: generated token
    """

    items = {"account_email": account_email,
             "oauth_client_id": oauth_client_id,
             "oauth_redirect_uri": oauth_redirect_uri,
             "oauth_scope": oauth_scope,
             "account_password": account_password,
             "account_otp_secret": account_otp_secret}
    for key, value in kwargs.items():
        if key not in items:
            items[key] = value

    generator = GoogleTokenGenerator(**items)
    return generator.generate()
