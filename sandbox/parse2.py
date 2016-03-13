# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 10:36:50 2016

@author: yiyuezhuo
"""


def s_to_hs(s):
    hss=s.encode('hex').upper()
    rl=[]
    for i in range(len(hss)/2):
        rl.append(hss[i*2:(i+1)*2])
    return rl
    
def hs_to_s(hs):
    s=''.join(hs)
    s=s.decode('hex')
    return s
    
def parse_i_tail(hs,index):
    # it parse content right on the "i"
    first=int(hs[index],16)
    if not(first in [1,2,3,4]):
        return first
    else:
        sl=hs[index+1:index+1+first]
        sl.reverse()
        return int(''.join(sl),16)

def load_from_file(cls,fname):
    f=open(fname,'r')
    sl=f.read().split()
    f.close()
    return [s_to_hs(s) for s in sl]
    
def key_match(key,hs,index):
    return key==hs[index:index+len(key)]
def keys_match(keys,hs,index):
    for key in keysL:
        if key_match(key,hs,index):
            return key
    return None
    


at_escape=load_from_file('at_escape.txt')
builtin_escape=load_from_file('builtin_escape.txt')

escape=at_escape+[['04','08']]

f=open('Enemies.rvdata','rb')
b=f.read()
f.close()
hs=s_to_hs(b)

index=0
root={'list':[]}
stack=[root]
while index<len(hs):
    char=hs[index]
    escape_key=keys_match(escape,hs,index)
    if escape_key:
        index+=len(escape_key)
        continue
    builtin_key=keys_match(builtin_escape,hs,index)
    if builtin_key:
        pair={'type':builtin_key,'value':None}
        stack[-1]['list'].append(pair)
        stack.append(pair)
    if char=='['.encode('hex'):
        new={'list':[],'type':hs[index:index+3]}
        stack[-1]['list'].append(new)
        stack.append(new)
        index+=3
        continue
    if char=='o'.encode('hex'):
        if hs[index+1]==';'.encode('hex'):
            new={'type':hs[index:index+3]}
            
    
    raise Exception('unhandle error')
        
