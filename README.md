# Practice
Innovation and Entrepreneurship Practice<br>
所实现的项目<br>
1.MD结构选择SM3实现基本生成杂凑值功能<br>
2.实现SM3的生日攻击<br>
3.实现MD5的中间相遇攻击<br>
4.实现SM2的基本加密解密功能<br>
5.SM2数字签名<br>
6.用python实现比特币并模拟进行交易<br>
7.实现构造默克尔树<br>
项目介绍<br>
MD结构选择SM3实现基本生成杂凑值功能<br>
代码运行效果如下图示：
![image](https://github.com/nadphwr/Practice/blob/main/sm3.png)<br>
please input the plaintext:12b3456def87eab98721f<br>
杂凑值: 880e532b620efd5e6e456b49f905cdc906161bc76e967a352ddfac0aa52afd6<br>
可见能正常生成杂凑值。<br>
SM3的生日攻击<br>
通过建立消息库，随机选取一个消息生成其杂凑值，再遍历消息库看是否产生碰撞。<br>
MD5的中间相遇攻击（虚拟机实现）<br>
![image](https://github.com/nadphwr/Practice/blob/main/md5.png)<br>
SM2的加解密功能（有待完善）<br>
![image](https://github.com/nadphwr/Practice/blob/main/sm2.png)<br>
过程中的ECC类引用了参考代码，过程中使用的sm3算法为自己编写，但最后未能正确解密，考虑可能是自己编写的sm3代码运行时数据类型是str型，与ECC类的参考代码运行时的数据类型bytes型在encode时会产生一定的区别，所以导致解密过程存在一定问题，还需要后续继续完善。<br>
SM2签名<br>
![image](https://github.com/nadphwr/Practice/blob/main/sign.png)<br>
用python实现比特币并模拟交易<br>
实现思路和代码参考了https://link.zhihu.com/?target=http%3A//karpathy.github.io/2021/06/21/blockchain/
先生成原始地址和交易的目的地址<br>
![image](https://github.com/nadphwr/Practice/blob/main/bitcoin1.png)<br>
之后<br>
![image](https://github.com/nadphwr/Practice/blob/main/bitcoin2.png)<br>
之后通过网页https://kuttler.eu/en/bitcoin/btc/faucet/获取虚拟比特币并进行交易<br>
![image](https://github.com/nadphwr/Practice/blob/main/模拟交易1.png)<br>
![image](https://github.com/nadphwr/Practice/blob/main/模拟交易2.png)<br>
默克尔树<br>
先建立几个高层节点，初始化为空，之后生成相应个数的底层节点，计算其哈希值，之后由下往上计算其父节点的哈希值，构造默克尔树。<br>
![image](https://github.com/nadphwr/Practice/blob/main/merkeltree1.png)<br>
![image](https://github.com/nadphwr/Practice/blob/main/merkeltree2.png)<br>
![image](https://github.com/nadphwr/Practice/blob/main/merkeltree3.png)<br>
![image](https://github.com/nadphwr/Practice/blob/main/merkeltree4.png)<br>
