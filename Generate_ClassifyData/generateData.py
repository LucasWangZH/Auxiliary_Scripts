#encoding utf-8
import cv2
import numpy as np
import os

datasetJPGPath = './jpeg/'
datasetXMLPath = './anno_xml/'
datasetTXTPath = './anno_txt/'
datasetSAVEPath = './data/'


CHEMICAL_BBOX_LABEL_NAMES = (
    'cheng',
    'tiejiatai',
    'xiangpidaoguan',
    'shiguan',
    'daoqiguan',
    'shou',
    'jiazi',
    'phpeiyangmin',
    'bolipian',
    'jiujingdeng',
    'diguan',
    'shaobei',
    'nophpeiyangmin',
    'liangtong',
    'chengliangzhi',
    'liusuanping',
    'bolibang',
    'shiguanjia',
    'pen',
    'zhicao',
    'lvzhiloudou',
    'wulvzhiloudou',
    'shiguankou',
    'shiguanwei',
    'liangtongkou',
    'liangtongwei',
    'renlian',
    'phshizhi')


def file_name(file_dir):
    L = []
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.jpg':
                L.append(os.path.join(file))
    return L

def cv_imread(file_path):
    cv_img = cv2.imdecode(np.fromfile(file_path,dtype= np.uint8),-1)
    return cv_img

def getTxtname(file_dir,labelf,replicate):
    L = []
    f = open(file_dir)
    lines = f.readlines()
    labels = []
    bbox = []
    for i in range(len(lines)-2):
        line = lines[i+2].split(",")
        if line[1] == 'phshizhi':
            continue
        label = CHEMICAL_BBOX_LABEL_NAMES.index(line[1])

        xmin = min(int(line[2]),int(line[5]))
        ymin = min(int(line[3]),int(line[6]))
        xmax = max(int(line[5]),int(line[2]))
        ymax = max(int(line[3]),int(line[6]))

        box = [xmin,ymin,xmax,ymax]

        bbox.append(box)
        labelf.writelines(str(label))
        labelf.writelines('\r\n')


    return bbox


iter = 0


labelf = open("labels.txt","w")
for i in range(1):

    picFilenames = file_name(datasetJPGPath)
    print("L: ",len(picFilenames))

    for i in range(len(picFilenames)):

        Filename = picFilenames[i]
        picFilename = datasetJPGPath + Filename
        imgOri = cv_imread(picFilename)

        Filename = Filename[:-4]
        txtFilename = datasetTXTPath + Filename + '.txt'
        try:
            bbox = getTxtname(txtFilename,labelf,1)
        except Exception as e:
            print(picFilenames[i])

        for box in bbox:
            img = imgOri[box[1]:box[3],box[0]:box[2]]
            picname = datasetSAVEPath + str(iter) + ".jpg"
            iter = iter + 1
            cv2.imwrite(picname,img)

            """
            h_flip = cv2.flip(img, 1)
            picname = datasetSAVEPath + str(iter) + ".jpg"
            iter = iter + 1
            cv2.imwrite(picname, h_flip)

            v_flip = cv2.flip(img, 0)
            picname = datasetSAVEPath + str(iter) + ".jpg"
            iter = iter + 1
            cv2.imwrite(picname, v_flip)

            hv_flip = cv2.flip(img,-1)
            picname = datasetSAVEPath + str(iter) + ".jpg"
            iter = iter + 1
            cv2.imwrite(picname, hv_flip)
            """

















