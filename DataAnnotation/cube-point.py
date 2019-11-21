#!/usr/bin/python
# coding=utf-8
# V 1.1

'''
b 	切换点和框标注
r 	键删除图片，txt文件
a 	增加标注的点数
q 	删除标注的点数
w、< 	上一张图片
s、> 	下一张图片
u 	更改基准
空格 	保存
ctrl+左击	 删除点
ctrl+右击	 更改位置
alt+左击	 更改属性
alt+右击	 更改label
esc 	退出
'''
import cv2
import os, xml.dom.minidom, sys
import numpy as np
if sys.version_info.major == 2:
	import drawhz as drawhz
else:
	import drawhz3 as drawhz

#path="C:/Users/slkj/Desktop/che/0726end/test-end/jpeg"
#path="C:/Users/slkj/Desktop/che/0802最新样本/test"
path  = "C:/Users/slkj/Desktop/che/过滤实验/化学试验-end/化学试验-end/侧面/2"
model="cube"
f_name=""


className_list='''
cheng=电子秤
pen=水盆
tiejiatai=铁架台
xiangpidaoguan=橡皮导管
shiguan=试管
daoqiguan=导气管
shou=手
jiazi=夹子
peiyangmin=培养皿
phshizhi=ph试纸
bolipian=毛玻璃片
jiujingdeng=酒精灯
diguan=滴管
shaobei=烧杯
liangtong=量筒
chengliangzhi=称量纸
liusuanping=硫酸瓶
bolibang=玻璃棒
shiguanjia=试管夹
zhicao=纸槽
lvzhiloudou=带滤纸漏斗
wulvzhiloudou=无滤纸漏斗
shiguankou=试管口
shiguanwei=试管尾
nophpeiyangmin=无ph培养皿
phpeiyangmin=ph培养皿
phshizhi=ph试纸
renian=人脸
liangtongkou=量筒口
liangtongwei=量筒尾
tiejiaquan=铁夹圈
lvzhi=滤纸
shirunping=湿润瓶
loudoujianzui=漏斗尖嘴
'''



if sys.version_info.major == 2:
	path = path.decode("utf-8").encode("gbk")

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
		r=v
		g=t
		b=p
	elif h_i == 1:
		r=q
		g=v
		b=p
	elif h_i == 2:
		r=p
		g=v
		b=t
	elif h_i == 3:
		r=p
		g=q
		b=v
	elif h_i == 4:
		r=t
		g=p
		b=v
	elif h_i == 5:
		r=v
		g=p
		b=q
	else:
		r=1
		g=1
		b=1
	return (int(r*255), int(g*255), int(b*255))

g_colors = []
def getColor(n, num=0):
	global g_colors, check_label
	
	if len(g_colors) == 0:
		for i in range(100):
			h = i / float(num)
			g_colors.append(hsv2rgb(h, 1, 1))
	return g_colors[n % len(g_colors)]

def drawHZ(im, text, org, color=(0, 255, 0), fontSize=15, bold=True, italic=False, underline=False):
	drawhz.draw(im, text, org, color, fontSize, bold, italic, underline)

def saveBreakPoint():
	with open("breakpoint.txt", 'w') as f:
		f.write(str(currentImg))
	f.close()
	
def loadBreakPoint():
	if os.path.exists("breakpoint.txt"):
		with open("breakpoint.txt", 'r') as f:
			a = f.read()
		f.close()
		return a
	else:
		return 0

def saveToTxt(w, h):
	with open(os.path.splitext(imgs[currentImg])[0] + '.txt', 'w') as f:
		validCount = 0
		for obj in objs:
			if currentPoint == 0:
				validCount = validCount + 1
			else:
				validCount = len(objs) - 1
		f.write("%d\n" % validCount)
		f.write("%d,%d\n" % (w, h))
		for i in range(len(objs)):
			obj = objs[i]
			# 为什么进行判断 在currentpoint不等于0的时候，最后一个obj不保存
			if not i == len(objs) - 1:
				
				f.write("%s,%s" % (obj[0],obj[1]))
				for i in range(2, len(obj)):				
					f.write(",%d,%d,%s" % (obj[i][0], obj[i][1], obj[i][2]))
				f.write("\n")
			else:
				
				if currentPoint == 0:
					f.write("%s,%s" % (obj[0],obj[1]))
					for i in range(2, len(obj)):
						f.write(",%d,%d,%s" % (obj[i][0], obj[i][1], obj[i][2]))
					f.write("\n")

