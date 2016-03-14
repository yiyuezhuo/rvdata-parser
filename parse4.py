# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 12:10:43 2016

@author: yiyuezhuo
"""

'''
这里跳过头直接从第二行的o开始解析，绝对只限制在这个范围内，绝不再浪费时间在一般化
模型里
'''
def s_to_hs(s):
    hss=s.encode('hex').upper()
    rl=[]
    for i in range(len(hss)/2):
        rl.append(hss[i*2:(i+1)*2])
    return rl
    
def parse_i_tail(hs,index):
    # it parse content right on the "i"
    first=int(hs[index],16)
    if first==0:
        return 0,1
    elif not(first in [1,2,3,4]):
        return first-5,1
    else:
        sl=hs[index+1:index+1+first]
        sl.reverse()
        return int(''.join(sl),16),first+1
        
def parse_string_tail(hs,index):
    length,diff=parse_i_tail(hs,index)
    s=''.join(hs[index+diff:index+diff+length])
    return s.decode('hex'),diff+length
    
def parse_pairs_limit(hs,index,limit):
    index_origin=index
    value_l=[]
    for i in range(limit):
        rd=parse_pair(hs,index)
        value_l.append([int(rd['key'],16),rd['value']])
        index=index+rd['diff']
    return value_l,index-index_origin
    
def parse_o_limit(hs,index,limit):
    #解析平行的o,从o的下标开始
    value_l=[]
    diff_l=[]
    for i in range(limit):
        if hs[index:index+4]==['6F','3B','1B','0C']:
            value,diff=parse_pairs_limit(hs,index+4,7)
            value_l.append(value)
            diff_l.append(diff)
            index+=diff+4
        else:
            raise Exception('parse_o_limit')
    return value_l,sum(diff_l)+len(diff_l)*4
    
def parse_list(hs,index,key):
    if key=='07':
        return hs[index:index+87],87
    elif key=='1A':
        number,diff=parse_i_tail(hs,index+1)
        value_l,diffs=parse_o_limit(hs,index+2,number)
        return value_l,1+diff+diffs
        
def parse_o_as_value(hs,index,key):
    if key=='09':
        value,diff=parse_pairs_limit(hs,index+4,6)
        return value,diff+4
    elif key=='17':
        value,diff=parse_pairs_limit(hs,index+4,5)
        return value,diff+4
        

    

def parse_pair(hs,index):
    rd={'key':hs[index+1]}
    if hs[index+2]=='69':# i
        value,diff=parse_i_tail(hs,index+3)
        rd['value']=value
        rd['diff']=3+diff
    elif hs[index+2] in [s.encode('hex') for s in ['T','F','u']]:
        rd['value']=hs[index+2].decode('hex')
        rd['diff']=2+1
    elif hs[index+2]=='3B':
        rd['value']=hs[index+2:index+2+55]
        rd['diff']=2+55
    elif hs[index+2]=='5B':
        value,diff=parse_list(hs,index+2,hs[index+1])
        rd['value']=value
        rd['diff']=2+diff
    elif hs[index+2]=='6F':# o
        value,diff=parse_o_as_value(hs,index+2,hs[index+1])
        rd['value']=value
        rd['diff']=2+diff
    elif hs[index+2]=='22': #"
        value,diff=parse_string_tail(hs,index+3)
        rd['value']=value
        rd['diff']=3+diff
        #if rd['key']=='25':
        #    rd['diff']+=1
    elif hs[index+2:index+2+4]==['75','3B','07','3B']: # u ; . ;
        rd['value']=hs[index+2:index+2+58]
        rd['diff']=58
    else:
        raise Exception('do not parse as a pair')
    return rd
    
def parse(hs,index=971):
    length=len(hs)
    stack=[]
    
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
    # what happen 
    for record in stack:
        for i in record:
            if i[0]==9:
                record.extend(i[1])
                break
    return stack

def extract(stack):
    rank_map={20:'spirt',25:'def',24:'exp',34:'battler',
              36:'MP',38:'atk',16:'HP',8:'dex',41:'id',
              37:'des',17:'name'}
    rl=[]
    for record in stack:
        rd={}
        for var in record:
            if var[0] in rank_map.keys():
                rd[rank_map[var[0]]]=var[1]
        rl.append(rd)
    return rl
    
def extract_f(fname,index=971,raw=False):
    f=open(fname,'rb')
    b=f.read()
    f.close()
    hs=s_to_hs(b)
    stack=parse(hs,index=index)
    if raw:
        return stack
    else:
        return extract(stack)


'''
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
'''