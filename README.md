This is an attempt at implementing the [signed-yaml specification][signed-yaml]
 in Python.

The specification is not complete, so consider this an unfinished work.  
Additionally, other than being internally consistent, there has been no outside
 verification of this code.


# API

Super simple API for now.

## syml.Sign(_document_, _private_key_path_, _private_key_passphrase_=None)

#### Arguments

  * ``document`` - A YAML document, as a ``string``, ``unicode`` or ``object``.
  * ``private_key_path`` - File path to the private key as PEM
  * ``private_key_passphrase`` - Passphrase for private key, if needed

#### Return

A ``unicode`` object of the signed message.

#### Raises

  * ``syml.exceptions.InvalidKeyException``

## syml.Verify(_message_, _public_key_path_)

#### Arguments

  * ``message`` - A signed YAML message, as ``unicode``.
  * ``public_key_path`` - File path to the public key as PEM

#### Return

``None`` if document does not verify.  ``unicode`` document string if it does.

#### Raises

  * ``syml.exceptions.InvalidKeyException``

[signed-yaml]: https://github.com/sdmp/signed-yaml
