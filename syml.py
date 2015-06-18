# -*- coding: utf-8 -*-

import math
import string
import yaml
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_PSS
from Crypto.Hash import SHA256


# TODO: numpy or something has to have better options for these
def pack(i):
    b = bytearray()
    while i:
        b.append(i & 0xFF)
        i >>= 8
    return b


def unpack(b):
    b = bytearray(b.encode("utf8"))
    return sum((1 << (bi*8)) * bb for (bi, bb) in enumerate(b))


def verify_digest(digest, signature, public_key_path):
    with open(public_key_path, 'rb') as key_handle:
        key = RSA.importKey(key_handle.read())
        if key.size() < 2047:
            raise Exception("Key must be 2048 bits or larger.")
        verifier = PKCS1_PSS.new(key)
        return verifier.verify(digest, base64.standard_b64decode(signature))


def sign_digest(digest, private_key_path):
    with open(private_key_path, 'rb') as key_handle:
        key = RSA.importKey(key_handle.read())
        if not key.can_sign():
            raise Exception("Private key required.")
        if key.size() < 2047:
            raise Exception("Key must be 2048 bits or larger.")
        signer = PKCS1_PSS.new(key)
        sig = signer.sign(digest)
        return base64.standard_b64encode(sig)


def conform_yaml_document(document):
    """Takes a loose YAML document and forces conformance to signed yaml spec."""
    # Unicode support requires some tinkering.
    # http://pyyaml.org/ticket/11
    if type(unicode) != document:
        document = document.decode("utf-8")

    spec_doc = (yaml.safe_dump(yaml.safe_load(document),
                               explicit_start=True,
                               explicit_end=True,
                               allow_unicode=True)).decode("utf-8")
    spec_doc = spec_doc.strip(" \r\n\t")
    return spec_doc


def message_digest(document):
    """Expects document as a unicode object."""
    digest = SHA256.new()
    digest.update(document.encode("utf-8"))
    return digest


def compose_message(document, signature):
    chunks = int(math.ceil(len(signature)/80.0))
    signature = "\r\n".join([signature[i*80:i*80+80] for i in range(0, chunks)])
    return signature + "\r\n" + document


def decompose_message(message):
    division_index = string.find(message, "\r\n---")
    if division_index == -1:
        raise Exception("Invalid SYML Document")
    return message[:division_index].replace("\r\n", ""), message[division_index+2:]


if __name__ == "__main__":
    document = """
  a: ∆
  b:
    c: 3
    d: 4
"""

    document = conform_yaml_document(document)
    digest = message_digest(document)
    signature = sign_digest(digest, "./private_key.pem")

    message = compose_message(document, signature)

    print message

    signature, document = decompose_message(message)
    d_digest = message_digest(document)

    print "verify:", verify_digest(d_digest, signature, "./public_key.pem")
