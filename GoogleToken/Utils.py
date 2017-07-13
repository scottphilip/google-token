# Author:       Scott Philip (sp@scottphilip.com)
# Version:      0.4 (13 July 2017)
# Source:       https://github.com/scottphilip/google-token/
# Licence:      GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007)

from GoogleToken.Configuration import GoogleTokenConfiguration
from os.path import expanduser, join
try:
    from urllib.parse import urlencode
    from urllib.request import HTTPErrorProcessor
except ImportError:
    from urllib import urlencode
    from urllib2 import HTTPErrorProcessor


class GoogleTokenBase(object):
    """
    Base helper class
    """

    def __init__(self, config):
        self.config = config if config is not None else GoogleTokenConfiguration()

    def get_oauth_url(self):
        data = {}
        data.update(self.config.oauth2_data)
        for key in data:
            if hasattr(self.config, data[key]):
                data[key] = getattr(self.config, data[key])
        return "{0}://{1}{2}?{3}" \
            .format(self.config.oauth2_protocol,
                    self.config.oauth2_domain,
                    self.config.oauth2_path,
                    urlencode(data))

    def get_cookie_file_path(self):
        if self.config.cookie_storage_path is not None:
            return self.config.cookie_storage_path
        return join(expanduser("~"), "{0}.cookies".format(self.config.account_email))


class GoogleTokenHttpNoRedirect(HTTPErrorProcessor):
    """
    Http No Redirect Handler
    """
    def http_response(self, request, response):
        return response
    https_response = http_response


class GoogleTokenCookieKeys(object):
    """
    Cookie Object Keys
    """
    VERSION = "version"
    NAME = "name"
    VALUE = "value"
    PORT = "port"
    DOMAIN = "domain"
    PATH = "path"
    SECURE = "secure"
    EXPIRY = "expiry"
    DISCARD = "discard"
    COMMENT = "comment"
    COMMENT_URL = "comment_url"


class GoogleTokenPageElements(object):
    """
    Google Login Page Elements
    """
    TOTPPIN = "totpPin"
    EMAIL = "Email"
    SUBMIT = "submit"
    NEXT = "next"
    PASSWD = "Passwd"
    CHALLENGE = "challenge"
    SIGNIN = "signIn"
    LOCATION = "location"
    ACCESS_TOKEN = "access_token"
    EXPIRES_IN = "expires_in"


class GoogleTokenChallengeTypes(object):
    """
    Google Challenge Types
    """
    AZ = "az"
    TOTP = "totp"


def debug(config, *args, **kwargs):
    if config.logger is not None:
        config.logger.debug(["GOOGLE_TOKEN", args], **kwargs)


def error(config, *args, **kwargs):
    if config.logger is not None:
        config.logger.error(["GOOGLE_TOKEN", args], **kwargs)
