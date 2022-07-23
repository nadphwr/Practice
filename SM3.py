# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 19:17:35 2022

@author: nadph
"""

'''SM3'''
import copy

IV='0x7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
T_j_0_15='0x79cc4519'
T_j_16_63='0x7a879d8a'

def FFj(x,y,z,j):
    result=[]
    if j>=0 and j<=15:
        for i in range(32):
            result.append(x[i]^y[i]^z[i])
        return ''.join(result)
    if j>=16 and j<=63:
        for i in range(32):
            result.append((x[i] and y[i])or(x[i] and z[i])or(y[i] and z[i]))
        return ''.join(result)

def GGj(x,y,z,j):
    result=[]
    if j>=0 and j<=15:
        for i in range(32):
            result.append(x[i]^y[i]^z[i])
        return ''.join(result)
    if j>=16 and j<=63:
        for i in range(32):
            result.append((x[i] and y[i])or(not x[i] and z[i]))
        return ''.join(result)

def sm3_fill(m):
    len_m=len(m)
    k=0
    while True:
        if (len_m+1+k)%512==418:
            break
        k=k+1
    m=m+'1'
    for i in range(k):
        m=m+'0'
    lenm=bin(len_m)
    lenm[:2]='00'
    tempm=''
    for i in range(64-len(lenm)):
        tempm=tempm+'0'
    m=tempm+lenm
    return m

def sm3_spilt(m):
    l=len(m)//512
    B_list=[]
    for j in range(l):
        B_list.append(m[0+j*512:512+j*512])
    return B_list

def sm3_extend(B):
    B_1=B[0]
    lst_b=[]
    for i in range(16):
        lst_b.append(B_1[0+i*32:32+i*32])
    W_j=[]
    W_jp=[]
    for i in range(16):
        W_j.append(lst_b[i])
    for i in range(16,68):
        temp_wj=[]
        for j in range(32):#按位异或
            temp_wj.append(W_j[i-16][j]^W_j[i-9][j])
        temp_wj0=bin(int(W_j[i-3],2)<<15).replace('0b','')
        if len(temp_wj0)<=32:
            temp_wj0=temp_wj0.zfill(32)
        else:
            temp_wj0=temp_wj0[len(temp_wj0)-32:]
            
        for j in range(32):
            temp_wj[j]=temp_wj[j]^temp_wj0[j]
            
        tmp_15=bin(int(''.join(temp_wj),2)<<15).replace('0b','')
        if len(tmp_15)<=32:
            tmp_15=tmp_15.zfill(32)
        else:
            tmp_15=tmp_15[len(tmp_15)-32:]
            
        tmp_23=bin(int(''.join(temp_wj),2)<<23).replace('0b','')
        if len(tmp_23)<=32:
            tmp_23=tmp_23.zfill(32)
        else:
            tmp_23=tmp_23[len(tmp_23)-32:]
            
        for j in range(32):
            temp_wj[j]=tmp_15[j]^temp_wj[j]^tmp_23[j]
            
        tmp_13=bin(int(W_j[i-13],2)<<7).replace('0b','')
        if len(tmp_13)<=32:
            tmp_13=tmp_13.zfill(32)
        else:
            tmp_13=tmp_13[len(tmp_13)-32:]
            
        for j in range(32):
            temp_wj[j]=temp_wj[j]^tmp_13[j]^W_j[i-6][j]
        W_j.append(''.join(temp_wj))
    for i in range(0,64):
        temp_wjp=[]
        for j in range(32):
            temp_wjp.append(W_j[i][j]^W_j[i+4][j])
        W_jp.append(''.join(temp_wjp))
    return W_j,W_jp

def sm3_CF(V,B,Wj,Wjp):
    A=V[:8]
    B=V[8:16]
    C=V[16:24]
    D=V[24:32]
    E=V[32:40]
    F=V[40:48]
    G=V[48:56]
    H=V[56:64]
    for j in range(64):
        tmp_A=bin(int(bin(int(''.join(A),16)),2)<<12).replace('0b','')
        tmp_cpA=copy.copy(tmp_A)
        if len(tmp_A)<=32:
            tmp_A=tmp_A.zfill(32)
        else:
            tmp_A=tmp_A[len(tmp_A)-32:]
            
        if j>=0 and j<=15:
            tmp_T=bin(int(bin(int(T_j_0_15,16)),2)<<j).replace('0b','')
        if len(tmp_T)<=32:
            tmp_T=tmp_T.zfill(32)
        else:
            tmp_T=tmp_T[len(tmp_T)-32:]
        if j>=16 and j<=63:
            tmp_T=bin(int(bin(int(T_j_16_63,16)),2)<<j).replace('0b','')
        if len(tmp_T)<=32:
            tmp_T=tmp_T.zfill(32)
        else:
            tmp_T=tmp_T[len(tmp_T)-32:]
        
        SS1=bin(int(bin(int(tmp_A,2)+int(E,16)+int(tmp_T,2)),2)<<7)
        SS2=[]
        for i in range(len(A)):
            SS2.append(SS1[i]^tmp_cpA[i])
        SS2=''.join(SS2)
        TT1=bin(int(FFj(A,B,C),2)+int(D,16)+int(SS2,2)+int(Wjp[j],2))
        TT2=bin(int(GGj(E,F,G),2)+int(H,16)+int(SS1,2)+int(Wj[j],2))
        D=C
        C=B<<9
        B=A
        A=TT1
        H=G
        G=F<<19
        F=E
        tmp_tt2=TT2<<9
        tmp1_tt2=TT2<<17
        for i in range(32):
            TT2[i]=TT2[i]^tmp_tt2[i]^tmp1_tt2[i]
        E=TT2
    register=A+B+C+D+E+F+G
    Vi=[]
    for i in range(256):
        Vi.append(register[i]^V[i])
    return ''.join(Vi)

plaintext=input("please input the plaintext:")
plaintext=sm3_fill(plaintext)
lstB=sm3_spilt(plaintext)
W,W_0=sm3_extend(lstB)
V=[IV]
for i in range(64):
    V.append(sm3_CF(V[i], lstB[i], W[i], W_0[i]))
print(V)


#brithday attack
#随机选取一个massage计算其tag，之后从消息空间中寻找碰撞
#生成消息空间
