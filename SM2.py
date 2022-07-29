# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 19:53:28 2022

@author: nadph
"""

'''SM2'''
import random
import time
import math
import numpy as np
from _sm3 import sm3
 
small_primes = np.array([2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41,
                         43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109,
                         113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191,
                         193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269,
                         271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353,
                         359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439,
                         443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523,
                         541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617,
                         619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709,
                         719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811,
                         821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907,
                         911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997])
 
 
def is_prime(num):
    if num < 2:
        return False
    for prime in small_primes:
        if num % prime == 0:
            return False
    return rabin_miller(num,10)
 
 
def rabin_miller(n,times):
    judge=0
    for j in range(times):
        a=random.randint(1,n-1)
        #print(a)
        N=n-1
        k=0
        while True:
            if N%2 !=0:
                m=N
                break
            N=N//2
            k+=1    
        b=pow(a,m,n)
        #print(b)
        flag=0
        if b%n==1:
            judge+=1
        else:
            for i in range(k):
                if b%n==n-1:
                    judge+=1
                    flag=1
                    break
                else:
                    b=pow(b,2,n)
            if flag==0:
                judge+=0
    if judge>=0.25*times:
        return True
    else:
        return False
 
# 将字节转换为int
def to_int(byte):
    return int.from_bytes(byte, byteorder='big')
 
# 转换为bytes
def to_byte(x, size=None):
    if isinstance(x, int):
        if size is None: 
            size = 0
            tmp = x >> 64
            while tmp:
                size += 8
                tmp >>= 64
            tmp = x >> (size << 3)
            while tmp:
                size += 1
                tmp >>= 8
        elif x >> (size << 3): 
            x &= (1 << (size << 3)) - 1
        return x.to_bytes(size, byteorder='big')
    elif isinstance(x, str):
        x = x.encode()
        if size != None and len(x) > size: 
        return x
    elif isinstance(x, bytes):
        if size != None and len(x) > size: 
            x = x[:size] 
        return x
    elif isinstance(x, tuple) and len(x) == 2 and type(x[0]) == type(x[1]) == int:
        return to_byte(x[0], size) + to_byte(x[1], size)
    return bytes(x)

# 将列表元素转换为bytes并连接
def join_bytes(data_list):
    return b''.join([to_byte(i) for i in data_list])

def gcd(a, b):
    return a if b == 0 else gcd(b, a % b)
 
# 求乘法逆元过程中的辅助递归函数
def get_(a, b):
    if b == 0:
        return 1, 0
    x1, y1 = get_(b, a % b)
    x, y = y1, x1 - a // b * y1
    return x, y
 
# 求乘法逆元
def get_inverse(a, p): 
    if gcd(a, p) == 1:
        x, y = get_(a, p)
        return x % p
    return 1
def get_cpu_time():
    return time.perf_counter()
 
# 密钥派生函数
def KDF(Z, klen):
    ksize = klen >> 3
    K = bytearray()
    for ct in range(1, math.ceil(ksize / HASH_SIZE) + 1):
        K+=bytearray(sm3(str(to_int(Z + to_byte(ct, 4)))).encode())
    return K[:ksize]
 
#比特位数
def get_bit_num(x):
    if isinstance(x, int):
        num = 0
        tmp = x >> 64
        while tmp:
            num += 64
            tmp >>= 64
        tmp = x >> num >> 8
        while tmp:
            num += 8
            tmp >>= 8
        x >>= num
        while x:
            num += 1
            x >>= 1
        return num
    elif isinstance(x, str):
        return len(x.encode()) << 3
    elif isinstance(x, bytes):
        return len(x) << 3
    return 0
 
'''引用代码'''
# 椭圆曲线密码类（实现一般的EC运算，不局限于SM2）
class ECC:
    def __init__(self, p, a, b, n, G, h=None):
        self.p = p
        self.a = a
        self.b = b
        self.n = n
        self.G = G
        if h:
            self.h = h
        self.O = (-1, -1)  # 定义仿射坐标下无穷远点（零点）
 
        # 预先计算Jacobian坐标两点相加时用到的常数
        self._2 = get_inverse(2, p)
        self.a_3 = (a + 3) % p
 
    # 椭圆曲线上两点相加（仿射坐标）
    # SM2第1部分 3.2.3.1
    # 仅提供一个参数时为相同坐标点相加
    def add(self, P1, P2=None):
        x1, y1 = P1
        if P2 is None or P1 == P2:  # 相同坐标点相加
            # 处理无穷远点
            if P1 == self.O:
                return self.O
            # 计算斜率k（k已不具备明确的几何意义）
            k = (3 * x1 * x1 + self.a) * get_inverse(2 * y1, self.p) % self.p
            # 计算目标点坐标
            x3 = (k * k - x1 - x1) % self.p
            y3 = (k * (x1 - x3) - y1) % self.p
        else:
            x2, y2 = P2
            # 处理无穷远点
            if P1 == self.O:
                return P2
            if P2 == self.O:
                return P1
            if x1 == x2:
                return self.O
            # 计算斜率k
            k = (y2 - y1) * get_inverse(x2 - x1, self.p) % self.p
            # 计算目标点坐标
            x3 = (k * k - x1 - x2) % self.p
            y3 = (k * (x1 - x3) - y1) % self.p
        return x3, y3
 
    # 椭圆曲线上的点乘运算（仿射坐标）
    def multiply(self, k, P):
        # 判断常数k的合理性
        assert type(k) is int and k >= 0, 'factor value error'
        # 处理无穷远点
        if k == 0 or P == self.O:
            return self.O
        if k == 1:
            return P
        elif k == 2:
            return self.add(P)
        elif k == 3:
            return self.add(P, self.add(P))
        elif k & 1 == 0:  # k/2 * P + k/2 * P
            return self.add(self.multiply(k >> 1, P))
        elif k & 1 == 1:  # P + k/2 * P + k/2 * P
            return self.add(P, self.add(self.multiply(k >> 1, P)))
 
    # 输入P，返回-P
    def minus(self, P):
        Q = list(P)
        Q[1] = -Q[1]
        return tuple(Q)
 
    # Jacobian加重射影坐标下两点相加
    # SM2第1部分 A.1.2.3.2
    # 输入点包含两项时为仿射坐标，三项为Jacobian加重射影坐标，两点坐标系可不同
    # 两点相同时省略第二个参数
    def Jacb_add(self, P1, P2=None):
        if P2 is None or P1 == P2:  # 相同点相加
            # 处理无穷远点
            if P1 == self.O:
                return self.O
 
            # 根据参数包含的项数判断坐标系（是仿射坐标则转Jacobian坐标）
            x1, y1, z1 = P1 if len(P1) == 3 else (*P1, 1)
 
            # t1 = 3 * x1**2 + self.a * pow(z1, 4, self.p)
            # t2 = 4 * x1 * y1**2
            # t3 = 8 * pow(y1, 4, self.p)
            # x3 = (t1**2 - 2 * t2) % self.p
            # y3 = (t1 * (t2 - x3) - t3) % self.p
            # z3 = 2 * y1 * z1 % self.p            
            z3 = (y1 * z1 << 1) % self.p
            if z3 == 0:  # 处理无穷远点
                return self.O
            T2 = y1 * y1 % self.p
            T4 = (T2 << 3) % self.p
            T5 = x1 * T4 % self.p
            T6 = z1 * z1 % self.p
            T1 = (x1 + T6) * (x1 - T6) * 3 % self.p
            T1 = (T1 + self.a_3 * T6 * T6) % self.p
            T3 = T1 * T1 % self.p
            T2 = T2 * T4 % self.p
            x3 = (T3 - T5) % self.p
            T4 = T5 + (T5 + self.p >> 1) - T3 if T5 & 1 else T5 + (T5 >> 1) - T3
            T1 = T1 * T4 % self.p
            y3 = (T1 - T2) % self.p
        else:  # 不同点相加
            # 处理无穷远点
            if P1 == self.O:
                return P2
            if P2 == self.O:
                return P1
 
            # 根据参数包含的项数判断坐标系（是仿射坐标则转Jacobian坐标）
            x1, y1, z1 = P1 if len(P1) == 3 else (*P1, 1)
            x2, y2, z2 = P2 if len(P2) == 3 else (*P2, 1)
 
            if z2 != 1 and z1 != 1:
                z1_2 = z1 * z1 % self.p
                z2_2 = z2 * z2 % self.p
                t1 = x1 * z2_2 % self.p
                t2 = x2 * z1_2 % self.p
                t3 = t1 - t2
                z3 = z1 * z2 * t3 % self.p
                if z3 == 0:  # 处理无穷远点
                    return self.O
                t4 = y1 * z2 * z2_2 % self.p
                t5 = y2 * z1 * z1_2 % self.p
                t6 = t4 - t5
                t7 = t1 + t2
                t8 = t4 + t5
                t3_2 = t3 * t3 % self.p
                x3 = (t6 * t6 - t7 * t3_2) % self.p
                t9 = (t7 * t3_2 - (x3 << 1)) % self.p
                y3 = (t9 * t6 - t8 * t3 * t3_2) * self._2 % self.p
            else:  # 可简化计算
                if z1 == 1:  # 确保第二个点的z1=1
                    x1, y1, z1, x2, y2 = x2, y2, z2, x1, y1
                T1 = z1 * z1 % self.p
                T2 = y2 * z1 % self.p
                T3 = x2 * T1 % self.p
                T1 = T1 * T2 % self.p
                T2 = T3 - x1
                z3 = z1 * T2 % self.p
                if z3 == 0:  # 处理无穷远点
                    return self.O
                T3 = T3 + x1
                T1 = T1 - y1
                T4 = T2 * T2 % self.p
                T5 = T1 * T1 % self.p
                T2 = T2 * T4 % self.p
                T3 = T3 * T4 % self.p
                T4 = x1 * T4 % self.p
                x3 = T5 - T3 % self.p
                T2 = y1 * T2 % self.p
                T3 = T4 - x3
                T1 = T1 * T3 % self.p
                y3 = T1 - T2 % self.p
                # T1 = z1 * z1 % self.p
                # T3 = x2 * T1 % self.p
                # T2 = T3 - x1
                # z3 = z1 * T2 % self.p
                # if z3 == 0: # 处理无穷远点
                # return self.O
                # T1 = (T1 * y2 * z1  - y1) % self.p
                # T4 = T2 * T2 % self.p
                # x3 = T1 * T1 - (T3 + x1) * T4 % self.p
                # T1 = T1 * (x1 * T4 - x3) % self.p
                # y3 = T1 - y1 * T2 * T4 % self.p
 
        return x3, y3, z3
 
    # Jacobian加重射影坐标下的点乘运算
    # SM2第1部分 A.3
    # 输入点包含两项时为仿射坐标，三项为Jacobian坐标
    # conv=True时结果转换为仿射坐标，否则不转换
    # algo表示选择的算法， r表示算法三（滑动窗法）的窗口值
    def Jacb_multiply(self, k, P, conv=True, algo=2, r=5):
        # 处理无穷远点
        if k == 0 or P == self.O:
            return self.O
 
        # 仿射坐标转Jacobian坐标
        # if len(P) == 2: 
        # P = (*P, 1)
 
        # 算法一：二进制展开法
        if algo == 1:
            Q = P
            for i in bin(k)[3:]:
                Q = self.Jacb_add(Q)
                if i == '1':
                    Q = self.Jacb_add(Q, P)
 
        # 算法二：加减法
        elif algo == 2:
            h = bin(3 * k)[2:]
            k = bin(k)[2:]
            k = '0' * (len(h) - len(k)) + k
            Q = P
            minusP = self.minus(P)
            for i in range(1, len(h) - 1):
                Q = self.Jacb_add(Q)
                if h[i] == '1' and k[i] == '0':
                    Q = self.Jacb_add(Q, P)
                elif h[i] == '0' and k[i] == '1':
                    Q = self.Jacb_add(Q, minusP)
 
        # 算法三：滑动窗法
        # 当k为255/256位时，通过test_r函数测试，r=5复杂度最低
        elif algo == 3:
            k = bin(k)[2:]
            l = len(k)
            if r >= l:  # 如果窗口大于k的二进制位数，则本算法无意义
                return self.Jacb_multiply(int(k, 2), P, conv, 2)
 
            # 保存P[j]值的字典
            P_ = {1: P, 2: self.Jacb_add(P)}
            for i in range(1, 1 << (r - 1)):
                P_[(i << 1) + 1] = self.Jacb_add(P_[(i << 1) - 1], P_[2])
 
            t = r
            while k[t - 1] != '1':
                t -= 1
            hj = int(k[:t], 2)
            Q = P_[hj]
            j = t
            while j < l:
                if k[j] == '0':
                    Q = self.Jacb_add(Q)
                    j += 1
                else:
                    t = min(r, l - j)
                    while k[j + t - 1] != '1':
                        t -= 1
                    hj = int(k[j:j + t], 2)
                    Q = self.Jacb_add(self.Jacb_multiply(1 << t, Q, False, 2), P_[hj])
                    j += t
 
        return self.Jacb_to_affine(Q) if conv else Q
 
    # Jacobian加重射影坐标转仿射坐标
    # SM2第1部分 A.1.2.3.2
    def Jacb_to_affine(self, P):
        if len(P) == 2:  # 已经是仿射坐标
            return P
        x, y, z = P
        # 处理无穷远点
        if z == 0:
            return self.O
        z_ = get_inverse(z, self.p)  # z的乘法逆元
        x2 = x * z_ * z_ % self.p
        y2 = y * z_ * z_ * z_ % self.p
        return x2, y2
 
    # 判断是否为无穷远点（零点）
    def is_zero(self, P):
        if len(P) == 2:  # 仿射坐标
            return P == self.O
        else:  # Jacobian加重射影坐标
            return P[2] == 0
 
    # 判断是否为域Fp中的元素
    # 可输入多个元素，全符合才返回True
    def on_Fp(self, *x):
        for i in x:
            if 0 <= i < self.p:
                pass
            else:
                return False
        return True
 
    # 判断是否在椭圆曲线上
    def on_curve(self, P):
        if self.is_zero(P):
            return False
        if len(P) == 2:  # 仿射坐标
            x, y = P
            return y * y % self.p == (x * x * x + self.a * x + self.b) % self.p
        else:  # Jacobian加重射影坐标
            x, y, z = P
            return y * y % self.p == (x * x * x + self.a * x * pow(z, 4, self.p) + self.b * pow(z, 6, self.p)) % self.p
 
    # 生成密钥对
    # 返回值：d为私钥，P为公钥
    # SM2第1部分 6.1
    def gen_keypair(self):
        d = random.randint(1, self.n - 2)
        P = self.Jacb_multiply(d, self.G)
        return d, P
 
    # 公钥验证
    # SM2第1部分 6.2.1
    def pk_valid(self, P):
        # 判断点P的格式
        if P and len(P) == 2 and type(P[0]) == type(P[1]) == int:
            pass
        else:
            self.error = '格式有误'  # 记录错误信息
            return False
        # a) 验证P不是无穷远点O
        if self.is_zero(P):
            self.error = '无穷远点'
            return False
        # b) 验证公钥P的坐标xP和yP是域Fp中的元素
        if not self.on_Fp(*P):
            self.error = '坐标值不是域Fp中的元素'
            return False
        # c) 验证y^2 = x^3 + ax + b (mod p)
        if not self.on_curve(P):
            self.error = '不在椭圆曲线上'
            return False
        # d) 验证[n]P = O
        if not self.is_zero(self.Jacb_multiply(self.n, P, False)):
            self.error = '[n]P不是无穷远点'
            return False
        return True
 
    # 确认目前已有公私钥对
    def confirm_keypair(self):
        if not hasattr(self, 'pk') or not self.pk_valid(self.pk) or self.pk != self.Jacb_multiply(self.sk, self.G):
            # 目前没有合格的公私钥对则生成
            while True:
                d, P = self.gen_keypair()
                if self.pk_valid(P):  # 确保公钥通过验证
                    self.sk, self.pk = d, P
                    return
 
 
# 国家密码管理局：SM2椭圆曲线公钥密码算法推荐曲线参数
SM2_p = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFF
SM2_a = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF00000000FFFFFFFFFFFFFFFC
SM2_b = 0x28E9FA9E9D9F5E344D5A9E4BCF6509A7F39789F515AB8F92DDBCBD414D940E93
SM2_n = 0xFFFFFFFEFFFFFFFFFFFFFFFFFFFFFFFF7203DF6B21C6052B53BBF40939D54123
SM2_Gx = 0x32C4AE2C1F1981195F9904466A39C9948FE30BBFF2660BE1715A4589334C74C7
SM2_Gy = 0xBC3736A2F4F6779C59BDCEE36B692153D0A9877CC62A474002DF32E52139F0A0
SM2_G=(SM2_Gx,SM2_Gy)
h=1
PARA_SIZE = 32  # 参数长度（字节）
HASH_SIZE = 32  # sm3输出256位（32字节）
KEY_LEN = 128  # 默认密钥位数
 
# SM2示例中的椭圆曲线系统参数
def tmp_para():
    p = 0x8542D69E4C044F18E8B92435BF6FF7DE457283915C45517D722EDB8B08F1DFC3
    a = 0x787968B4FA32C3FD2417842E73BBFEFF2F3C848B6831D7E0EC65228B3937E498
    b = 0x63E4C6D3B23B0C849CF84241484BFE48F61D59A5B16BA06E6E12D1DA27C5249A
    xG = 0x421DEBD61B62EAB6746434EBC3CC315E32220B3BADD50BDC4C4E6C147FEDD43D
    yG = 0x0680512BCBB42C07D47349D2153B70C4E5D7FDFCBFA36EA1A85841B9E46E09A2
    n = 0x8542D69E4C044F18E8B92435BF6FF7DD297720630485628D5AE74EE7C32E79B7
    G = (xG, yG)
    h = 1
    return p, a, b, n, G, h

# SM2类继承ECC(参考代码）
class SM2(ECC):
    def __init__(self, p=SM2_p, a=SM2_a, b=SM2_b, n=SM2_n, G=(SM2_Gx, SM2_Gy), h=None,
                 ID=None, sk=None, pk=None, genkeypair=True):  # genkeypair表示是否自动生成公私钥对
        if not h:  # 余因子h默认为1
            h = 1
        ECC.__init__(self, p, a, b, n, G, h)
        self.keysize = len(to_byte(n))  # 密钥长度（字节）
        if type(ID) in (int, str):  # 身份ID（数字或字符串）
            self.ID = ID
        else:
            self.ID = ''
        if sk and pk:  # 如果提供的公私钥对通过验证，即使genkeypair=True也不会重新生成
            self.sk = sk  # 私钥（int [1,n-2]）
            self.pk = pk  # 公钥（x, y）
            self.confirm_keypair()  # 验证该公私钥对，不合格则生成
        elif genkeypair:  # 自动生成合格的公私钥对
            self.confirm_keypair()
        if hasattr(self, 'sk'):  # 签名时
            self.d_1 = get_inverse(1 + self.sk, self.n)
    def para_valid(self):
        # a) 验证q = p是奇素数
        if not is_prime(self.p):
            self.error = 'p不是素数'  # 记录错误信息
            return False
        # b) 验证a、b、Gx和Gy是区间[0, p−1]中的整数
        if not self.on_Fp(self.a, self.b, *self.G):
            self.error = 'a、b或G坐标值不是域Fp中的元素'
            return False
        # d) 验证(4a^3 + 27b^2) mod p != 0
        if (4 * self.a * self.a * self.a + 27 * self.b * self.b) % self.p == 0:
            self.error = '(4a^3 + 27b^2) mod p = 0'
            return False
        # e) 验证Gy^2 = Gx^3 + aGx + b (mod p)
        if not self.on_curve(self.G):
            self.error = 'G不在椭圆曲线上'
            return False
        # f) 验证n是素数，n > 2^191 且 n > 4p^1/2
        if not is_prime(self.n) or self.n <= 1 << 191 or self.n <= 4 * self.p ** 0.5:
            self.error = 'n不是素数或n不够大'
            return False
        # g) 验证[n]G = O
        if not self.is_zero(self.Jacb_multiply(self.n, self.G, False)):
            self.error = '[n]G不是无穷远点'
            return False
        # i) 验证抗MOV攻击条件和抗异常曲线攻击条件成立（A.4.2.1）
        B = 27  # MOV阈B
        t = 1
        for i in range(B):
            t = t * self.p % self.n
            if t == 1:
                self.error = '不满足抗MOV攻击条件'
                return False
        # 椭圆曲线的阶N=#E(Fp)计算太复杂，未实现A.4.2.2验证
        # Fp上的绝大多数椭圆曲线确实满足抗异常曲线攻击条件
        return True
 
    # 计算Z
    # SM2第2部分 5.5
    # ID为数字或字符串，P为公钥（不提供参数时返回自身Z值）
    def get_Z(self, ID=None, P=None):
        save = False
        if not P:  # 不提供参数
            if hasattr(self, 'Z'):  # 再次计算，返回曾计算好的自身Z值
                return self.Z
            else:  # 首次计算自身Z值
                ID = self.ID
                P = self.pk
                save = True
        entlen = get_bit_num(ID)
        ENTL = to_byte(entlen, 2)
        Z = sm3(str(to_int(join_bytes([ENTL, ID, self.a, self.b, *self.G, *P]))))
        if save:  # 保存自身Z值
            self.Z = Z

          
          
          
          
    def encrypt(self, M, PB, k=None):
        if self.is_zero(self.multiply(self.h, PB)):  # S
            return False, 'S是无穷远点'
        M = to_byte(M)
        klen = get_bit_num(M)
        while True:
            if not k:
                k = random.randint(1, self.n - 1)
            # x2, y2 = self.multiply(k, PB)
            x2, y2 = self.Jacb_multiply(k, PB)
            t = to_int(KDF(join_bytes([x2, y2]), klen))
            if t == 0: 
                k = 0
            else:
                break
        # C1 = to_byte(self.multiply(k, self.G), self.keysize) # (x1, y1)
        C1 = to_byte(self.Jacb_multiply(k, self.G), self.keysize)  # (x1, y1)
        C2 = to_byte(to_int(M) ^ t, klen >> 3)
        C3 = sm3(str(to_int(join_bytes([x2, M, y2]))))
        return True, join_bytes([C1, C2, C3])

    def decrypt(self, C):
        x1 = to_int(C[:self.keysize])
        y1 = to_int(C[self.keysize:self.keysize << 1])
        C1 = (x1, y1)
        if not self.on_curve(C1):
            return False,'failed'
        if self.is_zero(self.multiply(self.h, C1)):  # S
            return False,'failed'
        # x2, y2 = self.multiply(self.sk, C1)
        x2, y2 = self.Jacb_multiply(self.sk, C1)
        klen = len(C) - (self.keysize << 1) - HASH_SIZE << 3
        t = to_int(KDF(join_bytes([x2, y2]), klen))
        if t == 0:
            return False,'failed'
        C2 = C[self.keysize << 1:-HASH_SIZE]
        M = to_byte(to_int(C2) ^ t, klen >> 3)
        u = sm3(str(to_int(join_bytes([x2, M, y2]))))
        C3 = C[-HASH_SIZE:]
        if u != C3:
            return False,'failed'
        return True, M
def test_encryption():
    M = 'encryption standard'
    dB = 0x1649AB77A00637BD5E2EFE283FBF353534AA7F7CB89463F208DDBC2920BB0DA0
    xB = 0x435B39CCA8F3B508C1488AFC67BE491A0F7BA07E581A0E4849A5CF70628A7E0A
    yB = 0x75DDBA78F15FEECB4C7895E2C1CDF5FE01DEBB2CDBADF45399CCF77BBA076A42
    PB = (xB, yB)
    k = 0x4C62EEFD6ECFC2B95B92FD6C3D9575148AFA17425546D49018E5388D49DD7B4F
    sm2_A = SM2(*tmp_para())
    sm2_B = SM2(*tmp_para(), '', dB, PB)
    time_1 = get_cpu_time()
    res, C = sm2_A.encrypt(M, PB, k)
    if not res:
        print('错误：', C)
        return
    res, M2 = sm2_B.decrypt(C)
    if not res:
        print('错误：', M2)
        return
    time_2 = get_cpu_time()
    print('耗时%.2f ms' % ((time_2 - time_1) * 1000))
    print('结果：%s，解密得：%s(%s)' % (res, M2.hex(), M2.decode()))
 
if __name__ == "__main__":
    test_encryption()
