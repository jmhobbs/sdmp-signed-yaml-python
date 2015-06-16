# -*- coding: utf-8 -*-

import math
import yaml
from hashlib import sha256
import base64
import Crypto.PublicKey.RSA as RSA


# TODO: numpy or something has to have better options for these
def pack(i):
    b = bytearray()
    while i:
        b.append(i & 0xFF)
        i >>= 8
    return b


def unpack(b):
    b = bytearray(b)
    return sum((1 << (bi*8)) * bb for (bi, bb) in enumerate(b))


def sign_digest(digest, key_path):
    with open(key_path, 'rb') as key_handle:
        key = RSA.importKey(key_handle.read())
        if not key.can_sign():
            raise Exception("Private key required.")
        if key.size() < 2047:
            raise Exception("Key must be 2048 bits or larger.")
        # TODO: Should this be using PKCS#1 PSS or PKCS#1 v1.5 or something?
        sig = key.sign(digest, None)[0]
        return base64.standard_b64encode(pack(sig))


def conform_yaml_document(document):
    """Takes a loose YAML document and forces conformance to signed yaml spec."""
    # Unicode support requires some tinkering.
    # http://pyyaml.org/ticket/11
    if type(unicode) != document:
        document = document.decode("utf-8")

    return (yaml.safe_dump(yaml.safe_load(document),
                           explicit_start=True,
                           explicit_end=True,
                           allow_unicode=True)).decode("utf-8")


def message_digest(document):
    """Expects document as a unicode object."""
    return sha256(document.encode("utf-8")).digest()


def compose_message(document, signature):
    chunks = int(math.ceil(len(signature)/80.0))
    signature = "\r\n".join([signature[i*80:i*80+80] for i in range(0, chunks)])
    return signature + "\r\n" + document


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

    print compose_message(document, signature)
