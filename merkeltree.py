# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 19:12:21 2022

@author: nadph
"""

'''merkel tree'''
import math
import random
import hashlib
def make_data(x):
    if x>6 and x<15:
        raw_str="readytocreateanode54321"
        nums=math.floor(1e5*random.random())
        nums=str(nums)
        nums=nums.zfill(5)
        end_str=raw_str+nums
        print(end_str)
        return end_str
    elif x>=0 and x<7:
        return None
    else:
        return -1

class Node:
    def __init__(self,name):
        self.name=name
        self.child1=None
        self.child2=None
        self.hash=None
        self.data=None
    def upd_data(self,data):
        self.data=data
        self.hash=hashlib.md5(data.encode('utf-8')).hexdigest()[8:-8]
        print(self.hash)
        return self.hash
        
class Tree:
    def __init__(self):
        self.root=None
    def add_node(self,name):
        new_node=Node(name)
        end_str=make_data(name)
        print("new node is:",name)
        if end_str!=None and end_str!=-1:
            new_node.upd_data(end_str)
            print("new node's data is:",new_node.data)
            print("new node's hash is:",new_node.hash)
        if self.root==None:
            self.root=new_node
        else:
            tmp_node_lst=[self.root]
            while True:
                pop_node=tmp_node_lst.pop(0)
                if pop_node.child1==None:
                    pop_node.child1=new_node
                    return
                elif pop_node.child2==None:
                    pop_node.child2=new_node
                    return
                else:
                    tmp_node_lst.append(pop_node.child1)
                    tmp_node_lst.append(pop_node.child2)
    def upd_hash(self):
        if self.root==None:
            return None
        tmp_node_lst=[self.root]
        lst_item=[(self.root.name,self.root.data,self.root.hash)]
        while len(tmp_node_lst)!=0:
            pop_node=tmp_node_lst.pop(0)
            if pop_node.child1!=None and pop_node.child2!=None:
                if pop_node.child1.hash!=None and pop_node.child2.hash!=None:
                    print("update the nodes:",pop_node.name)
                    end_str=pop_node.child1.hash+pop_node.child2.hash
                    end_hash=pop_node.upd_data(end_str)
                    print(end_hash)
            if pop_node.child1!=None:
                tmp_node_lst.append(pop_node.child1)
            if pop_node.child2!=None:
                tmp_node_lst.append(pop_node.child2)
        return
    def traverse(self):
        if self.root==None:
            return None
        tmp_node_lst=[self.root]
        lst_item=[(self.root.name,self.root.data,self.root.hash)]
        while len(tmp_node_lst)!=0:
            pop_node=tmp_node_lst.pop(0)
            if pop_node.child1!=None:
                tmp_node_lst.append(pop_node.child1)
                lst_item.append((pop_node.child1.name,pop_node.child1.data,pop_node.child1.hash))
            if pop_node.child2!=None:
                tmp_node_lst.append(pop_node.child2)
                lst_item.append((pop_node.child2.name,pop_node.child2.data,pop_node.child2.hash))
        return lst_item
    
if __name__=='__main__':
    t=Tree()
    for i in range(7):
        t.add_node(i)
    for i in range(7,15):
        t.add_node(i)
    for i in range(4,0,-1):
        print("第",i,"层节点")
        print(t.upd_hash())
print(t.traverse())