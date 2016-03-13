# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 18:16:41 2016

@author: yiyuezhuo
"""

from parse4 import s_to_hs,parse_pair

def load_from_file(cls,fname):
    f=open(fname,'r')
    sl=f.read().split()
    f.close()
    return [s_to_hs(s) for s in sl]


at_escape=load_from_file('at_escape.txt')
builtin_escape=load_from_file('builtin_escape.txt')





f=open('Enemies.rvdata','rb')
b=f.read()
f.close()
hs=s_to_hs(b)

index=971
length=len(hs)
stack=[]

#state='root'



while index<length:
    if hs[index:index+4]==['6F','3B','00','1B']:
        new=[['6F','3B','00','1B']]
        stack.append(new)
        #state='root'
        index+=4
    elif hs[index]=='3B': # ;
        rd=parse_pair(hs,index)
        #stack[-1].append([rd['key'],rd['value']])
        stack[-1].append([int(rd['key'],16),rd['value']])
        index+=rd['diff']
    else:
        raise Exception
