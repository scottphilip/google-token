import unittest
from GoogleToken import GoogleTokenParameters


class TestConfiguration(unittest.TestCase):

    def test_create_instance_googletokenparameters(self):
        instance = GoogleTokenParameters()
        self.assertIsNotNone(instance, "GoogleTokenParameters instance is None")