def loadTxt(number):	
	global point, obj, objs
	name = os.path.splitext(imgs[currentImg])[0] + '.txt'

	print(os.path.splitext(imgs[currentImg]))

	if os.path.exists(name):
		with open(name, 'r') as f:
			lines = f.readline()
			# shape 是图片宽高
			shape = f.readline()
			line = ''
			for i in range(int(lines)):				
				line = f.readline().strip()
				
				o = line.split(',')
				if o[0] == "":
					continue
                
				obj.append(o[0])
                
				obj.append(o[1])
				for j in range( (int)((len(o) - 2) / 3) ):

					for k in range(3):
						if k == 2:
							point.append((o[j * 3 + k + 2]) == "True" )
							
						else:
							point.append((int)(o[j * 3 + k + 2]) )
						
					obj.append(point)
					point = []
				
				objs.append(obj)
				obj = []
		
		return objs
	else:
		return []

def refresh(x=0, y=0):
	_x=x
	_y=y
	img = bak.copy()
	if not objs == None:
		for i in range(len(objs)):
			obj = objs[i]

			if obj[0]=="point":
				for j in range(2, len(obj)):
					
					if len(obj[j]) > 2:
						if obj[j][2]:
							
							cv2.circle(img, (obj[j][0], obj[j][1]), 4,(0, 0, 255), 2)
						else:

							cv2.circle(img, (obj[j][0], obj[j][1]), 4,(0, 255, 0), 4)
					if j > 2:
						cv2.line(img, (obj[j - 1][0], obj[j - 1][1]), (obj[j][0], obj[j][1]), colors[className.index(obj[1])], 2)	
				if i == len(objs) - 1:
					if currentPoint >= 1:
						if not x == 0 and not y ==0:
							
							cv2.line(img, (objs[i][2][0], objs[i][2][1]), (x, y), (255, 255, 0), 2)
							if not currentPoint == num - 1:
								xlen = x - objs[i][2][0]
								ylen = y - objs[i][2][1]
								x =  x + (num - currentPoint + 1) * xlen
								y =  y + (num - currentPoint  + 1) * ylen
								cv2.line(img, (objs[i][2][0], objs[i][2][1]), (x, y), (255, 255, 0), 2)
			elif obj[0]=="cube":
				if len(obj) <= 3:
					cv2.circle(img, (obj[2][0], obj[2][1]), 4,(0, 255, 0), 2)
				else:
					cv2.rectangle(img, (obj[2][0], obj[2][1]), (obj[3][0], obj[3][1]), colors[className.index(obj[1])], 3)
					cv2.circle(img, (obj[4][0], obj[4][1]), 4,(0, 255, 0), 2)
			drawHZ(img, str(className.index(obj[1]) + 1) + className_hz[className.index(obj[1])], (obj[2][0], obj[2][1]),color = colors[className.index(obj[1])])
	
	cv2.putText(img, str(currentImg) + '|' + str(len(imgs)), (10, 80), 2, 1, (0, 255, 0), 1)
	
	if (currentClass + basic) > len(className_hz) - 1:
		
		drawHZ(img, str(len(className_hz)) + className_hz[len(className_hz)-1],  (10, 20),fontSize=20)
	else:
		drawHZ(img, str(currentClass + basic+1) + className_hz[currentClass + basic], (10, 20), fontSize=20)
	#cv2.putText(img, str(num), (10, 110), 2, 1, (0, 255, 0), 1)
	drawHZ(img, "点数：" + str(num), (10, 90))
	drawHZ(img, "基准：" + str(basic), (10, 110))

	drawHZ(img, "已标注：" + str(len(objs)), (10, 130),fontSize=20)
	drawHZ(img, "模式：" + model, (10, 150), fontSize=20)
	if model=="cube" and not x == 0:
		cv2.line(img, (_x, 0), (_x, 1000), (255, 255, 0), 2)
		cv2.line(img, (0, _y), (1000, _y), (255, 255, 0), 2)

	cv2.imshow("image", img)

