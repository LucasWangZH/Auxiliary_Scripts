# -*- coding: utf-8 -*-
"""
Created on Tue May 14 11:06:59 2019

@author: slkj
"""

import os, random, shutil
def movefile(dir):
    pathDir = os.listdir(dir)
# num是要随机选取的图片数量
    num = 130
    sample = random.sample(pathDir,num)
    print(sample)

    for name in sample:
        #若果是拷贝，不是移动，就把move改为copyfile
        shutil.move(fileDir+name, tarDir+name)
if __name__ == '__main__':
    fileDir = "D:/project/openposelab/rawimages_train/"
    tarDir = "D:/project/openposelab/rawimages_test/"
    movefile(fileDir)