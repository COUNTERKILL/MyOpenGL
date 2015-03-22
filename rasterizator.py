from __future__ import division
import Image, ImageDraw, math
import numpy as np
TEXTURE = Image.Image()

SCREEN = np.zeros((1024, 1024, 3), dtype=int)
ZBUFFER = np.zeros((1024, 1024, 3), dtype=float)
# fill image gray color
SCREEN.fill(80)

class Vertex:
	def __init__(self, x, y, z, color):
		self.x = x
		self.y = y
		self.z = z
		self.color = color
		return
	def __init__(self, x, y, z, u, v):
		self.x = x
		self.y = y
		self.z = z
		self.u = u
		self.v = v
		return
	x = 0.0
	y = 0.0
	z = 0.0
	u = 0.0
	v = 0.0
	color = (0, 0, 0)
#end class Vertex	
	
# get point intersection normal from point to line with this line
# v0 - point
# v1, v2 - point of line
def GetPointIntersectionNormalLine(v0, v1, v2):
	l = math.sqrt(((v0.x - v1.x) ** 2) + ((v0.y - v1.y) ** 2))
	l1 = math.sqrt(((v0.x - v2.x) ** 2) + ((v0.y - v2.y) ** 2))
	l3 = math.sqrt(((v1.x - v2.x) ** 2) + ((v1.y - v2.y) ** 2))
	
	x1 = (l*l - l1*l1 + l3*l3) / (2.0 * l3) # dist from Normal intersection point to v1
	x2 = l3 - x1 # dist from Normal intersection point to v2
	x = (x1/(x1+x2)) * v2.x + (x2/(x1+x2)) * v1.x
	y = (x1/(x1+x2)) * v2.y + (x2/(x1+x2)) * v1.y
	retV = Vertex(0, 0, 0, (0, 0, 0)) # because will not defined in this file
	retV.x = x
	retV.y = y
	return retV
	
	
# Brezencham algorythm
def DrawLine(image, v0, v1):
	dx = (v1.x-v0.x)
	dy = (v1.y-v0.y)
	if abs(dx) > abs(dy):
		if dx==0:
			if v0.y > v1.y:
				step = -1
			else:
				step = 1
			for y in range(v0.y, v1.y, step):
				SCREEN[x, y] = v1.color
		else:
			s = dy/dx
			if v0.x > v1.x:
				step = -1
			else:
				step = 1
			for x in range(v0.x, v1.x, step):
				y = int(s * (x - v0.x) + v0.y);
				SCREEN[x, y] = v1.color
	else:
		if dy==0:
			if v0.x > v1.x:
				step = -1
			else:
				step = 1
			for x in range(v0.x, v1.x, step):
				SCREEN[x, y] = v1.color

		else:
			s = dx/dy
			if v0.y > v1.y:
				step = -1
			else:
				step = 1
			for y in range(v0.y, v1.y, step):
				x = int(s * (y - v0.y) + v0.x);
				SCREEN[x, y] = v1.color
	return;
#end drawLine

