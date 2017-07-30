# Author:       Scott Philip (sp@scottphilip.com)
# Version:      0.7 (30 July 2017)
# Source:       https://github.com/scottphilip/google-token/
# Licence:      GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007)

import json
from os.path import expanduser, join, isdir
from os import makedirs
from tempfile import gettempdir
from datetime import datetime


SECURE_VARIABLES = ["account_password", "account_otp_secret"]


class GoogleTokenConfiguration(object):
    account_email = None
    account_password = None
    account_otp_secret = None
    cookie_storage_path = None
    oauth_client_id = None
    oauth_redirect_uri = None
    oauth_scope = None
    logger = None
    image_path = None
    execute_script = None
    phantomjs_path = "phantomjs"
    phantomjs_config_useragent = "phantomjs.page.settings.userAgent"
    phantomjs_log_path = None
    cookies_ignore_discard = False
    cookies_store_plain = False
    url_accounts = "https://accounts.google.com"
    url_my_account = "https://myaccount.google.com"
    url_service_login = "https://accounts.google.com/ServiceLogin"
    url_accounts_no_form = "https://accounts.google.com/x"
    timeout_seconds = 30
    oauth2_protocol = "https"
    oauth2_domain = "accounts.google.com"
    oauth2_path = "/o/oauth2/v2/auth"
    user_agent = "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:25.0) Gecko/20100101 Firefox/25.0"
    default_headers = None
    oauth2_data = None

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
                continue
            raise Exception("Unknown Argument: {0}".format(key))

        argument_missing = []
        if self.account_email is None:
            argument_missing.append("account_email")
        if self.oauth_client_id is None:
            argument_missing.append("oauth_client_id")
        if self.oauth_redirect_uri is None:
            argument_missing.append("oauth_redirect_uri")
        if self.oauth_scope is None:
            argument_missing.append("oauth_scope")
        if len(argument_missing) > 0:
            raise Exception("REQUIRED_ARGUMENT", str(argument_missing))

        if not isdir(join(gettempdir(), "GoogleToken", self.account_email)):
            makedirs(join(gettempdir(), "GoogleToken", self.account_email))

        self.cookie_storage_path = join(expanduser("~"), "{0}.tok".format(self.account_email)) \
            if self.cookie_storage_path is None else self.cookie_storage_path

        self.image_path = join(gettempdir(), "GoogleToken", self.account_email, datetime.now()
                               .strftime("%Y-%m-%d_%H-%M-%S")) if \
            self.image_path is None else self.image_path

        self.phantomjs_log_path = join(gettempdir(), "GoogleToken", self.account_email, "phantomjs.log") if \
            self.phantomjs_log_path is None else self.phantomjs_log_path

        self.default_headers = {"User-Agent": self.user_agent} if self.default_headers is \
                                                                  None else self.default_headers

        self.oauth2_data = {"response_type": "token",
                            "client_id": "oauth_client_id",
                            "redirect_uri": "oauth_redirect_uri",
                            "scope": "oauth_scope"}

    def json(self):
        result = {}
        for attribute in self.__dict__:
            try:
                if attribute not in SECURE_VARIABLES:
                    json.dumps(getattr(self, attribute))
                    result[attribute] = getattr(self, attribute)
                else:
                    result[attribute] = "*"*10
            except Exception:
                ignore = True
        return json.dumps(result)
