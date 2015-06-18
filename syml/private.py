# -*- coding: utf-8 -*-

import math
import string
import yaml
from Crypto.Hash import SHA256

from . import exceptions


def conform_yaml_document(document):
    """Takes a loose YAML document and forces conformance to signed yaml spec."""
    # Unicode body requires some tinkering.
    # http://pyyaml.org/ticket/11
    if isinstance(document, basestring):
        if not isinstance(document, unicode):
            document = document.decode("utf-8")
        document = yaml.safe_load(document)

    spec_doc = (yaml.safe_dump(document,
                               explicit_start=True,
                               explicit_end=True,
                               allow_unicode=True,
                               default_flow_style=False)).decode("utf-8")
    # Message message_hash is for the YAML body _only_
    spec_doc = spec_doc.strip(" \r\n\t")
    return spec_doc


def hash_document(document):
    message_hash = SHA256.new()
    message_hash.update(document.encode("utf-8"))
    return message_hash


def compose_message(document, signature):
    chunks = int(math.ceil(len(signature)/80.0))
    signature = "\r\n".join([signature[i*80:i*80+80] for i in range(0, chunks)])
    return signature + "\r\n" + document


def decompose_message(message):
    """Split a message into document and signature"""
    division_index = string.find(message, "\r\n---")
    if division_index == -1:
        raise exceptions.InvalidMessageException("Invalid Secure YAML Document")
    return message[:division_index].replace("\r\n", ""), message[division_index+2:]
