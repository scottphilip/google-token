from GoogleToken.Utils import *
from http.cookiejar import MozillaCookieJar
from http.cookiejar import Cookie
from pyotp.totp import TOTP
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import WebDriverWait
from os.path import join, exists
from os import makedirs
from time import time, sleep
from datetime import datetime
from urllib.parse import urlparse


class GoogleTokenPhantomLogin(GoogleTokenBase):
    """
    PhantomJS log into google account to generate a refresh token.  Phantom
    is only required for the first login.
    """

    def __init__(self, params, config):
        super(GoogleTokenPhantomLogin, self).__init__(params, config)
        self.oauth2_url = self.__get_oauth_url()
        self.driver = webdriver \
            .PhantomJS(self.config.phantomjs_path,
                       desired_capabilities={
                           self.config.phantomjs_config_useragent:
                               self.config.user_agent})

    def wait_for(self, condition_function, timeout):
        start_time = time()
        while time() < start_time + timeout:
            if condition_function():
                return True
            else:
                sleep(0.5)
        self.save_screen_shot("TIMEOUT")
        return False

    def save_cookies(self):
        self.driver.get(self.config.url_accounts_noform)
        driver_cookies = self.driver.get_cookies()
        cookie_jar = MozillaCookieJar()
        for driver_cookie in driver_cookies:
            http_cookie = self.get_cookie(driver_cookie)
            cookie_jar.set_cookie(http_cookie)
        cookie_jar.save(self.__get_cookie_file_path(),
                        ignore_discard=self.config.cookies_ignore_discard)

    @staticmethod
    def get_cookie(item):
        return Cookie(item[GoogleTokenCookieKeys.VERSION] if GoogleTokenCookieKeys.VERSION in item else 1,
                                     item[GoogleTokenCookieKeys.NAME] if GoogleTokenCookieKeys.NAME in item else None,
                                     item[GoogleTokenCookieKeys.VALUE] if GoogleTokenCookieKeys.VALUE in item else None,
                                     item[GoogleTokenCookieKeys.PORT] if GoogleTokenCookieKeys.PORT in item else None,
                                     True if GoogleTokenCookieKeys.PORT in item else False,
                                     item[GoogleTokenCookieKeys.DOMAIN] if GoogleTokenCookieKeys.DOMAIN in item else None,
                                     True if GoogleTokenCookieKeys.DOMAIN in item else False,
                                     True if GoogleTokenCookieKeys.DOMAIN in item and
                                             item[GoogleTokenCookieKeys.DOMAIN].startswith(".") in item else False,
                                     item[GoogleTokenCookieKeys.PATH] if GoogleTokenCookieKeys.PATH in item else None,
                                     True if GoogleTokenCookieKeys.PATH in item else False,
                                     True if GoogleTokenCookieKeys.SECURE in item else False,
                                     item[GoogleTokenCookieKeys.EXPIRY] if GoogleTokenCookieKeys.EXPIRY in item else None,
                                     True if GoogleTokenCookieKeys.DISCARD in item else False,
                                     item[GoogleTokenCookieKeys.COMMENT] if GoogleTokenCookieKeys.COMMENT in item else None,
                                     item[GoogleTokenCookieKeys.COMMENT_URL] if GoogleTokenCookieKeys.COMMENT_URL in
                                                                                item else None,
                                     1,
                                     rfc2109=True) if item is not None else None

    def save_screen_shot(self, name):
        if self.params.image_path is not None:
            folder_path = join(self.params.image_path, self.params.account_email)
            if not exists(folder_path):
                makedirs(folder_path)
            file_name = "{0}-{1}.png"\
                .format(str(datetime.now().strftime("%Y%m%d-%H%M%S")), name)
            full_path = join(folder_path, file_name)
            self.driver.get_screenshot_as_file(full_path)
            self.__debug("SCREEN_SHOT_SAVED", self.driver.current_url, full_path)

    def open_login_page(self):
        self.__debug("PHANTOM_JS_LOGIN_START")
        self.driver.get(self.oauth2_url)
        self.save_screen_shot("LOGIN_PAGE")

    def enter_email(self):
        self.save_screen_shot("ENTER_EMAIL")
        WebDriverWait(self.driver, self.config.timeout_seconds)\
            .until(ec.element_to_be_clickable((By.ID, GoogleTokenPageElements.EMAIL)))
        self.driver.find_element_by_id(GoogleTokenPageElements.EMAIL)\
            .send_keys(self.params.account_email)
        WebDriverWait(self.driver, self.config.timeout_seconds)\
            .until(ec.element_to_be_clickable((By.ID, GoogleTokenPageElements.NEXT)))
        self.driver.find_element_by_id(GoogleTokenPageElements.NEXT).click()

    def enter_password(self):
        self.save_screen_shot("ENTER_PASSWORD")
        WebDriverWait(self.driver, self.config.timeout_seconds)\
            .until(ec.element_to_be_clickable((By.ID, GoogleTokenPageElements.PASSWD)))
        self.driver.find_element_by_id(GoogleTokenPageElements.PASSWD)\
            .send_keys(self.params.account_password)
        WebDriverWait(self.driver, self.config.timeout_seconds)\
            .until(ec.element_to_be_clickable((By.ID, GoogleTokenPageElements.SIGNIN)))
        self.driver.find_element_by_id(GoogleTokenPageElements.SIGNIN).click()

    @staticmethod
    def get_challenge_url(type):
        return "/{0}/{1}".format(GoogleTokenPageElements.CHALLENGE, type)

    def dual_factor(self):
        if self.driver.current_url.find(self.get_challenge_url(GoogleTokenChallengeTypes.TOTP)) > 0:
            return self.enter_totp(self.params.otp_secret)
        elif self.driver.current_url.count(self.get_challenge_url(GoogleTokenChallengeTypes.AZ)) > 0:
            return self.wait_for(self.is_login_complete, 300)
        return True

    def enter_totp(self, otp_secret):
        self.save_screen_shot("ENTER_ONE_TIME_PASS_CODE")
        if otp_secret is None:
            raise Exception("REQUIRED_TOTP_SECRET_IS_EMPTY")
        code = TOTP(otp_secret).now()
        WebDriverWait(self.driver, self.config.timeout_seconds)\
            .until(ec.element_to_be_clickable((By.ID, GoogleTokenPageElements.TOTPPIN)))
        self.driver.find_element_by_id(GoogleTokenPageElements.TOTPPIN).send_keys(code)
        self.driver.find_element_by_id(GoogleTokenPageElements.SUBMIT).click()
        return True

    def login(self):
        self.open_login_page()
        self.enter_email()
        self.enter_password()
        if not self.dual_factor():
            raise Exception("DUAL FACTOR LOGIN ERROR.", self.driver.current_url)
        if not self.wait_login_complete():
            self.__debug("UNABLE_TO_CONFIRM_SUCCESSFUL_LOGIN", self.driver.current_url)
        return self.get_script_result()

    def wait_login_complete(self):
        return self.wait_for(self.is_login_complete, self.params.timeout_seconds)

    def is_login_complete(self):
        if self.params.execute_script is not None:
            return self.driver.execute_script("return {0} != null".format(self.params.execute_script))
        current_url_obj = urlparse(self.driver.current_url)
        redirect_url_obj = urlparse(self.params.oauth_redirect_uri)
        return current_url_obj.netloc.upper() == redirect_url_obj.netloc.upper()

    def get_script_result(self):
        if self.params.execute_script is not None:
            return self.driver.execute_script("return {0}".format(self.params.execute_script))
        return True
