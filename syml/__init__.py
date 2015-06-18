# -*- coding: utf-8 -*-

import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS

from . import exceptions
from . import private


__all__ = ["Sign", "Verify", "exceptions"]


def Sign(document, private_key_path, private_key_passphrase=None):
    with open(private_key_path, 'rb') as key_handle:
        private_key = RSA.importKey(key_handle.read(), private_key_passphrase)
        if not private_key.has_private():
            raise exceptions.InvalidKeyException("Key can not sign. Private key required.")
        if private_key.size() < 2047:
            raise exceptions.InvalidKeyException("Key must be 2048 bits or larger.")

    document = private.conform_yaml_document(document)
    document_hash = private.hash_document(document)

    signer = PKCS1_PSS.new(private_key)
    signature = signer.sign(document_hash)
    return private.compose_message(document, base64.standard_b64encode(signature))


def Verify(message, public_key_path):
    with open(public_key_path, 'rb') as key_handle:
        public_key = RSA.importKey(key_handle.read())
        if public_key.size() < 2047:
            raise exceptions.InvalidKeyException("Key must be 2048 bits or larger.")

    signature, document = private.decompose_message(message)
    document_hash = private.hash_document(document)

    verifier = PKCS1_PSS.new(public_key)
    if verifier.verify(document_hash, base64.standard_b64decode(signature)):
        return document
    else:
        return None
