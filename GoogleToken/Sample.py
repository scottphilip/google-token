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
