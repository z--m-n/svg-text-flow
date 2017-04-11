#!/usr/bin/env python3

from bs4 import BeautifulSoup, Tag   
import re
import os

if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Translate text flow in SVG from foreignObject to flowRoot.')
    parser.add_argument("-i", nargs=1, metavar=('input'),default='',
                            help="path to input SVG", type=str)
    parser.add_argument("-o", nargs=1, metavar=('output'),default='',
                            help="path to output SVG", type=str)
    parser.add_argument("-s", nargs=2, metavar=('scale'),default=[75, 115],
                            help='scale font size and line height (%%)', type=int)                            
    parser.add_argument("-f", nargs=1, metavar=('font'),default=["sans-serif"],
                            help="default font", type=str)                              
    parser.add_argument("-v","--verbose", help="increase output verbosity",
                            action="store_true")
    args = parser.parse_args()
    
    ifile = args.i[0] if args.i else None 
    ofile = args.o[0] if args.o else None
    scale = args.s
    dfont = args.f[0]
    
    print("Default Font: {}".format(dfont))
    print("     Scaling: {0}% (font) {1}% (height)".format(scale[0],scale[1]))
       
    if not (ifile and ofile) or \
        not os.path.exists(ifile) or os.path.exists(ofile):
        raise SystemExit('Exit: provide valid input ("{0}") and output ("{1}") file names'.format(ifile,ofile))
    
    with open(ifile) as fd:
        soup = BeautifulSoup(fd.read(),'xml')

    # foriegnObject objects
    foos = soup.findAll('foreignObject')

    # style
    sts  = "color: #000000;font-family: "+dfont+";font-size: 12px;font-style: normal;font-weight: normal;text-align: center;text-decoration: none;margin: 0;"
    stf  = "font-stretch:normal;line-height:120%;letter-spacing:0px;word-spacing:0px;fill-opacity:1;stroke:none;stroke-width:1px;stroke-linecap:butt;stroke-linejoin:miter;stroke-opacity:1;"
    stl  = dict([tuple(n.split(':')) for n in (stf+sts).replace(': ',':').split(';') if n!=""])
    sfw  = dict([('bold',800),('light',300),('normal',400)])

    for k in list(range(len(foos))):
        foo    = foos[k]

        # position and size of the foreignobject textflow rectangle
        x,y,w,h=[foo.get(x) for x in ['x','y','width','height']]   

        # style
        ptags = foo.findAll('span') # catch multiple <p><span>...</span></p> blocks
        ptag = ptags[0]             # take style attributes from the first element
        st = ptag.get('style').replace(': ',':')
        st = dict([tuple(n.split(':')) for n in st.split(';') if n!=''])
        std = {**stl,**st}          # pyhon >3.4 

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
        std['font-size'] = '{0:.1f}px'.format(float(std['font-size'].replace('px',''))*scale[0]/100.)
        std['line-height'] = '{0}%'.format(int(std['line-height'].replace('%',''))*scale[1]/100.)
        sta = ''.join([ '{}:{};'.format(k,v) for k,v in std.items() ])
        
        # parent group
        g = foo.findParent()

        # flowRoot and children elements
        tid  = str(k)
        tag1 = Tag(g, name="flowRoot", attrs={"id":"flowRoot"+tid,"xml:space":"preserve","style":sta,})
        tag2 = Tag(g, name="flowRegion", attrs={"id":"flowRegion"+tid})
        tag3 = Tag(g, name="rect", attrs={"id":"rect"+tid,"x":x,"y":y,"width":w,"height":h,"style":sta})
        tag4 = [] 
        for pt in ptags:
            tag4.append(Tag(g, name="flowPara", attrs={"id":"flowPara"+tid}))
            tag4[-1].string = pt.getText().strip()

        # replace foreignObject with flowRoot
        foo.replace_with(tag1)
        tag1.insert(0, tag2)
        tag2.insert(0, tag3)
        for pt in tag4:
            tag1.append(pt)

    with open(ofile,'w') as fd:
        fd.write(str(soup))   
