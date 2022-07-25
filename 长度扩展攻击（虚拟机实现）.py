# -*- coding: utf-8 -*-
"""
Created on Mon Jul 25 13:24:39 2022

@author: nadph
"""

'''长度扩展攻击'''

import hashlib
import hashpumpy

key=b'flag{0987654321234567890abcdefg}add_salt'
str_md5 = hashlib.md5(key).hexdigest()
print(str_md5)
md5_att=hashpumpy.hashpump(str_md5,'add_salt','length_extend',32)
print(md5_att)
flag=b'flag{0987654321234567890abcdefg}'
attend=md5_att[1]
print(hashlib.md5(flag+attend).hexdigest())
