# -*- coding: utf-8 -*-
"""
Created on Sat Jul 30 17:40:57 2022

@author: nadph
"""

from ecdsa import SigningKey, NIST384p
sk = SigningKey.generate(curve=NIST384p)
vk = sk.verifying_key
signature = sk.sign(b"message")
print(signature.hex())
assert vk.verify(signature, b"message")
print(vk.verify(signature,b"message"))