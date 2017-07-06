from GoogleToken.Utils import *
from http.cookiejar import MozillaCookieJar
from os.path import isfile
from urllib.parse import urlparse, parse_qs
from urllib.request import build_opener, Request, HTTPCookieProcessor


class GoogleTokenGenerator(GoogleTokenBase):
    """
    Google Token Generator
    """

    def __init__(self, params, config=None):
        super(GoogleTokenGenerator, self).__init__(params, config)

    def generate(self):
        cookie_path = self.__get_cookie_file_path()
        if not isfile(cookie_path):
            self.__phantom_login()
        return self.__cookies_login()

    def __phantom_login(self):
        from GoogleToken.Phantom import GoogleTokenPhantomLogin
        phantom_login = GoogleTokenPhantomLogin(self.params, self.config)
        phantom_login.login()
        phantom_login.save_cookies()

    def __cookies_login(self):
        with GoogleTokenHttpHandler(self.params, self.config) as http_handler:
            return http_handler.get_access_token()


class GoogleTokenHttpHandler(GoogleTokenBase):
    """
    Http Handler
    """

    def __init__(self, params, config):
        super(GoogleTokenHttpHandler, self).__init__(params, config)
        self.cookie_jar = MozillaCookieJar()
        if not isfile(self.__get_cookie_file_path()):
            raise Exception("COOKIE_FILE_NOT_FOUND", self.__get_cookie_file_path())
        self.cookie_jar.load(self.__get_cookie_file_path())
        self.opener = build_opener(GoogleTokenHttpNoRedirect,
                          HTTPCookieProcessor(self.cookie_jar))

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cookie_jar.save(self.__get_cookie_file_path(),
                             ignore_discard=self.config.cookies_ignore_discard)

    def get_access_token(self):
        request = Request(self.__get_oauth_url(),
                                         headers=self.config.default_headers,
                                         method="GET")
        response = self.opener.open(request)
        response_code = response.getcode()
        response_headers = response.info()
        if response_code != 302:
            raise Exception("UNEXPECTED_HTTP_RESPONSE_CODE", response_code)
        if GoogleTokenPageElements.LOCATION not in response_headers:
            raise Exception("REDIRECT_LOCATION_NOT_FOUND", response_headers)
        redirect_location = response_headers[GoogleTokenPageElements.LOCATION]
        fragment_url = self.__get_fragment(redirect_location)
        fragment_url_obj = parse_qs(fragment_url)
        if GoogleTokenPageElements.ACCESS_TOKEN not in fragment_url_obj:
            raise Exception("ACCESS_TOKEN_NOT_FOUND", fragment_url_obj)
        return fragment_url_obj[GoogleTokenPageElements.ACCESS_TOKEN]

    @staticmethod
    def __get_fragment(url):
        parsed = urlparse(url)
        if parsed.fragment is None:
            raise Exception("URL_FRAGMENT_NOT_FOUND")
        return parsed.fragment
