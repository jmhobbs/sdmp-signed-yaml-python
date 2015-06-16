This is an attempt at implementing the [signed-yaml specification][signed-yaml]
 in Python.

The specification is not complete, so consider this an unfinished work.  
Additionally, other than being internally consistent, there has been no outside
 verification of this code.

# Try it out.

First, you need an RSA key. Create the public key now too for giggles.

    > openssl genrsa -out private_key.pem 2048
    > openssl rsa -in private_key.pem -pubout -out public_key.pem

Then, just run ``syml.py`` and it'll do a test document for you.

```
(env)jmhobbs@venera:~/Working/sdmp-signed-yaml ✪ python syml.py 
8gu6DhxzVOyt47BzVgmaTtAxYg21N40i4jMM7oyM2ZZ8M8V7z7zrE/pqJbswN4B3vNUDKAXA5E6EBFYJ
3TfEUyERQ6F7sBo16tssp9TIFNK1Mp4szTYG8aKZw8+vnICH5u7GvA50wQuIJTD0JKs4ZyYUor59pQPx
eqBLQ/R5lzjKN/IxscJyBWenreFqZcIdMqMGYjy88oKkyLb/L/0Db1JuoJdxuKQ1eDwdNbV2Hgx6R7xx
tJ3H4CTH3x0WRGbrAHShZ8TEZH7QLSXPtOcdWdY/3B/yaMJgALT3EeBkBtGp6EYBg6nA+AoddSBtdoKs
YuHYosVkxDUk2aHyXCiyIg==
---
a: ∆
b: {c: 3, d: 4}
...

```

That's all it does right now.

[signed-yaml]: https://github.com/sdmp/signed-yaml
