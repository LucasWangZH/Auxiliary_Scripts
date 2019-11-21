# -*- coding: UTF-8 -*-
import cv2
import re
import os
import numpy as np
files = []
path_url="C:/Users/slkj/Desktop/che/过滤实验/数据汇总/汇总/新样本/正面JPEG"

for root,dirs,file in os.walk(path_url,topdown=False):
    for name in file:
        url=os.path.join(root,name)
        if os.path.splitext(url)[1]=='.jpg':
            files.append(url)

def level(x,width):
    value =0
    if x>width/2 or x<width/2:
        value =width-x
    else:
        value=x
    return value
for i in range(len(files)):
    img = cv2.imdecode(np.fromfile(files[i], dtype=np.uint8), cv2.IMREAD_UNCHANGED)  # 打开含有中文路径的图片
    #img = cv2.imread(files[i])
    #img = cv2.imdecode(np.fromfile(files[i], dtype=np.uint8), -1)
    img1 = cv2.flip(img,1)
    img_url = files[i][:-4]
    #print(img_url[1]+"."+img_url[2])
    #cv2.imwrite(img_url+"_level0.jpg",img1)
    cv2.imencode('.jpg', img1)[1].tofile(img_url+"_level0.jpg")
    file = open(img_url+".txt","r+")
    level_file = open(img_url+"_level0.txt",'w')
    line = file.readline()
    index = 0
    #结算台标签
    # lable = ['jst1006', 'jst1025', 'jst1026', 'jst1027', 'jst1029','jst1030','jst1031','jst1032','jst1033','jst1034','jst1035','jst1036','jst1037','jst1038'
    #     , 'jst1039','jst1040','jst1041','jst1042','jst1043','jst1044','jst1046','jst1047','jst1048','jst1049'
    #     , 'jst1050','jst1051','jst1052','jst1053','jst1054','jst1055','jst1056','jst1057','jst1058','jst1059'
    #     , 'jst1060','jst1062','jat1036']
    lable = ['daoqiguan','lvzhi','bolibang','loudou','tiejiatai','lanzi','cheng','pen','xiangpidaoguan',
             'jiujingdeng','qimiping','jiazi','bolipian','liusuanping'
        , 'shiguan','liusuanping','tiejiatai','chengliangzhi','shaobei','diguan','phshizhi','liangtong','jiazi'
             ,'renlian','liangtongkou','liangtongwei']
    width = 0
    hight = 0
    while line:
        if index ==0:
            level_file.writelines(line)
        if index ==1:
            level_file.writelines(line)
            line = line.rstrip("\n")
            whs = re.split(",",line)
            width = int(whs[0])
            hight = int(whs[0])
            # width = 1280
            # hight = 960
        if index >=2:
            line = line.rstrip("\n")
            xylist = re.split(",", line)
            #fs = lable.index(xylist[1])
            # if fs == 0:
            if(xylist[0] == "point"):
                continue
            print(files[i])
            cv2.rectangle(img,(int(xylist[2]),int(xylist[3])),(int(xylist[5]),int(xylist[6])),(0,0,255))
            cv2.rectangle(img1,(level(int(xylist[2]),width),int(xylist[3])),(level(int(xylist[5]),width),int(xylist[6])),(0,0,255))
            text =xylist[0]+","+xylist[1]+"," + str(level(int(xylist[2]),width)) + "," + str(int(xylist[3])) + ",False," + str(level(
                int(xylist[5]),width)) + "," + str(int(xylist[6])) + ",False," + str(level(int(xylist[8]),width)) + "," +str(int(xylist[9])) + ",False"+"\n"
            level_file.writelines(text)
            # else:
            #     cv2.circle(img,(int(xylist[2]),int(xylist[3])),8,(0,0,255))
            #     cv2.circle(img1,(level(int(xylist[2]),width),int(xylist[3])),8,(0,0,255))
            #     text ="point,hand,"+str((level(int(xylist[2]),width)))+","+str(int(xylist[3]))+",False"+"\n"
            #     level_file.writelines(text)
        index = index +1
        line = file.readline()
    file.close()
    level_file.close()
    # cv2.imshow("before",img)
    # cv2.imshow("test",img1)
    # cv2.waitKey(0)