def RasterizationPoly(image, v1, v2, v3):
	if v1.y > v2.y:
		if v1.y > v3.y:
			vHight = v1
			if v3.y > v2.y:
				vMiddle = v3
				vLow = v2
			else:
				vMiddle = v2
				vLow = v3
		else:
			vMiddle = v1
			vLow = v2
			vHight = v3
	else:
		if v2.y > v3.y:
			vHight = v2
			if v3.y > v1.y:
				vMiddle = v3
				vLow = v1
			else:
				vMiddle = v1
				vLow = v3
		else:
			vMiddle = v2
			vLow = v1
			vHight = v3
	breakLow = False
	breakHight = False
	if vMiddle.y == vLow.y:
		breakLow = True
	if vMiddle.y == vHight.y:
		breakHight = True
	if not breakHight:
		# low part of poly
		alpha = (vHight.x - vMiddle.x)/(vHight.y - vMiddle.y)
		beta = (vHight.x - vLow.x)/(vHight.y - vLow.y)
		
		# texCoord is defined
		if hasattr(v1, "u"):
			alphaT = (vHight.u - vMiddle.u)/(vHight.v - vMiddle.v)
			betaT = (vHight.u - vLow.u)/(vHight.v - vLow.v)
			kT = vHight.v - vMiddle.v
			k = vHight.y - vMiddle.y
		for dy in range(0, vHight.y - vMiddle.y):
			x1 = int(beta * (dy + vMiddle.y - vLow.y)) + vLow.x
			x2 = int(alpha * dy) + vMiddle.x
			if hasattr(v1, "u"):
				x1T = betaT * (dy * (vHight.v - vMiddle.v)/(vHight.y - vMiddle.y) + vMiddle.v - vLow.v) + vLow.u
				x2T = alphaT * dy * (vHight.v - vMiddle.v)/(vHight.y - vMiddle.y) + vMiddle.u
				xTdX = abs((x2T -x1T)/(x2-x1+0.001))
			if x1 > x2:
				step = -1
			else:
				step = 1
			y = vMiddle.y + dy
			for x in range(x1, x2, step):
				colorSet = [0,0,0]
				# texCoord is defined
				if hasattr(v1, "v"):
					xT = (x - x1) * xTdX + x1T
					yT = vMiddle.v + (kT/k) * dy
					(width, height) = TEXTURE.size
					iyT = int(height * yT)
					ixT = int(width * xT)
					colorSet[0], colorSet[1], colorSet[2]  = TEXTURE.getpixel((ixT, iyT))
				else:
					v0 = Vertex(0, 0, 0, (0, 0, 0))
					v0.x = x
					v0.y = y
					
					pV1toV2 = GetPointIntersectionNormalLine(v3, v1, v2)
					pV2toV3 = GetPointIntersectionNormalLine(v1, v2, v3)
					pV1toV3 = GetPointIntersectionNormalLine(v2, v1, v3)
					
					pTopV1toV2 = GetPointIntersectionNormalLine(v0, v3, pV1toV2) # point intersection perp from pixel to perp from v3 to v1-v2 line. 0_o
					pTopV2toV3 = GetPointIntersectionNormalLine(v0, v1, pV2toV3)
					pTopV1toV3 = GetPointIntersectionNormalLine(v0, v2, pV1toV3)
					
					distToV1 = math.sqrt(((pTopV2toV3.x - v1.x)**2) + ((pTopV2toV3.y - v1.y)**2))
					distToV2 = math.sqrt(((pTopV1toV3.x - v2.x)**2) + ((pTopV1toV3.y - v2.y)**2))
					distToV3 = math.sqrt(((pTopV1toV2.x - v3.x)**2) + ((pTopV1toV2.y - v3.y)**2))
					
					distV1toP = math.sqrt(((pV2toV3.x - v1.x)**2) + ((pV2toV3.y - v1.y)**2))
					distV2toP = math.sqrt(((pV1toV3.x - v2.x)**2) + ((pV1toV3.y - v2.y)**2))
					distV3toP = math.sqrt(((pV1toV2.x - v3.x)**2) + ((pV1toV2.y - v3.y)**2))
					
					colorSet1 = [0,0,0]
					colorSet2 = [0,0,0]
					colorSet3 = [0,0,0]
					for i in range(0, 3): 
						colorSet1[i] = v1.color[i] * (1.0 - distToV1/distV1toP) # color from 1 vertex
						colorSet2[i] = v2.color[i] * (1.0 - distToV2/distV2toP) # color from 2 vertex
						colorSet3[i] = v3.color[i] * (1.0 - distToV3/distV3toP) # color from 3 vertex
					for i in range(0, 3): 
						colorSet[i] = colorSet1[i] + colorSet2[i] + colorSet3[i]
				color = tuple(int(i) for i in colorSet)
				SCREEN[x, y] = color
				
	if not breakLow:
		# hight part of poly
		alpha = (vMiddle.x - vLow.x)/(vMiddle.y - vLow.y)
		beta = (vHight.x - vLow.x)/(vHight.y - vLow.y)
		# texCoord is defined
		if hasattr(v1, "u"):
			alphaT = (vMiddle.u - vLow.u)/(vMiddle.v - vLow.v)
			betaT = (vHight.u - vLow.u)/(vHight.v - vLow.v)
			kT = vMiddle.v - vLow.v
			k = vMiddle.y - vLow.y
		for dy in range(0, vMiddle.y - vLow.y):
			x1 = int(beta * dy) + vLow.x
			x2 = int(alpha * dy) + vLow.x
			if hasattr(v1, "u"):
				x1T = betaT * (dy * (vMiddle.v - vLow.v)/(vMiddle.y - vLow.y)) + vLow.u
				x2T = alphaT * dy * (vMiddle.v - vLow.v)/(vMiddle.y - vLow.y) + vLow.u
				xTdX = abs((x2T - x1T)/(x2-x1+0.001))
				
			if x1 > x2:
				step = -1
			else:
				step = 1
			for x in range(x1, x2, step):
				y = vLow.y + dy
				colorSet = [0,0,0]
				# texCoord is defined
				if hasattr(v1, "v"):
					xT = (x - x1) * xTdX + x1T
					yT = vLow.v + (kT/k) * dy
					(width, height) = TEXTURE.size
					iyT = int(height * yT)
					ixT = int(width * xT)
					colorSet[0], colorSet[1], colorSet[2]  = TEXTURE.getpixel((ixT, iyT))
				else:
					v0 = Vertex(0, 0, 0, (0, 0, 0))
					v0.x = x
					v0.y = y
					
					pV1toV2 = GetPointIntersectionNormalLine(v3, v1, v2)
					pV2toV3 = GetPointIntersectionNormalLine(v1, v2, v3)
					pV1toV3 = GetPointIntersectionNormalLine(v2, v1, v3)
					
					pTopV1toV2 = GetPointIntersectionNormalLine(v0, v3, pV1toV2) # point intersection perp from pixel to perp from v3 to v1-v2 line. 0_o
					pTopV2toV3 = GetPointIntersectionNormalLine(v0, v1, pV2toV3)
					pTopV1toV3 = GetPointIntersectionNormalLine(v0, v2, pV1toV3)
					
					distToV1 = math.sqrt(((pTopV2toV3.x - v1.x)**2) + ((pTopV2toV3.y - v1.y)**2))
					distToV2 = math.sqrt(((pTopV1toV3.x - v2.x)**2) + ((pTopV1toV3.y - v2.y)**2))
					distToV3 = math.sqrt(((pTopV1toV2.x - v3.x)**2) + ((pTopV1toV2.y - v3.y)**2))
					
					distV1toP = math.sqrt(((pV2toV3.x - v1.x)**2) + ((pV2toV3.y - v1.y)**2))
					distV2toP = math.sqrt(((pV1toV3.x - v2.x)**2) + ((pV1toV3.y - v2.y)**2))
					distV3toP = math.sqrt(((pV1toV2.x - v3.x)**2) + ((pV1toV2.y - v3.y)**2))
					
					colorSet1 = [0,0,0]
					colorSet2 = [0,0,0]
					colorSet3 = [0,0,0]
					
					for i in range(0, 3): 
						colorSet1[i] = v1.color[i] * (1.0 - distToV1/distV1toP) # color from 1 vertex
						colorSet2[i] = v2.color[i] * (1.0 - distToV2/distV2toP) # color from 2 vertex
						colorSet3[i] = v3.color[i] * (1.0 - distToV3/distV3toP) # color from 3 vertex
					for i in range(0, 3): 
						colorSet[i] = colorSet1[i] + colorSet2[i] + colorSet3[i]
				color = tuple(int(i) for i in colorSet)
				SCREEN[x, y] = color
				

