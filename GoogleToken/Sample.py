# Author:       Scott Philip (sp@scottphilip.com)
# Version:      0.3 (13 July 2017)
# Source:       https://github.com/scottphilip/google-token/
# Licence:      GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007)

from GoogleToken import GoogleTokenGenerator, GoogleTokenConfiguration


class Sample(object):
    @staticmethod
    def create_cookie_file(config):
        generator = GoogleTokenGenerator(config)
        token = generator.generate()
        if token is None:
            raise Exception("LOGIN_FAILED")

    @staticmethod
    def get_access_token(config):
        generator = GoogleTokenGenerator(config)
        return generator.generate()
