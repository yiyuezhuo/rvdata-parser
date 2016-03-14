# -*- coding: utf-8 -*-
"""
Created on Mon Mar 14 17:09:03 2016

@author: yiyuezhuo
"""

from parse4 import extract_f
import os
from PIL import Image, ImageDraw, ImageFont

class Block(object):
    def __init__(self,left_border=0,right_border=0,top_border=0,bottom_border=0,
                 align='left',extend=False):
        #TODO align,extend is not avaiable
        self.left_border=left_border
        self.right_border=right_border
        self.top_border=top_border
        self.bottom_border=bottom_border
        self.align=align
        self.extend=extend
    def plot(self,im,left,top,width,height):
        self.draw(im,left+self.left_border,top+self.top_border,
                  width-self.right_border,height-self.bottom_border)
    def draw(self,im,left,top,width,height):
        pass
    def mysize(self):
        pass
    
class TextBlock(Block):
    def __init__(self,text,font_path,font_size,font_color,**kwargs):
        Block.__init__(self,**kwargs)
        self.text=unicode(text,'utf8') if type(text)!=unicode else text 
        self.font_path=font_path
        self.font_size=font_size
        self.font_color=font_color
        self.fnt = ImageFont.truetype(self.font_path, self.font_size)
    def draw(self,im,left,top,width,height):
        '''It's not implement other setting'''
        fnt=self.fnt
        d=ImageDraw.Draw(im)
        d.text((left,top),self.text,font=fnt,fill=self.font_color)
    def mysize(self):
        return self.fnt.getsize(self.text)
        #return (self.fnt.size*len(self.text),self.fnt.size)
        
class ImageBlock(Block):
    def __init__(self,image_path,**kwargs):
        Block.__init__(self,**kwargs)
        self.image_path=image_path
        self.size=Image.open(image_path).size
    def draw(self,im,left,top,width,height):
        sub_im=Image.open(self.image_path)
        sub_im=sub_im.resize((width,height))
        #print (left,top,left+width,top+height)
        im.paste(sub_im,(left,top,left+width,top+height))
    def mysize(self):
        return self.size
    
class Layer(object):
    def __init__(self,width_limit=None,height_limit=None):
        #TODO width_limit,height_limit is not avaiable
        self.stream=[]
        self.width_limit=width_limit
        self.height_limit=height_limit
    def add(self,block,link=1):
        self.stream.append((block,link))
    def plan(self):
        lines=[[]]
        weights=[0.0]
        for block,link in self.stream:
            if len(lines[-1])==0 or weights[-1]+link<=1.0:
                lines[-1].append(block)
                weights[-1]+=link
            else:
                lines.append([block])
                weights.append(link)
        return lines,weights
    def render(self):
        # get size
        lines,weights=self.plan()
        size_l=[]
        for line in lines:
            size_l.append([block.mysize() for block in line])
        width_l=[sum(map(lambda x:x[0],line)) for line in size_l]
        height_l=[max(map(lambda x:x[1],line)) for line in size_l]
        width=max(width_l)
        height=sum(height_l)
        left=0
        top=0
        im=Image.new('RGBA',(width,height))
        for index,line in enumerate(lines):
            left=0
            #w=width_l[index]/len(lines[index])
            #w=width/len(lines[index])
            h=height_l[index]
            for i,block in enumerate(line):
                w=size_l[index][i][0]
                #print left,top,w,h
                block.plot(im,left,top,w,h)
                left+=w
            top+=h
        #print width_l,height_l
        #raise Exception
        return im
            
            
            
        
class Card_factory(object):
    def __init__(self,battler_path,out_path,Enemies_path,font_path):
        self.battler_path=battler_path
        self.out_path=out_path
        self.Enemies_path=Enemies_path
        self.enemies=extract_f(self.Enemies_path)
        self.font_path=font_path
        if not os.path.exists(battler_path):
            raise Exception('please assign a valid path to get battler image')
        if not(os.path.exists(out_path)):
            os.mkdir(out_path)
    def take_image(self,dic):
        inner_path=unicode(dic['battler'],'utf8')
        image_path=os.path.join(self.battler_path,inner_path+'.png')
        im=Image.open(image_path)
        return im
    def _get_card(self,dic):
        im=self.take_image(dic)
        xs,ys=im.size
        base_size=(153,220)
        fnt = ImageFont.truetype(self.font_path, 30)
        d=ImageDraw.Draw(im)
        text_s=unicode(dic['name'],'utf8')
        d.text((10,10),text_s,font=fnt,fill=(100,100,100,100))
        return im
    def get_card(self,dic):
        layer=Layer()
        image_path=os.path.join(self.battler_path,unicode(dic['battler'],'utf8')+'.png')
        font_path=self.font_path
        layer.add(TextBlock(dic['name'],font_path,25,(100,100,100,100)))
        layer.add(ImageBlock(image_path))
        matrix=[['atk',' ','def'],['HP','  ','MP']]
        for line in matrix:
            for var in line:
                if ' ' in var:
                    layer.add(TextBlock(var,font_path,20,(100,100,100,200)),link=0.1)
                else:
                    text=var.upper()+' '+str(dic[var])
                    layer.add(TextBlock(text,font_path,20,(100,100,100,200)),link=0.45)
        return layer.render()
    def output(self):
        for dic in self.enemies:
            name=unicode(dic['name'],'utf8')+'.png'
            try:
                im=self.get_card(dic)
                im.save(os.path.join(self.out_path,name))
                print 'succ to output',name
            except:
                print 'fail to output ',name
        
        
#cf=Card_factory(u'../../猪头人的复仇/Graphics/Battlers','card','Enemies.rvdata','simsun.ttc')
#cf.get_card(cf.enemies[-1])
        