def addPoint(x, y, hidden):
	global currentPoint, obj, point
	point.append(x)
	point.append(y)

	if model=="cube":
		point.append(False)
	else:
		point.append(hidden)
	
	#point.append(hidden)
	obj.append(point)
	point = []
	if currentPoint == 0:
		a = currentClass + basic
		if a >= len(className):
			a = len(className) - 1 
		obj.insert(0, model)
		obj.insert(1, className[a])
		objs.append(obj)
	
	if model=="cube":
		
		if currentPoint == 1:
			point.append((int)((obj[2][0]+obj[3][0])/2))
			point.append((int)((obj[2][1]+obj[3][1])/2))
			point.append(False)
			obj.append(point)
			point=[]
			
			currentPoint = currentPoint + 1
		
	currentPoint = currentPoint + 1
	
def delObj(x, y):
	if len(objs) > 0:
		ds = []
		for i in range(len(objs)):
			d = (x - objs[i][2][0]) * (x - objs[i][2][0]) + (y - objs[i][2][1]) * (y - objs[i][2][1])
			ds.append(d)
		if min(ds) <= 400:
			i = ds.index(min(ds))
			del objs[i]
			return True
	return False

def changeHidden(x, y):
	m = -1
	n = -1
	distance = float('inf')
	if model == "point":
		if len(objs) > 0:
			for i in range(len(objs)):
				
				for j in range(2, len(objs[i])):
					d = (x - objs[i][j][0]) * (x - objs[i][j][0]) + (y - objs[i][j][1]) * (y - objs[i][j][1])
					
					if d < distance and d < 900:
						distance = d
						m = i
						n = j
			if n >=0 and m >=0:
				if objs[m][n][2] == False:
					objs[m][n][2] = True
				else:
					objs[m][n][2] = False

def changeLocation(x, y):
	m = -1
	n = -1
	distance = float('inf')
	if len(objs) > 0:
		for i in range(len(objs)):
			for j in range(2, len(objs[i])):
				d = (x - objs[i][j][0]) * (x - objs[i][j][0]) + (y - objs[i][j][1]) * (y - objs[i][j][1])
				if d < distance and d < 900:
					distance = d
					m = i
					n = j 
		if n >=0 and m >=0:
			objs[m][n][0] = x
			objs[m][n][1] = y

def chlaebl(x, y):
	if len(objs) > 0:
		ds = []
		for i in range(len(objs)):
			d = (x - objs[i][2][0]) * (x - objs[i][2][0]) + (y - objs[i][2][1]) * (y - objs[i][2][1])
			ds.append(d)
		if min(ds) <= 400:
			i = ds.index(min(ds))
			#del objs[i]
			if objs[i][1]==label_one:
				objs[i][1]=label_two
			elif objs[i][1]==label_two:
				objs[i][1]=label_three
			elif objs[i][1]==label_three:
				objs[i][1]=label_four
			elif objs[i][1]==label_four:
				objs[i][1]=label_five
			elif objs[i][1]==label_five:
				objs[i][1]=label_one
			elif objs[i][1]==label_six:
				objs[i][1]=label_seven
			elif objs[i][1]==label_seven:
				objs[i][1]=label_eight
			elif objs[i][1]==label_eight:
				objs[i][1]=label_one

def on_mouse(event, x, y, flag, param):
	global point, objs, hidden, currentPoint, obj
	if event == cv2.EVENT_MOUSEMOVE:
		refresh(x, y)

	if flag==10:
		if event == cv2.EVENT_MOUSEMOVE:
			changeLocation(x, y)
			refresh()
	else:

		if event == cv2.EVENT_LBUTTONDOWN:
			# 删除点
			if flag == 9:

				if delObj(x, y):
					currentPoint = 0
					obj = []
				refresh()     
			# 更改属性
			elif flag == 33: # alt__33, shift__17
				changeHidden(x, y)
				refresh()
			
			elif flag == 1:
				hidden = False
				addPoint(x, y, hidden)
				refresh()
		if event == cv2.EVENT_RBUTTONDOWN:

			if flag==34:
				chlaebl(x,y)
				refresh()
				
			else:
				hidden = True
				addPoint(x, y, hidden)
				refresh()

	if currentPoint >= num:
		currentPoint = 0
		obj = []

num = int(sys.argv[2]) if len(sys.argv) > 2 else 3
path = path + "/" if not path.endswith("/") else path

