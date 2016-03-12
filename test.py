# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 22:30:48 2016

@author: yiyuezhuo
"""

import struct
from collections import Counter

f=open('Enemies.rvdata','rb')
b=f.read()
f.close()
'''
dic=[[('name','jack'),('query','select'),('cost',10),('value',5)],
      ['lee','update',5,0],
        ['yiyuezhuo','insert',100,-3]]
        
import pickle
f=open('python_pickle','wb')
pickle.dump(dic,f)
f.close()

for i in range(3):
    f=open('python_pickle_'+str(i),'wb')
    pickle.dump(dic,f,protocol=i)
    f.close()

f=open('range100','wb')
pickle.dump(range(1000),f,protocol=2)
f.close()
'''

def show_hex(s,line_chars=16):
    s=s.encode('hex').upper()
    maxiter=len(s)/(line_chars*2)+1
    for i in range(maxiter):
        ss=s[i*32:(i+1)*32]
        sl=[]
        for j in range(line_chars):
            sl.append(ss[j:j+2])
        print ' '.join(sl)

print b.count('6F3B0A0A'.decode('hex'))

def parse_move_3A(s,index):
    assert s[index]==':'
    rl=[]
    while True:
        rl.append(index)
        diff=int(s[index+1].encode('hex'),16)
        if diff>16:
            diff-=1
        print 'detect',s[index+diff-1]
        print 'diff',diff
        print 'index',index
        if s[index+diff-1]!=':':
            return rl
        index=index+diff
        
def parse_i_tail(hs,index):
    # it parse content right on the "i"
    first=int(hs[index],16)
    if not(first in [1,2,3,4]):
        return first
    else:
        sl=hs[index+1:index+1+first]
        sl.reverse()
        return int(''.join(sl),16)
    
def parse_test(s):
    parse_move_3A(s,8*16+1)
    #return parse_move_3A(s,20)
    
def compare(s):
    s=s.encode('hex').upper()
    index_l=[]
    right_l=[]
    diff_l=[]
    for i in range(len(s)/2):
        char=s[2*i:2*(i+1)]
        if char=='3A':
            index_l.append(i)
            right_char=s[2*(i+1):2*(i+2)]
            right_l.append(int(right_char,16))
    for i in range(len(index_l)-1):
        diff_l.append(index_l[i+1]-index_l[i])
    return zip(index_l,right_l,diff_l)
    
def get_hs(s):
    hss=s.encode('hex').upper()
    rl=[]
    for i in range(len(hss)/2):
        rl.append(hss[i*2:(i+1)*2])
    return rl
    
def extract_string(s):
    hs=get_hs(s)
    cut_l=[]
    for index in range(len(hs)):
        char=hs[index]
        if char=='22':
            s_len=parse_i_tail(hs,index+1)
            cut_l.append((index,s_len))
    rl=[]
    for left,s_len in cut_l:
        hex_s=''.join(hs[left:left+s_len])
        rl.append(hex_s.decode('hex'))
    return rl
    
def count_semicolon_right(hs):
    sl=[]
    for index,char in enumerate(hs):
        if char=='3B':
            sl.append(int(hs[index+1],16))
    return Counter(sl)
    
