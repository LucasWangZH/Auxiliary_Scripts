# -*- coding: utf-8 -*-
"""
Created on Tue Apr 30 15:25:04 2019

@author: zyx
"""
import os
import sys
import glob
from PIL import Image

src_img_dir="C:/Users/slkj/Desktop/che/过滤实验/数据汇总/汇总/新样本/正面JPEG"
src_txt_dir="C:/Users/slkj/Desktop/che/过滤实验/数据汇总/汇总/新样本/正面TXT"
src_xml_dir="C:/Users/slkj/Desktop/che/过滤实验/数据汇总/汇总/新样本/正面XML"

img_list=glob.glob(src_img_dir+'/*.jpg')

print(img_list[0])

img_basenames=[]
for item in img_list:
    img_basenames.append(os.path.basename(item))

print(img_basenames[0])

img_names=[]
for item in img_basenames:
    item1,item2=os.path.splitext(item)
    img_names.append(item1)

print(img_names[0])

for img in img_names:    
    print(img)
    gt=open(src_txt_dir+'/'+img+'.txt').read().splitlines()
    width,height=gt[1].split(',')

    xml_file=open((src_xml_dir+'/'+img[:]+'.xml'),'w')
    xml_file.write('<annotation>\n')
    #xml_file.write('    <folder>physics</folder>\n')
    #xml_file.write('    <filename>'+str(img)+'.jpg'+'</filename>\n')
    xml_file.write('    <size>\n')
    xml_file.write('        <width>'+str(width)+'</width>\n')
    xml_file.write('        <height>'+str(height)+'</height>\n')
    xml_file.write('    </size>\n')
    
    for i in range(2,len(gt)):
        info=gt[i].split(',')
        #print(len(info))
        if info[0] == 'point':
            continue
        if info[1]=='cheng':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>cheng</name>\n')
        elif info[1] == 'phshizhi':
            continue
        elif info[1]=='pen':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>pen</name>\n')
        elif info[1]=='xiangpidaoguan':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>xiangpidaoguan</name>\n')
        elif info[1]=='shiguan':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>shiguan</name>\n')
        elif info[1]=='jiazi':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>jiazi</name>\n')
        elif info[1]=='bolipian':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>bolipian</name>\n')
        elif info[1]=='jiujingdeng':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>jiujingdeng</name>\n')
        elif info[1]=='diguan':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>diguan</name>\n')
        elif info[1]=='shaobei':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>shaobei</name>\n')
        elif info[1]=='nophpeiyangmin':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>nophpeiyangmin</name>\n')
        elif info[1]=='liangtong':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>liangtong</name>\n')
        elif info[1]=='chengliangzhi':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>chengliangzhi</name>\n')
        elif info[1]=='liusuanping':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>liusuanping</name>\n')
        elif info[1]=='daoqiguan':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>daoqiguan</name>\n')
        elif info[1]=='phpeiyangmin':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>phpeiyangmin</name>\n')
        elif info[1]=='shou':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>shou</name>\n')
        elif info[1]=='bolibang':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>bolibang</name>\n')
        elif info[1]=='tiejiatai':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>tiejiatai</name>\n')
        elif info[1]=='lvzhiloudou':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>lvzhiloudou</name>\n')
        elif info[1]=='wulvzhiloudou':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>wulvzhiloudou</name>\n')
        elif info[1]=='shiguankou':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>shiguankou</name>\n')
        elif info[1]=='shiguanwei':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>shiguanwei</name>\n')
        elif info[1]=='zhicao':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>zhicao</name>\n')   
        elif info[1]=='shiguanjia':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>shiguanjia</name>\n')
        elif info[1]=='renlian':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>renlian</name>\n')
        elif info[1]=='liangtongkou':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>liangtongkou</name>\n')
        elif info[1]=='liangtongwei':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>liangtongwei</name>\n')
        elif info[1]=='lvzhi':
            continue
            xml_file.write('    <object>\n')
            xml_file.write('        <name>lvzhi</name>\n')
        elif info[1]=='tiejiaquan':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>tiejiaquan</name>\n')
        elif info[1]=='loudoujianzui':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>loudoujianzui</name>\n')
        elif info[1]=='shirunping':
            #continue
            xml_file.write('    <object>\n')
            xml_file.write('        <name>shirunping</name>\n')
        elif info[1]=='hbshaobei':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>shaobei</name>\n')
        elif info[1]=='leverFulCrum':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>leverFulCrum</name>\n')
        elif info[1]=='leverEnd':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>leverEnd</name>\n')
        elif info[1]=='cursor':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>cursor</name>\n')
        elif info[1]=='weight':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>weight</name>\n')
        elif info[1]=='hand':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>hand</name>\n')
        elif info[1]=='spring':
            xml_file.write('    <object>\n')
            xml_file.write('        <name>spring</name>\n')
        xml_file.write('        <bndbox>\n')
        xml_file.write('            <xmin>'+str(min(int(info[2]),int(info[5])))+'</xmin>\n')
        xml_file.write('            <ymin>'+str(min(int(info[3]),int(info[6])))+'</ymin>\n')
        xml_file.write('            <xmax>'+str(max(int(info[2]),int(info[5])))+'</xmax>\n')
        xml_file.write('            <ymax>'+str(max(int(info[3]),int(info[6])))+'</ymax>\n')
        xml_file.write('        </bndbox>\n')
        xml_file.write('    </object>\n')
    
    xml_file.write('</annotation>')


        










