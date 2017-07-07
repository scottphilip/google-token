


class GoogleTokenParameters(object):
    """
    Account Parameters
    """

    def __init__(self,
                 account_email=None,
                 account_password=None,
                 account_otp_secret=None,
                 cookie_storage_path=None,
                 oauth_client_id=None,
                 oauth_redirect_uri=None,
                 oauth_scope=None,
                 logger=None,
                 image_path=None,
                 execute_script=None):
        """
        :param account_email: Google Account Username/Email.
        :param account_password: Google Account Password.  Required only for first login
        :param account_otp_secret: Google One Time Passcode Secret.  Only required if
                                   enabled and for the first login
        :param cookie_storage_path: Path to file containing cookies for given account
        :param oauth_client_id: OAUTH2 Client Id for login destination
        :param oauth_redirect_uri: OAUTH2 Redirect URI for login destination
        :param oauth_scope: OAUTH2 Scope for login destination
        :param logger: Logger
        :param image_path: Debugging screen shot directory
        :param execute_script: Execute javascript to verify login success
        """
        self.account_email = account_email
        self.account_password = account_password
        self.account_otp_secret = account_otp_secret
        self.cookie_storage_path = cookie_storage_path
        self.oauth_client_id = oauth_client_id
        self.oauth_redirect_uri = oauth_redirect_uri
        self.oauth_scope = oauth_scope
        self.execute_script = execute_script


class GoogleTokenConfiguration(object):
    """
    System Configuration Settings
    """

    def __init__(self, phantomjs_path="phantomjs",
                 phantomjs_config_useragent="phantomjs.page.settings.userAgent",
                 phantomjs_log_path=None,
                 cookies_ignore_discard=False,
                 url_accounts="https://accounts.google.com",
                 url_my_account="https://myaccount.google.com",
                 url_service_login="https://accounts.google.com/ServiceLogin",
                 url_accounts_no_form="https://accounts.google.com/x",
                 timeout_seconds=30,
                 oauth2_protocol="https",
                 oauth2_domain="accounts.google.com",
                 oauth2_path="/o/oauth2/v2/auth",
                 user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0",
                 default_headers=None,
                 oauth2_data=None,
                 logger=None,
                 image_path=None):
        self.phantomjs_path = phantomjs_path
        self.phantomjs_config_useragent = phantomjs_config_useragent
        if phantomjs_log_path is None:
            import os
            self.phantomjs_log_path = os.path.join(os.path.expanduser("~"), "phantomjs.log")
        else:
            self.phantomjs_log_path = phantomjs_log_path
        self.cookies_ignore_discard = cookies_ignore_discard
        self.url_accounts = url_accounts
        self.url_my_account = url_my_account
        self.url_service_login = url_service_login
        self.url_accounts_no_form = url_accounts_no_form
        self.timeout_seconds = timeout_seconds
        self.oauth2_protocol = oauth2_protocol
        self.oauth2_domain = oauth2_domain
        self.oauth2_path = oauth2_path
        self.user_agent = user_agent
        self.logger = logger
        self.image_path = image_path
        self.default_headers = {"Accept": "application/json, text/plain, */*",
                                "Accept-Language": "en-US",
                                "Accept-Encoding": "gzip",
                                "Connection": "Keep-Alive",
                                "User-Agent": user_agent} if default_headers is None else default_headers
        self.oauth2_data = {"response_type": "token",
                            "client_id": "oauth_client_id",
                            "redirect_uri": "oauth_redirect_uri",
                            "scope": "oauth_scope"} if oauth2_data is None else oauth2_data
