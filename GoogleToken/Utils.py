from GoogleToken.Configuration import GoogleTokenConfiguration
from urllib.parse import urlencode
from urllib.request import HTTPErrorProcessor


class GoogleTokenBase(object):
    """
    Base helper class
    """

    def __init__(self, params, config):
        self.params = params
        self.config = config if config is not None else GoogleTokenConfiguration()

    def __get_oauth_url(self):
        data = self.config.oauth2_data
        for key in data:
            if data[key].upper() in self.params.upper():
                data[key] = self.params[key]
        return "{0}://{1}{2}?{3}" \
            .format(self.config.oauth2_protocol,
                    self.config.oauth2_domain,
                    self.config.oauth2_path,
                    urlencode(data))

    def __get_cookie_file_path(self):
        if self.params.cookie_storage_path is not None:
            return self.params.cookie_storage_path
        return "~/GoogleToken/{0}.cookies".format(self.params.account_email)

    def __error(self, *args):
        if self.params.logger is not None:
            self.params.logger.error(args)

    def __debug(self, *args):
        if self.params.logger is not None:
            self.params.logger.debug(args)


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


class GoogleTokenChallengeTypes(object):
    """
    Google Challenge Types
    """
    AZ = "az"
    TOTP = "totp"
