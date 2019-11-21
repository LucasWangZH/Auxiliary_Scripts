# coding=utf-8

# 删除单个点 ： ctrl + 左击
# 删除单个物体所有点 ： ctrl + 右击
# 删除全部：    c 键
import cv2
import os
import numpy as np
import drawhz as drawhz


path = "img"

label_map='''
标签0=label0
标签1=label1
标签2=label2
标签3=label3
标签4=label4
标签79=label79
'''

files = []
objs = []
obj = []

labelName = []
labelName_hz = []

currentClass=0
basic=0

classes = label_map.split("\n")

for cl in classes:
    if not cl == "":
        labelName.append(cl.split("=")[1])
        labelName_hz.append(cl.split("=")[0])

for root, dir, _files in os.walk("D:/project/openposelab/newdata"):
    for _file in _files:
        if _file.endswith(".jpg") or _file.endswith(".jpeg"):
            files.append(os.path.join(root, _file))

def drawHZ(im, text, org, color=(0, 255, 0), fontSize=15, bold=True, italic=False, underline=False):
	drawhz.draw(im, text, org, color, fontSize, bold, italic, underline)

g_colors = []
def hsv2rgb(h, s, v):
    h_i = int(h * 6)
    f = h * 6 - h_i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r = 0
    g = 0
    b = 0
    if h_i == 0:
        r = v
        g = t
        b = p
    elif h_i == 1:
        r = q
        g = v
        b = p
    elif h_i == 2:
        r = p
        g = v
        b = t
    elif h_i == 3:
        r = p
        g = q
        b = v
    elif h_i == 4:
        r = t
        g = p
        b = v
    elif h_i == 5:
        r = v
        g = p
        b = q
    else:
        r = 1
        g = 1
        b = 1
    return (int(r * 255), int(g * 255), int(b * 255))

def getColor(n, num=30):
    global g_colors

    if len(g_colors) == 0:
        for i in range(100):
            h = i / float(num)
            g_colors.append(hsv2rgb(h, 1, 1))
    return g_colors[n % len(g_colors)]


def drawImg():
    bak = img.copy()
    for i in range(len(objs)):
        cv2.drawContours(bak, np.array([objs[i][1:]]), 0, getColor(i), -1)
    cv2.addWeighted(bak, 0.5, img, 0.5, 0, show_img)

    # 对正在标注的
    for i in range(1, len(obj)):
        cv2.circle(show_img, (obj[i][0], obj[i][1]), 1, (0, 255, 0), 2)
        if i > 1:
            cv2.line(show_img, (obj[i][0], obj[i][1]), (obj[i - 1][0], obj[i - 1][1]),  (0, 255, 0))

    drawHZ(show_img, labelName_hz[currentClass], (10, 10), (0, 255, 0), 20, True)
    drawHZ(show_img, "%s/%s"%(num, len(files)), (10, 30), (0, 255, 0), 20, True)

def refresh():
    drawImg()
    cv2.imshow("image", show_img)

def addObj(x, y):
    if len(obj) < 1:
        obj.append(["label", labelName[currentClass]])

    if x > 0 and y > 0:
        obj.append([x, y])
    print(obj)


def delObj(x, y):
    for _x, _y in obj:
        pass

def delAllObj(x, y):
    if len(objs) > 0:
        ds = []
        for _obj in objs:
            ds.append((x - _obj[1][0]) * (x - _obj[1][0]) + (y - _obj[1][1]) * (y - _obj[1][1]))
        if min(ds) < 400:
            i = ds.index(min(ds))
            del objs[i]


def onMouse(event, x, y, flag, params):
    if event == cv2.EVENT_MOUSEMOVE:
        return
    if event == cv2.EVENT_LBUTTONDOWN:
        if flag == 1:# 左击
            addObj(x, y)
            refresh()

        if flag == 9: # ctrl + 左击
            delObj(x, y)
            refresh()

    if event == cv2.EVENT_RBUTTONDOWN:
        if flag == 10:# ctrl + 右击
            delAllObj(x, y)
            refresh()

def saveToText(file):
    with open(file.replace(".jpg", ".txt"), "w") as f:
        f.write(str(len(objs) + 1) + "\n")
        f.write("%s,%s\n"%(img.shape[0], img.shape[1]))

        for i in range(len(objs)):
            for j in range(len(objs[i])):
                f.write("%s,%s" % (objs[i][j][0], objs[i][j][1]))
                if j < len(objs[i]) - 1:
                    f.write(",")
            f.write("\n")

def loadObjsText(file):
    global objs
    objs = []
    if os.path.exists(file.replace(".jpg", ".txt")):
        with open(file.replace(".jpg", ".txt"), "r") as f:
            lines = f.readlines()
            for i in range(2, len(lines)):
                line = lines[i].replace("\n", "").split(",")
                obj = []
                for i in range(len(line)):
                    if len(line[i]) < 1:
                        continue
                    if i > 1:
                        if i % 2 == 0:
                            obj.append([(int)(line[i]), (int)(line[i + 1])])
                    else:
                        if i % 2 == 0:
                            obj.append([line[i], line[i + 1]])
                if len(obj) > 0:
                    objs.append(obj)

    return objs


cv2.namedWindow("image", cv2.WINDOW_NORMAL)
cv2.setMouseCallback("image", onMouse)

img = []
show_img = []
running = True
num = 0
while running:

    objs = loadObjsText(files[num])

    while num < len(files):
        img = cv2.imread(files[num])
        show_img = img.copy()
        refresh()
        key = cv2.waitKey()

        if key == ord(' '):
            if len(obj) > 1:
                objs.append(obj)

            saveToText(files[num])
            obj=[]
            objs=[]
            num = num + 1
            if num == len(files):
                num = 0
            if num < len(files):
                objs = loadObjsText(files[num])

            continue

        if key == ord("c"):
            objs = []
            obj = []
            continue

        if key == 27:
            if len(obj) > 1:
                objs.append(obj)
            saveToText(files[num])
            running = False
            break

        if key == ord("a"):
            if len(obj) > 1:
                objs.append(obj)
                obj = []
            continue
            
        if key == ord('w'):
            obj = []
            objs = []
            num = num - 1
            if num < 0:
                num = len(files) - 1
            break
        if key == ord("s"):
            obj = []
            objs = []
            num = num + 1
            if num >= len(files):
                num = 0
            break

        if key >= ord('0') and key <= ord("9"):
            currentClass = key - ord('0') + basic
            print(currentClass)

        if key == ord("e"):
            basic = basic + 10
            currentClass = 10 + currentClass

            if basic > 70:
                basic = 0

            if currentClass >= 80:
                currentClass = 0

cv2.destroyAllWindows()
 