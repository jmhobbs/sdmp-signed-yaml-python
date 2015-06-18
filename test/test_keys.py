# -*- coding: utf-8 -*-

import unittest
import os.path

import syml

document = """---
a: Hello
b:
    - c
    - d
..."""

class TestKeys (unittest.TestCase):

    def test_key_size(self):
        """Keys must be 2048 bits"""

        self.assertRaises(syml.exceptions.InvalidKeyException,
                          syml.Sign,
                          document,
                          os.path.join(os.path.dirname(__file__), "keys", "private_key_512.pem")
                          )

    def test_private_key(self):
        """You can't sign with a public key"""

        self.assertRaises(syml.exceptions.InvalidKeyException,
                          syml.Sign,
                          document,
                          os.path.join(os.path.dirname(__file__), "keys", "public_key.pem")
                          )
