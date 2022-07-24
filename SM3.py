# -*- coding: utf-8 -*-
"""
Created on Thu Jul 14 19:17:35 2022

@author: nadph
"""

'''SM3'''
import copy

IV='7380166f4914b2b9172442d7da8a0600a96f30bc163138aae38dee4db0fb0e4e'
T_j_0_15='0x79cc4519'
T_j_16_63='0x7a879d8a'

def FFj(x,y,z,j):
    result=[]
    x=bin(int(x,16)).replace('0b','').zfill(32)
    y=bin(int(y,16)).replace('0b','').zfill(32)
    z=bin(int(z,16)).replace('0b','').zfill(32)
    print(x)
    if j>=0 and j<=15:
        for i in range(32):
            result.append(int(x[i])^int(y[i])^int(z[i]))
        return ''.join('%s' %id for id in result)
    if j>=16 and j<=63:
        for i in range(32):
            result.append((x[i] and y[i])or(x[i] and z[i])or(y[i] and z[i]))
        return ''.join('%s' %id for id in result)

def GGj(x,y,z,j):
    result=[]
    x=bin(int(x,16)).replace('0b','').zfill(32)
    y=bin(int(y,16)).replace('0b','').zfill(32)
    z=bin(int(z,16)).replace('0b','').zfill(32)
    if j>=0 and j<=15:
        for i in range(32):
            result.append(int(x[i])^int(y[i])^int(z[i]))
        return ''.join('%s' %id for id in result)
    if j>=16 and j<=63:
        for i in range(32):
            result.append((x[i] and y[i])or(not x[i] and z[i]))
        return ''.join('%s' %id for id in result)

def sm3_fill(m):
    len_m=len(m)
    k=0
    while True:
        if (len_m+1+k)%512==448:
            break
        k=k+1
    m=m+'1'
    for i in range(k):
        m=m+'0'
    lenm=list(bin(len_m))
    lenm[:2]=['0','0']
    lenm=''.join(lenm)
    tempm=''
    for i in range(64-len(lenm)):
        tempm=tempm+'0'
    m=m+tempm+lenm
    return m

def sm3_spilt(m):
    l=len(m)//512
    print(len(m))
    B_list=[]
    for j in range(l):
        B_list.append(m[0+j*512:512+j*512])
        #print(B_list)
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
            temp_wj.append(int(W_j[i-16][j])^int(W_j[i-9][j]))
        temp_wj0=bin(int(W_j[i-3],2)<<15).replace('0b','')
        if len(temp_wj0)<=32:
            temp_wj0=temp_wj0.zfill(32)
        else:
            temp_wj0=temp_wj0[len(temp_wj0)-32:]
            
        for j in range(32):
            temp_wj[j]=temp_wj[j]^int(temp_wj0[j])
            
        tmp_15=bin(int(''.join('%s' %id for id in temp_wj),2)<<15).replace('0b','')
        if len(tmp_15)<=32:
            tmp_15=tmp_15.zfill(32)
        else:
            tmp_15=tmp_15[len(tmp_15)-32:]
            
        tmp_23=bin(int(''.join('%s' %id for id in temp_wj),2)<<23).replace('0b','')
        if len(tmp_23)<=32:
            tmp_23=tmp_23.zfill(32)
        else:
            tmp_23=tmp_23[len(tmp_23)-32:]
            
        for j in range(32):
            temp_wj[j]=int(tmp_15[j])^int(temp_wj[j])^int(tmp_23[j])
            
        tmp_13=bin(int(W_j[i-13],2)<<7).replace('0b','')
        if len(tmp_13)<=32:
            tmp_13=tmp_13.zfill(32)
        else:
            tmp_13=tmp_13[len(tmp_13)-32:]
            
        for j in range(32):
            temp_wj[j]=int(temp_wj[j])^int(tmp_13[j])^int(W_j[i-6][j])
        W_j.append(''.join('%s' %id for id in temp_wj))
    for i in range(0,64):
        temp_wjp=[]
        for j in range(32):
            temp_wjp.append(int(W_j[i][j])^int(W_j[i+4][j]))
        W_jp.append(''.join('%s' %id for id in temp_wjp))
    return W_j,W_jp

def sm3_CF(V,B,Wj,Wjp,j):
    A=V[:8]
    B=V[8:16]
    C=V[16:24]
    D=V[24:32]
    E=V[32:40]
    F=V[40:48]
    G=V[48:56]
    H=V[56:64]
    print("A:",A)
    print("B:",B)
    print("C:",C)
    print("D:",D)
    print("E:",E)
    print("F:",F)
    print("G:",G)
    print("H:",H)
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
        
        SS1=bin(int(bin(int(tmp_A,2)+int(E,16)+int(tmp_T,2)).replace('0b',''),2)<<7).replace('0b','')
        print(SS1)
        SS2=[]
        for i in range(len(A)):
            SS2.append(int(SS1[i])^int(tmp_cpA[i]))
        SS2=''.join('%s' %id for id in SS2)
        TT1=bin(int(FFj(A,B,C,j),2)+int(D,16)+int(SS2,2)+int(Wjp[j],2)).replace('0b','').zfill(32)
        TT2=bin(int(GGj(E,F,G,j),2)+int(H,16)+int(SS1,2)+int(Wj[j],2)).replace('0b','').zfill(32)
        D=C
        C=bin(int(bin(int(B,16)),2)<<9).replace('0b','')
        B=A
        A=TT1
        H=G
        G=bin(int(bin(int(F,16)),2)<<19).replace('0b','')
        F=E
        tmp_tt2=bin(int(bin(int(TT2,2)),2)<<9).replace('0b','')
        tmp1_tt2=bin(int(bin(int(TT2,2)),2)<<17).replace('0b','')
        TT2=list(TT2)
        print(TT2)
        for i in range(32):
            TT2[i]=int(TT2[i])^int(tmp_tt2[i])^int(tmp1_tt2[i])
        E=TT2
    register=A+B+C+D+E+F+G
    Vi=[]
    for i in range(256):
        Vi.append(register[i]^V[i])
    return ''.join(Vi)

plaintext=input("please input the plaintext:")
plaintext=sm3_fill(plaintext)
print(plaintext)
lstB=sm3_spilt(plaintext)
print(lstB)
W,W_0=sm3_extend(lstB)
#print(W)
#print(W_0)
V=[IV]
for i in range(64):
    V.append(sm3_CF(V[i], lstB[i], W[i], W_0[i],i))
print(V)


#brithday attack
#随机选取一个massage计算其tag，之后从消息空间中寻找碰撞
#生成消息空间
