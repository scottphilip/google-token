# Author:       Scott Philip (sp@scottphilip.com)
# Version:      0.7 (30 July 2017)
# Source:       https://github.com/scottphilip/google-token/
# Licence:      GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007)
import GoogleToken.Configuration

from GoogleToken.Utils import *
from http.cookiejar import MozillaCookieJar
from http.cookiejar import Cookie
from pyotp.totp import TOTP
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from os.path import join, exists
from os import makedirs
from time import time, sleep
from datetime import datetime
try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class GoogleTokenPhantomLogin(object):
    """
    PhantomJS log into google account to generate a refresh token.  Phantom
    is only required for the first login.
    """

    def __init__(self, config):
        self.config = config
        debug(self.config, "SYSTEM_CONFIGURATION", self.config.json())
        self.oauth2_url = get_oauth_url(self.config)
        self.driver = webdriver \
            .PhantomJS(executable_path=self.config.phantomjs_path,
                       service_log_path=self.config.phantomjs_log_path,
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
        self.driver.get(self.config.url_accounts_no_form)
        driver_cookies = self.driver.get_cookies()
        cookie_jar = MozillaCookieJar()
        for driver_cookie in driver_cookies:
            http_cookie = self.get_cookie(driver_cookie)
            cookie_jar.set_cookie(http_cookie)
        save_cookie_jar(self.config, cookie_jar)

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
        if self.config.image_path is not None:
            folder_path = join(self.config.image_path)
            if not exists(folder_path):
                makedirs(folder_path)
            file_name = "{0}-{1}.png" \
                .format(str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")), name)
            full_path = join(folder_path, file_name)
            self.driver.get_screenshot_as_file(full_path)
            debug(self.config, "SCREEN_SHOT_SAVED", self.driver.current_url, full_path)

    def open_login_page(self):
        debug(self.config, "PHANTOM_JS_LOGIN_START")
        self.driver.get(self.oauth2_url)
        self.save_screen_shot("LOGIN_PAGE")

    def enter_email(self):
        self.save_screen_shot("ENTER_EMAIL")
        WebDriverWait(self.driver, self.config.timeout_seconds)\
            .until(expected_conditions.element_to_be_clickable((By.ID, GoogleTokenPageElements.EMAIL)))
        self.driver.find_element_by_id(GoogleTokenPageElements.EMAIL) \
            .send_keys(self.config.account_email)
        WebDriverWait(self.driver, self.config.timeout_seconds)\
            .until(expected_conditions.element_to_be_clickable((By.ID, GoogleTokenPageElements.NEXT)))
        self.driver.find_element_by_id(GoogleTokenPageElements.NEXT).click()

    def enter_password(self):
        self.save_screen_shot("ENTER_PASSWORD")
        WebDriverWait(self.driver, self.config.timeout_seconds)\
            .until(expected_conditions.element_to_be_clickable((By.ID, GoogleTokenPageElements.PASSWD)))
        self.driver.find_element_by_id(GoogleTokenPageElements.PASSWD) \
            .send_keys(self.config.account_password)
        WebDriverWait(self.driver, self.config.timeout_seconds)\
            .until(expected_conditions.element_to_be_clickable((By.ID, GoogleTokenPageElements.SIGNIN)))
        self.driver.find_element_by_id(GoogleTokenPageElements.SIGNIN).click()

    @staticmethod
    def get_challenge_path(type):
        return "/{0}/{1}".format(GoogleTokenPageElements.CHALLENGE, type)

    def dual_factor(self):
        if self.driver.current_url.find(self.get_challenge_path(GoogleTokenChallengeTypes.TOTP)) > 0:
            return self.enter_totp(self.config.account_otp_secret)
        elif self.driver.current_url.count(self.get_challenge_path(GoogleTokenChallengeTypes.AZ)) > 0:
            return self.wait_for(self.is_login_complete, 300)
        return True

    def enter_totp(self, otp_secret):
        self.save_screen_shot("ENTER_ONE_TIME_PASS_CODE")
        if otp_secret is None:
            raise Exception("REQUIRED_TOTP_SECRET_IS_EMPTY")
        code = TOTP(otp_secret).now()
        WebDriverWait(self.driver, self.config.timeout_seconds)\
            .until(expected_conditions.element_to_be_clickable((By.ID, GoogleTokenPageElements.TOTPPIN)))
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
            debug(self.config, "UNABLE_TO_CONFIRM_SUCCESSFUL_LOGIN", self.driver.current_url)
        return self.get_script_result()

    def wait_login_complete(self):
        return self.wait_for(self.is_login_complete, self.config.timeout_seconds)

    def is_login_complete(self):
        if self.config.execute_script is not None:
            return self.driver.execute_script("return {0} != null".format(self.config.execute_script))
        current_url_obj = urlparse(self.driver.current_url)
        redirect_url_obj = urlparse(self.config.oauth_redirect_uri)
        return current_url_obj.netloc.upper() == redirect_url_obj.netloc.upper()

    def get_script_result(self):
        if self.config.execute_script is not None:
            return self.driver.execute_script("return {0}".format(self.config.execute_script))
        return True
