# -*- coding: utf-8 -*-
"""
Created on Thu May 16 20:24:04 2019

@author: ljr


                        .::::.
                      .::::::::.
                     :::::::::::
                  ..:::::::::::'
               '::::::::::::'
                 .::::::::::
            '::::::::::::::..
                 ..::::::::::::.
               ``::::::::::::::::
                ::::``:::::::::'        .:::.
               ::::'   ':::::'       .::::::::.
             .::::'      ::::     .:::::::'::::.
            .:::'       :::::  .:::::::::' ':::::.
           .::'        :::::.:::::::::'      ':::::.
          .::'         ::::::::::::::'         ``::::.
      ...:::           ::::::::::::'              ``::.
     ```` ':.          ':::::::::'                  ::::..
                        '.:::::'                    ':'````..

"""

import os
import cv2 as cv
import random

path=""#曝光度为6的文件存放路径

all_names=os.listdir(os.getcwd()+"/"+path)

random.shuffle(all_names)

people=["Dujw","Wangzh"]
N=int(len(all_names)/len(people))

for i in range(len(people)):
    if os.path.exists(os.getcwd()+"/"+people[i]):
            os.mkdir(os.getcwd()+"/"+people[i])
    for j in range(N):
        img=cv.imread(os.getcwd()+"/"+path+"/"+all_names[i*N+j])
        cv.imwrite(os.getcwd()+"/"+people[i]+"/"+all_names[i*N+j],img)
    






















