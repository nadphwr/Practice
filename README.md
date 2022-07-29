# Practice
Innovation and Entrepreneurship Practice<br>
所实现的项目<br>
===========
1.MD结构选择SM3实现基本生成杂凑值功能<br>
---
2.实现SM3的生日攻击<br>
---
3.实现MD5的中间相遇攻击<br>
---
4.实现SM2的基本加密解密功能<br>
---
6.用python实现比特币并模拟进行交易<br>
---
7.实现构造默克尔树<br>
---
项目介绍<br>
=======
MD结构选择SM3实现基本生成杂凑值功能<br>
-----
代码运行效果如下图示：
![image](https://github.com/nadphwr/Practice/blob/main/sm3.png)<br>
please input the plaintext:12b3456def87eab98721f<br>
杂凑值: 880e532b620efd5e6e456b49f905cdc906161bc76e967a352ddfac0aa52afd6<br>
可见能正常生成杂凑值。<br>
SM3的生日攻击<br>
---
MD5的中间相遇攻击（虚拟机实现）<br>
---
![image](https://github.com/nadphwr/Practice/blob/main/md5.png)<br>
SM2的加解密功能（有待完善）<br>
---
![image](https://github.com/nadphwr/Practice/blob/main/sm2.png)<br>
过程中的ECC类引用了参考代码，过程中使用的sm3算法为自己编写，但最后未能正确解密，考虑可能是自己编写的sm3代码运行时数据类型是str型，与ECC类的参考代码运行时的数据类型bytes型在encode时会产生一定的区别，所以导致解密过程存在一定问题，还需要后续继续完善。<br>
