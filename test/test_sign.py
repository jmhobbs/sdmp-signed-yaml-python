# -*- coding: utf-8 -*-

import unittest
import os.path

import syml


class TestSign (unittest.TestCase):

    def test_string_document(self):
        document = """---
a: Hello
b:
    - c
    - d
..."""

        message = syml.Sign(document, os.path.join(os.path.dirname(__file__), "keys", "private_key.pem"))
        self.assertIsNotNone(message)
        self.assertIsInstance(message, unicode)

    def test_unicode_document(self):
        document = u"""---
a: ∆
b:
    - c
    - d
..."""

        message = syml.Sign(document, os.path.join(os.path.dirname(__file__), "keys", "private_key.pem"))
        self.assertIsNotNone(message)
        self.assertIsInstance(message, unicode)

    def test_object_document(self):
        document = {"a": u"∆", "b": ["c", "d"]}
        message = syml.Sign(document, os.path.join(os.path.dirname(__file__), "keys", "private_key.pem"))
        self.assertIsNotNone(message)
        self.assertIsInstance(message, unicode)
