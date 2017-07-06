class GoogleTokenParameters(object):
    """
    Account Parameters
    """
    def __init__(self, **kwargs):
        for key in kwargs.keys():
            if key in hasattr(self, key):
                setattr(self, key, kwargs.get(key))

    account_email = None
    """Google Account Username/Email"""

    account_password = None
    """Google Account Password.  Only required for first login."""

    account_otp_secret = None
    """Google One Time Passcode Secret.  Only required if enabled and for the first login."""

    cookie_storage_path = None
    """
    Path to file containing cookies for given account. 
    Defaults: ~/GoogleToken/<account_email>.cookies
    """

    oauth_client_id = None
    """OAUTH2 Client Id for login destination.  Required."""

    oauth_redirect_uri = None
    """OAUTH2 Redirect URI for login destination.  Required."""

    oauth_scope = "https://www.googleapis.com/auth/userinfo.email " + \
                  "https://www.googleapis.com/auth/userinfo.profile " + \
                  "https://www.google.com/m8/feeds/"
    """OAUTH2 Scope for login destination.  Required."""

    logger = None
    """Logger to help debug"""

    image_path = None
    """Directory to store debugging screen shots."""

    execute_script = None
    """Javascript to run to verify successful login."""


class GoogleTokenConfiguration(object):
    """
    System Configuration
    """
    phantomjs_path = "phantomjs"
    phantomjs_config_useragent = "phantomjs.page.settings.userAgent"
    cookie_directory_path = "~/GoogleToken"
    cookies_ignore_discard = False
    user_agent = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 "
                  "Firefox/25.0")
    default_headers = {"Accept": "application/json, text/plain, */*",
                       "Accept-Language": "en-US",
                       "Accept-Encoding": "gzip",
                       "Connection": "Keep-Alive",
                       "User-Agent": user_agent}
    url_accounts = "https://accounts.google.com"
    url_my_account = "https://myaccount.google.com"
    url_service_login = "{0}/ServiceLogin".format(url_accounts)
    url_accounts_no_form = "{0}/x".format(url_accounts)
    timeout_seconds = 30
    oauth2_protocol = "https"
    oauth2_domain = "accounts.google.com"
    oauth2_path = "/o/oauth2/v2/auth"
    oauth2_data = {"response_type": "token",
                   "client_id": "oauth_client_id",
                   "redirect_uri": "oauth_redirect_uri",
                   "scope": "oauth_scope"}



