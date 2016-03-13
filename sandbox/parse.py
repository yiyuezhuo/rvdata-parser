# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 08:38:31 2016

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



class Pattern(object):
    def __init__(self,key):
        self.key=key
    def match(self,hs,index):
        return hs[index:index+len(self.key)]==self.key
    def do(self,hs,index,stack):
        pass
    
class Escape(Pattern):
    def do(self,hs,index,stack):
        stack[-1].append(self.key)
        return index+len(self.key)
    @classmethod
    def load_from_file(cls,fname):
        f=open(fname,'r')
        sl=f.read().split()
        f.close()
        return [cls(s_to_hs(s)) for s in sl]
        
class List(Pattern):
    '''[ Int'''
    def do(self,hs,index,stack):
        pass
        
        
#escape=Escape.load_from_file('at_escape.txt')+Escape.load_from_file('buildin_escape.txt')
txt_escape_path= ['at_escape.txt','buildin_escape.txt']
escape=sum([Escape.load_from_file(fname) for fname in txt_escape_path],[])
escape.append(Escape(['04','08']))
