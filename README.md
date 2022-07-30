# Practice
Innovation and Entrepreneurship Practice<br>
成员：陈义薄云（所有项目完成人）<br>
所实现的项目<br>
1.MD结构选择SM3实现基本生成杂凑值功能<br>
2.实现SM3的生日攻击<br>
3.实现MD5的中间相遇攻击<br>
4.实现SM2的基本加密解密功能（存在解密正确性问题）<br>
5.SM2数字签名<br>
6.用python实现比特币并模拟进行交易<br>
7.实现构造默克尔树<br>
8.ECDSA<br>
未完成的项目<br>
1.尽最大努力优化SM3实现(软件)
2.forge a signature to pretend that you are Satoshi
3. verify the above pitfalls with proof-of-concept code
4.Implement a PGP scheme with SM2
5.PoC impl of the scheme, or do implement analysis by Google
6.implement sm2 2P decrypt with real network communication
7.forge a signature to pretend that you are Satoshi
8.research report on MP
9.Find a key with hash value “sdu_cst_20220610” under a message composed of your name followed by your student ID. For example, “San Zhan 202000460001”.
10.Find a 64-byte message under some  fulfilling that their hash value is symmetrical
11.Write a circuit to prove that your CET6 grade is larger than 425. a. Your grade info is like (cn_id, grade, year, sig_by_moe). These grades are published as commitments onchain by MoE. b. When you got an interview from an employer, you can prove to them that you have passed the exam without letting them know the exact grade.
12.The commitment scheme used by MoE is SHA256-based. a. commit = SHA256(cn_id, grade, year, sig_by_moe, r)
项目介绍<br>
MD结构选择SM3实现基本生成杂凑值功能<br>
SM3算法对于长度小于264位的消息，产生一个256位的消息摘要。算法以512位分组来处理输入的信息，每一分组又被划分为132个32位子分组，经过一系列的处理后，算法的输出由八个32位分组组成，将这些32位分组级联后产生一个256位的散列值。主要分为以下几个步骤：1.消息填充，对不满448bit倍数长度的消息，先填充1bit1，剩余比特填充0。之后再以大端方式填充64bit的消息长度。2.对消息进行分组扩展。3.对得到的消息字进行迭代运算，生成杂凑值。
代码运行效果如下图示：
![image](https://github.com/nadphwr/Practice/blob/main/sm3.png)<br>
please input the plaintext:12b3456def87eab98721f<br>
杂凑值: 880e532b620efd5e6e456b49f905cdc906161bc76e967a352ddfac0aa52afd6<br>
可见能正常生成杂凑值。<br>
SM3的生日攻击<br>
生日悖论，指如果一个房间里有23个或23个以上的人，那么至少有两个人的生日相同的概率要大于50%。这就意味着在一个典型的标准小学班级(30人)中，存在两人生日相同的可能性更高。对于60或者更多的人，这种概率要大于99%。即有大概率可以在一定的消息空间内找到碰撞。通过建立消息库，随机选取一个消息生成其杂凑值，再遍历消息库看是否产生碰撞。通过循环生成消息空间占用大量时间，之后依旧通过rho方法判断环找到摘要相同的碰撞，短时间内无运行结果。<br>
MD5的长度扩展攻击（虚拟机实现）<br>
首先是MD5的结构。MD5把每512位当作一组进行加密计算，首先有一个初始序列的值（该值是固定的），这个初始序列与信息的第一组512位进行运算，得到一个结果，该结果作为下一组512位的初始序列，再进行同样的运算，依此类推。需要注意的是，最后一个分组的后64位用来显示原消息的总长，是预留的，也就是说，最后一个分组只能有448。（https://blog.csdn.net/destiny1507/article/details/100543233）
因此要对消息进行填充。填充规则与sm3算法相同。因此若已知消息和消息摘要以及消息的长度，我们可以通过手动填充构建新的消息，计算其MD5值。同样可以成功。
![image](https://github.com/nadphwr/Practice/blob/main/md5.png)<br>
SM2的加解密功能（有待完善）<br>
![image](https://github.com/nadphwr/Practice/blob/main/sm2.png)<br>
过程中的ECC类引用了参考代码，过程中使用的sm3算法为自己编写，但最后未能正确解密，考虑可能是自己编写的sm3代码运行时数据类型是str型，与ECC类的参考代码运行时的数据类型bytes型在encode时会产生一定的区别，所以导致解密过程存在一定问题，还需要后续继续完善。<br>
SM2两方签名<br>
即不通过第三方进行密钥分发，只在A，B两方之间进行的签名。
![image](https://github.com/nadphwr/Practice/blob/main/sign.png)<br>
用python实现比特币并模拟交易<br>
实现思路和代码参考了https://link.zhihu.com/?target=http%3A//karpathy.github.io/2021/06/21/blockchain/
先生成原始地址和交易的目的地址<br>
![image](https://github.com/nadphwr/Practice/blob/main/bitcoin1.png)<br>
之后<br>
![image](https://github.com/nadphwr/Practice/blob/main/bitcoin2.png)<br>
之后通过网页https://kuttler.eu/en/bitcoin/btc/faucet/
获取虚拟比特币并进行交易<br>
![image](https://github.com/nadphwr/Practice/blob/main/模拟交易1.png)<br>
![image](https://github.com/nadphwr/Practice/blob/main/模拟交易2.png)<br>
默克尔树<br>
一个节点均由其子节点哈希而来。因此先建立几个高层节点，初始化为空，之后生成相应个数的底层节点，计算其哈希值，之后由下往上计算其父节点的哈希值，构造默克尔树。运行时无需额外输入，叶子节点均随机产生。<br>
![image](https://github.com/nadphwr/Practice/blob/main/merkeltree1.png)<br>
![image](https://github.com/nadphwr/Practice/blob/main/merkeltree2.png)<br>
![image](https://github.com/nadphwr/Practice/blob/main/merkeltree3.png)<br>
![image](https://github.com/nadphwr/Practice/blob/main/merkeltree4.png)<br>
ECDSA<br>
在以太坊中通常使用ECDSA签名来确保交易的正确性。ECDSA主要选择p-384曲线，即椭圆曲线参数a=-3.大致思路就是使用椭圆曲线ECC，其中参数p，a，b，生成素数阶n的循环群的点G。之后选择一个随机整数d作为私钥，之后计算B=dG作为公钥。签名时将私钥和消息进行签名，验证签名时用公钥，签名和消息进行验证。<br>
![image](https://github.com/nadphwr/Practice/blob/main/ecdsa.png)<br>
