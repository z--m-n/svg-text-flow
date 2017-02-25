# -*- coding: utf-8 -*-
"""
Created on Fri Dec 23 15:36:31 2016

@author: matthias zeeman
"""
    
from bs4 import BeautifulSoup, Tag   
import re

with open('/tmp/Example1.svg') as fd:
    soup = BeautifulSoup(fd.read(),'xml')

# foriegnObject objects
foos = soup.findAll('foreignObject')

# style
sts  = "color: #000000;font-family: Arial;font-size: 14px;font-style: normal;font-weight: normal;text-align: center;text-decoration: none;margin: 0;"
stf  = "font-stretch:normal;line-height:120%;letter-spacing:0px;word-spacing:0px;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;"
std  = dict([tuple(n.split(':')) for n in (stf+sts).replace(': ',':').split(';') if n!=""])
sfw  = dict([('bold',800),('light',300),('normal',400)])


for k in list(range(len(foos))):
    foo    = foos[k]
    
    # position and size of the foreignobject textflow rectangle
    x,y,w,h=[foo.get(x) for x in ['x','y','width','height']]   
    
    # style
    ptag  = foo.find('span') # find <span> or <p>?
    st = ptag.get('style').replace(': ',':')
    st = dict([tuple(n.split(':')) for n in st.split(';') if n!=''])
    std = {**std,**st} # pyhon >3.4 
    
    # style updates, sanatized font properties
    std['fill'] = std.pop('color')
    m = re.search('[\W\s]*(Italic)+',std['font-family'])
    if m:
        std['font-style'] = m.group().strip().lower()
        std['font-family'] = std['font-family'].replace(m.group(),'')
    m = re.search('[\W\s]*(Light|Bold)+',std['font-family'])
    if m and std['font-weight']=='normal':
        std['font-weight'] = sfw[ m.group().strip().lower() ]
        std['font-family'] = std['font-family'].replace(m.group(),'')
    sta = ''.join([ '{}:{};'.format(k,v) for k,v in std.items() ])    
    
    # parent group
    g = foo.findParent()
    
    # flowRoot and children elements
    tid  = str(k)
    tag1 = Tag(g, name="flowRoot", attrs={"id":"flowRoot"+tid,"xml:space":"preserve","style":sta,})
    tag2 = Tag(g, name="flowRegion", attrs={"id":"flowRegion"+tid})
    tag3 = Tag(g, name="rect", attrs={"id":"rect"+tid,"x":x,"y":y,"width":w,"height":h,"style":sta})
    tag4 = Tag(g, name="flowPara", attrs={"id":"flowPara"+tid})
    tag4.string = ptag.getText().strip()
    
    # replace foreignObject with flowRoot
    g.insert(0, tag1)
    tag1.insert(0, tag2)
    tag2.insert(0, tag3)
    tag1.insert(0, tag4)
    foo.decompose()
    
with open('/tmp/Example1_mod.svg','w') as fd:
    fd.write(str(soup))   
 
    
# inkscape --file='/tmp/Example1_mod.svg' --export-area-page --export-text-to-path --export-pdf='/tmp/Example1_mod+conv.pdf'
# inkscape --file='/tmp/Example1_mod.svg' --export-area-page --export-dpi=90 --export-png='/tmp/Example1_mod+conv.png'
    
    
