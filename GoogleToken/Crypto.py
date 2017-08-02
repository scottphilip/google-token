# Author:       Scott Philip (sp@scottphilip.com)
# Version:      0.7 (30 July 2017)
# Source:       https://github.com/scottphilip/google-token/
# Licence:      GNU GENERAL PUBLIC LICENSE (Version 3, 29 June 2007)
from cryptography.fernet import Fernet, InvalidToken
from base64 import b64encode, b64decode, urlsafe_b64encode, urlsafe_b64decode
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import sys
from os.path import isdir, join, isfile
from os import makedirs
import hashlib
import re
import platform

INVALID_KEY = "INVALID_KEY"
PRIVATE_KEY_DIR_NAME = ".keys"
UTF8 = "utf-8"


def get_bytes(value):
    if sys.version_info[0] >= 3:
        value_bytes = bytes(value, UTF8)
    else:
        value_bytes = bytes(value)
    return value_bytes


def get_string(bytes_value):
    return bytes_value.decode(UTF8)


def to_encrypted_string(b):
    return get_string(b64encode(b))


def from_encrypted_string(s):
    return b64decode(get_bytes(s))


def get_system_identity():
    pattern = "[^0-9a-zA-Z]+"
    keys = []
    for index, item_name in enumerate(platform.uname()):
        keys.append(platform.uname()[index].upper())
    result = "-".join(keys)
    return re.sub(pattern, "", result)


def get_hash_sha256(value):
    key_bytes = get_bytes(value)
    digest = hashes.Hash(hashes.SHA256(), backend=default_backend())
    digest.update(key_bytes)
    return digest.finalize()


def get_hash_ripemd160(value):
    h = hashlib.new("ripemd160")
    value_bytes = get_bytes(value)
    h.update(value_bytes)
    return str(h.hexdigest())


def get_user_key_file_path(data_dir, username):
    dir_path = join(data_dir, PRIVATE_KEY_DIR_NAME)
    if not isdir(dir_path):
        makedirs(dir_path)
    username_hash = get_hash_ripemd160(username.upper())
    return join(dir_path, ".{0}".format(username_hash))


def encrypt_data(value_bytes, private_key):
    f = Fernet(key=private_key)
    return f.encrypt(value_bytes)


def decrypt_data(encrypted_bytes, private_key):
    f = Fernet(key=private_key)
    return f.decrypt(encrypted_bytes)


def get_system_key():
    return urlsafe_b64encode(get_hash_sha256(get_system_identity().upper()))


def get_user_key(account=None, data_dir=None, logger=None):
    if account is None or data_dir is None:
        return get_system_key()
    user_key_file_path = get_user_key_file_path(data_dir, account)
    if not isfile(user_key_file_path):
        if logger is not None:
            logger.debug(["GOOGLE_TOKEN", "CRYPTO_USER_KEY_CREATION", account, user_key_file_path])
        random_user_key = get_string(Fernet.generate_key())
        random_user_key_encrypted = encrypt_data(get_bytes(random_user_key),
                                                 get_system_key())
        with open(user_key_file_path, "w") as write_file:
            write_file.write(to_encrypted_string(random_user_key_encrypted))
    with open(user_key_file_path) as read_file:
        decrypted_bytes = decrypt_data(from_encrypted_string(read_file.read()), get_system_key())
    return decrypted_bytes


def encrypt(value, account=None, data_dir=None, logger=None):
    user_key = get_user_key(account, data_dir, logger)
    encrypted_bytes = encrypt_data(get_bytes(value), user_key)
    return to_encrypted_string(encrypted_bytes)


def decrypt(value, account=None, data_dir=None, logger=None):
    user_key = get_user_key(account, data_dir, logger)
    encrypted_bytes = from_encrypted_string(value)
    return get_string(decrypt_data(encrypted_bytes, user_key))
