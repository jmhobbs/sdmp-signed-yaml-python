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

class TestSanity (unittest.TestCase):

    def test_sanity(self):
        """Sanity check that we are internally consistent."""

        message = syml.Sign(document, os.path.join(os.path.dirname(__file__), "keys", "private_key.pem"))
        result = syml.Verify(message, os.path.join(os.path.dirname(__file__), "keys", "public_key.pem"))

        self.assertTrue(result)