className = []
className_hz = []
basic = 0

listarr = className_list.split("\n")
for i in range(len(listarr)):
	if listarr[i].find("=") != -1:
		tarr = listarr[i].split("=")
		className.append(tarr[0])
		className_hz.append(tarr[1])

stop = False
imgs = []

print(path)
for root, dir, files in os.walk(path):
	print(files)
	for file in files:
		imgs.append(root + '/' + file)

print(path)

#imgs = [path + imgs[i] for i in range(len(imgs))]

for i in range(len(imgs)-1, -1, -1):
	if not imgs[i].lower().endswith("jpg") and not imgs[i].lower().endswith("png") and not imgs[i].lower().endswith("jpeg"):
		del imgs[i]

colors = []
getColor(0, len(className))

for i in range(len(className)):
	colors.append(getColor(i))

obj = []
objs = []
point = []
currentImg = 0
currentPoint = 0
currentClass = 0
hidden = False

cv2.namedWindow("8", cv2.WINDOW_NORMAL)
currentImg = int(loadBreakPoint())

if path + f_name in imgs:
	currentImg = imgs.index(path + f_name)
	
while True:
	currentImg = 0 if currentImg < 0 else (len(imgs)-1 if currentImg >= len(imgs) else currentImg)
	# 图片变换,但是需要重新去取图片文件
	print(imgs)

	img = cv2.imdecode(np.fromfile(imgs[currentImg], dtype=np.uint8), -1)
	bak = cv2.imdecode(np.fromfile(imgs[currentImg], dtype=np.uint8), -1)

	objs = loadTxt(currentImg)
	
	
	while True: 
		
		refresh()
		cv2.setMouseCallback("image", on_mouse)

		key = cv2.waitKey(0)

		if key == 44 :
			currentImg = currentImg - 1
			if currentImg < 0:
				currentImg = len(imgs) -1
			objs = []
			break

		if key ==46 or key == ord('s'):
			currentImg = currentImg + 1
			if currentImg >= len(imgs):
				currentImg = 0
			objs = []
			break
		if key == ord('r'):
			obj = []
			currentPoint = 0
			os.remove(imgs[currentImg])
			if os.path.exists(os.path.splitext(imgs[currentImg])[0] + '.xml'):
				os.remove(os.path.splitext(imgs[currentImg])[0] + '.xml')
			if os.path.exists(os.path.splitext(imgs[currentImg])[0] + '.txt'):
				os.remove(os.path.splitext(imgs[currentImg])[0] + '.txt')
			del imgs[currentImg]

			if currentImg >= len(imgs) -1:
				currentImg = 0
			obj = []
			objs = []
			break

		if key == ord('c'):
			objs = []

		if key >= ord('0') and key <= ord('9'):
			if key == ord('0'):
				currentClass = 9
			else:
				currentClass = key - ord('1')
			

		if key == 27:
			stop = True
			saveBreakPoint()
			break

		if key == ord('w'):
			currentImg = currentImg - 1
			if currentImg < 0:
				currentImg = len(imgs) -1
			currentPoint=0
			obj = []
			objs = []
			break
		   
		if key == ord(' '):
			#saveToXml()
			saveToTxt(img.shape[1], img.shape[0])
			saveBreakPoint()
			currentPoint = 0
			
			objs = []
			obj = []
			currentImg = currentImg + 1
			if currentImg >= len(imgs):
				currentImg = 0
			break
		if key == ord('u'):	
			if basic == 0:
				basic = 10
			elif basic == 10:
				basic = 20
			else:
				basic = 0

		if key == ord("i"):
			pass

		if key == ord('a'):
			if not model == "cube" or model == "point":
				num = num + 1

		if key == ord('q'):
			if not model == "cube" or model == "point":
				num = num - 1
				if num < 1:
					num = 1

		if key == ord('b'):
			if model =="cube":
				model ='point'
				if not currentPoint == num and not currentPoint == 0:
					objs.pop()
				obj=[]
				currentPoint=0
				
			else:
				model = 'cube'				
				if not currentPoint == num and not currentPoint == 0:
					objs.pop()
				obj=[]
				currentPoint=0
				num = 3
	if stop:
		break

cv2.destroyAllWindows()
