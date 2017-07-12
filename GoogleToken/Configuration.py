# Author:       Scott Philip (sp@scottphilip.com)
# Version:      0.3 (13 July 2017)
# Source:       https://github.com/scottphilip/google-token/
# Licence:      GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007)
import json
from os.path import expanduser, join
from tempfile import gettempdir
from datetime import datetime


class GoogleTokenConfiguration:
    """
    Configuration
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
                 execute_script=None,
                 phantomjs_path="phantomjs",
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
                 oauth2_data=None
                 ):

        self.account_email = account_email
        import os
        if not os.path.isdir(join(gettempdir(), "GoogleToken", self.account_email)):
            os.makedirs(join(gettempdir(), "GoogleToken", self.account_email))
        if self.account_email is None:
            raise Exception("account_email configuration must be set.")
        self.account_password = account_password
        self.account_otp_secret = account_otp_secret
        self.cookie_storage_path = cookie_storage_path if cookie_storage_path is not None \
            else join(expanduser("~"), "{0}.cookies".format(self.account_email))
        self.oauth_client_id = oauth_client_id
        self.oauth_redirect_uri = oauth_redirect_uri
        self.oauth_scope = oauth_scope
        self.logger = logger
        self.image_path = image_path if image_path is not None else join(
            gettempdir(),
            "GoogleToken",
            self.account_email,
            datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        self.execute_script = execute_script
        self.phantomjs_path = phantomjs_path
        self.phantomjs_config_useragent = phantomjs_config_useragent
        self.phantomjs_log_path = phantomjs_log_path if phantomjs_log_path is not None \
            else join(gettempdir(),
                      "GoogleToken",
                      self.account_email, "phantomjs.log")
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
        self.default_headers = {"User-Agent": user_agent} if default_headers is None else default_headers
        self.oauth2_data = {"response_type": "token",
                            "client_id": "oauth_client_id",
                            "redirect_uri": "oauth_redirect_uri",
                            "scope": "oauth_scope"} if oauth2_data is None else oauth2_data

    def json(self):
        result = {}
        for attribute in self.__dict__:
            try:
                json.dumps(getattr(self, attribute))
                result[attribute] = getattr(self, attribute)
            except Exception:
                ignore = True
        return json.dumps(result)
