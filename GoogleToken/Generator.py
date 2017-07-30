# Author:       Scott Philip (sp@scottphilip.com)
# Version:      0.7 (30 July 2017)
# Source:       https://github.com/scottphilip/google-token/
# Licence:      GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007)

from GoogleToken.Configuration import GoogleTokenConfiguration
from GoogleToken.Utils import *
from os.path import isfile

try:
    from urllib.parse import urlparse, parse_qs
    from urllib.request import build_opener, Request, HTTPCookieProcessor
except ImportError:
    from urlparse import urlparse, parse_qs
    from urllib2 import HTTPCookieProcessor, build_opener, Request


class GoogleTokenGenerator(object):
    """
    Google Token Generator
    """

    def __init__(self, **kwargs):
        self.config = GoogleTokenConfiguration(**kwargs)
        debug(self.config, "SYSTEM_CONFIGURATION", self.config.json())

    def generate(self):
        if not isfile(self.config.cookie_storage_path):
            debug(self.config, "COOKIE_FILE_NOT_FOUND", self.config.cookie_storage_path)
            self.__phantom_login()
        return self.__cookies_login()

    def __phantom_login(self):
        debug(self.config, "PHANTOM_LOGIN_STARTING")
        from GoogleToken.Phantom import GoogleTokenPhantomLogin
        phantom_login = GoogleTokenPhantomLogin(self.config)
        phantom_login.login()
        phantom_login.save_cookies()

    def __cookies_login(self):
        debug(self.config, "COOKIES_LOGIN_STARTING")
        with GoogleTokenHttpHandler(self.config) as http_handler:
            return http_handler.get_access_token()


class GoogleTokenHttpHandler(object):
    """
    Http Handler
    """

    def __init__(self, config):
        self.config = config
        if not isfile(self.config.cookie_storage_path):
            raise Exception("COOKIE_FILE_NOT_FOUND", self.config.cookie_storage_path)
        self.cookie_jar = open_cookie_jar(self.config)
        self.opener = build_opener(GoogleTokenHttpNoRedirect,
                                   HTTPCookieProcessor(self.cookie_jar))
        debug(self.config, "COOKIES_LOADED")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        save_cookie_jar(self.config, self.cookie_jar)
        debug(self.config, "COOKIES_SAVED")



    def get_access_token(self):
        request = Request(get_oauth_url(self.config),
                          headers=self.config.default_headers)
        debug(self.config, "SENDING_REQUEST")
        response = self.opener.open(request)
        response_code = response.getcode()
        response_headers = response.info()
        self.opener.close()
        debug(self.config, "RECEIVED_RESPONSE", response_code, str(response_headers))
        if response_code != 302:
            raise Exception("UNEXPECTED_HTTP_RESPONSE_CODE", response_code, str(response_headers))
        if GoogleTokenPageElements.LOCATION not in response_headers:
            raise Exception("REDIRECT_LOCATION_NOT_FOUND", response_code, str(response_headers))
        redirect_location = response_headers[GoogleTokenPageElements.LOCATION]
        fragment_url = self.get_fragment(redirect_location)
        debug(self.config, "URL_FRAGMENT", fragment_url)
        fragment_url_obj = parse_qs(fragment_url)
        if GoogleTokenPageElements.ACCESS_TOKEN not in fragment_url_obj:
            raise Exception("ACCESS_TOKEN_NOT_FOUND", response_code, str(response_headers))
        access_token = self.get_first_value(fragment_url_obj, GoogleTokenPageElements.ACCESS_TOKEN)
        expires_in_seconds = self.get_first_value(fragment_url_obj, GoogleTokenPageElements.EXPIRES_IN)
        from datetime import datetime, timedelta
        expiry_utc = datetime.utcnow() + timedelta(seconds=int(expires_in_seconds))

        return access_token, expiry_utc

    @staticmethod
    def get_first_value(obj, attr_name):
        for item in obj[attr_name] or []:
            return item
        return obj[attr_name]

    @staticmethod
    def get_fragment(url):
        parsed = urlparse(url)
        if parsed.fragment is None:
            raise Exception("URL_FRAGMENT_NOT_FOUND")
        return parsed.fragment
