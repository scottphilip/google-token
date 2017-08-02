# Author:       Scott Philip (sp@scottphilip.com)
# Version:      0.7 (30 July 2017)
# Source:       https://github.com/scottphilip/google-token/
# Licence:      GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007)
import json
import requests
from os.path import dirname
from GoogleToken.Crypto import encrypt, decrypt
try:
    from urllib.parse import urlencode
    from urllib.request import HTTPErrorProcessor
except ImportError:
    from urllib import urlencode
    from urllib2 import HTTPErrorProcessor


KEY_DIR_NAME = ".keys"


def get_oauth_url(config):
    data = {}
    data.update(config.oauth2_data)
    for key in data:
        if hasattr(config, data[key]):
            data[key] = getattr(config, data[key])
    return "{0}://{1}{2}?{3}" \
        .format(config.oauth2_protocol,
                config.oauth2_domain,
                config.oauth2_path, urlencode(data))


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


def save_cookie_jar(config, cookie_jar):
    file_content = json.dumps(requests.utils.dict_from_cookiejar(cookie_jar))
    if not config.cookies_store_plain:
        file_content = encrypt(value=file_content,
                               account=config.account_email,
                               data_dir=dirname(config.cookie_storage_path),
                               logger=config.logger)
    with open(config.cookie_storage_path, "w") as file:
        file.write(file_content)


def open_cookie_jar(config):
    with open(config.cookie_storage_path, "r") as file:
        file_content = file.read()
    cookies_json = _get_json(file_content)
    if cookies_json is None:
        decrypted = decrypt(value=file_content,
                            account=config.account_email,
                            data_dir=dirname(config.cookie_storage_path),
                            logger=config.logger)
        cookies_json = _get_json(decrypted, True)

    return requests.utils.cookiejar_from_dict(cookies_json)


def _get_json(value, throw_on_error=False):
    try:
        j = json.loads(value)
        return j
    except:
        if not throw_on_error:
            return None
        raise

#
# def __get_system_identity():
#     pattern = "[^0-9a-zA-Z]+"
#     keys = []
#     for index, item_name in enumerate(platform.uname()):
#         keys.append(platform.uname()[index].upper())
#     result = "-".join(keys)
#     return re.sub(pattern, "", result)
#
#
# def __get_system_key(config):
#     machine_id = __get_system_identity().upper()
#     if sys.version_info[0] >= 3:
#         machine_id = bytes(machine_id, encoding="utf-8")
#     else:
#         machine_id = bytes(machine_id)
#     digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
#     digest.update(machine_id)
#     return urlsafe_b64encode(digest.finalize())
#
#
# def __get_key(config):
#     h = hashlib.new("ripemd160")
#     if sys.version_info[0] >= 3:
#         account = bytes(config.account_email.upper(), "utf-8")
#     else:
#         account = bytes(config.account_email.upper())
#     h.update(account)
#     key_dir = join(dirname(config.cookie_storage_path), KEY_DIR_NAME)
#     if not isdir(key_dir):
#         makedirs(key_dir)
#     key_path = join(key_dir, ".{0}".format(h.hexdigest()))
#     f = Fernet(key=__get_system_key(config))
#     if not isfile(key_path):
#         key = Fernet.generate_key()
#         with open(key_path, "w+") as file:
#             encoded = b64encode(key)
#             file.write(f.encrypt(encoded).decode("utf-8"))
#         if osname == 'nt':
#             try:
#                 ctypes.windll.kernel32.SetFileAttributesW(key_path, 0x02)
#             except:
#                 ignore = True
#     with open(key_path, "r+") as file:
#         if sys.version_info[0] >= 3:
#             data = bytes(file.read(), encoding="utf-8")
#         else:
#             data = bytes(file.read())
#         return b64decode(f.decrypt(data))
#
#
# def __encrypt(config, plain_text):
#     if not plain_text:
#         return ""
#     from cryptography.fernet import Fernet
#     if sys.version_info[0] >= 3:
#         bytes_text = bytes(plain_text, encoding="ascii")
#     else:
#         bytes_text = bytes(plain_text)
#     cipher_suite = Fernet(key=__get_key(config))
#     token = cipher_suite.encrypt(bytes_text)
#     return b64encode(token).decode("utf-8")
#
#
# def __decrypt(config, encrypted_text):
#     if not encrypted_text:
#         return ""
#     if sys.version_info[0] >= 3:
#         data = b64decode(bytes(encrypted_text, encoding="utf-8"))
#     else:
#         data = b64decode(bytes(encrypted_text))
#     cipher_suite = Fernet(key=__get_key(config))
#     return cipher_suite.decrypt(data).decode("utf-8")