# DrawPoly
def DrawPoly(image, v1, v2, v3):
	#DrawLine(image, v1, v2, color)
	#DrawLine(image, v2, v3, color)
	#DrawLine(image, v1, v3, color)
	RasterizationPoly(image, v1, v2, v3)
	return;
#end DrawPoly


image = Image.new("RGBA", (1024,1024), (0,0,0,0))
TEXTURE = Image.open("texture.jpg")

(width, height) = image.size

#for i in range(0, width):
 # image.putpixel((i, i), (0, 255, 0))

color = (0, 0, 255)
v1 = Vertex(10,10,0, 0, 0)
v2 = Vertex(1000,200,0, 0.9766, 0.1953)
#DrawLine(image, v1, v2, color)
v3 = Vertex(500,1000,0, 0.4882, 0.9766)
DrawPoly(image, v1, v2, v3)
#draw = ImageDraw.Draw(image)
#draw. ellipse((10,10,300,300), fill="white", outline="red")
#del draw
#image.save("test.png", "PNG")

if hasattr(Vertex, "text"):
	print 123
for x in range(0, SCREEN.shape[0]):
	for y in range(0, SCREEN.shape[1]):
		image.putpixel((x, y), tuple(SCREEN[x, y]))
image.show()
image.save("C:\img.png", "PNG")
del image