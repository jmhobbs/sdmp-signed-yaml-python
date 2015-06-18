# -*- coding: utf-8 -*-

import unittest
import os.path

import yaml

import syml

document = """---
a: Hello
b:
    - c
    - d
..."""


class TestVerify (unittest.TestCase):

    def test_valid_verify(self):
        message = syml.Sign(document, os.path.join(os.path.dirname(__file__), "keys", "private_key.pem"))
        result = syml.Verify(message, os.path.join(os.path.dirname(__file__), "keys", "public_key.pem"))
        self.assertIsNotNone(result)
        self.assertEqual(yaml.load(document), yaml.load(result))

    def test_invalid_verify(self):
        message = syml.Sign(document, os.path.join(os.path.dirname(__file__), "keys", "private_key.pem"))
        result = syml.Verify(message, os.path.join(os.path.dirname(__file__), "keys", "public_key_unmatched.pem"))
        self.assertIsNone(result)
