from __future__ import division
import Image, ImageDraw, math

class Vertex:
	def __init__(self, x, y, z, color):
		self.x = x
		self.y = y
		self.z = z
		self.color = color
		return
	x = 0
	y = 0
	z = 0
	texCoordU = 0
	texCoordV = 0
	color = (0, 0, 0)
#end class Vertex	
	
	
	
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
				image.putpixel((v0.x, y), v1.color)
		else:
			s = dy/dx
			if v0.x > v1.x:
				step = -1
			else:
				step = 1
			for x in range(v0.x, v1.x, step):
				y = int(s * (x - v0.x) + v0.y);
				image.putpixel((x, y), v1.color)
	else:
		if dy==0:
			if v0.x > v1.x:
				step = -1
			else:
				step = 1
			for x in range(v0.x, v1.x, step):
				image.putpixel((x, v0.y), v1.color)
		else:
			s = dx/dy
			if v0.y > v1.y:
				step = -1
			else:
				step = 1
			for y in range(v0.y, v1.y, step):
				x = int(s * (y - v0.y) + v0.x);
				image.putpixel((x, y), v1.color)
	return;
#end drawLine

def RasterizationPoly(image, v1, v2, v3):
	if hasattr(v1, "texCoordU"):
		print "texcoord"
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
		for dy in range(0, vHight.y - vMiddle.y):
			x1 = int(beta * (dy + vMiddle.y - vLow.y)) + vLow.x
			x2 = int(alpha * dy) + vMiddle.x
			if x1 > x2:
				step = -1
			else:
				step = 1
			for x in range(x1, x2, step):
				y = vMiddle.y + dy
				distToV1 = math.sqrt(((x - v1.x)**2) + ((y - v1.y)**2))
				distToV2 = math.sqrt(((x - v2.x)**2) + ((y - v2.y)**2))
				distToV3 = math.sqrt(((x - v3.x)**2) + ((y - v3.y)**2))
				allDist = distToV1 + distToV2 + distToV3
				colorSet1 = [0,0,0]
				colorSet2 = [0,0,0]
				colorSet3 = [0,0,0]
				colorSet = [0,0,0]
				for i in range(0, 3): 
					colorSet1[i] = v1.color[i] * (distToV1/allDist) # color from 1 vertex
					colorSet2[i] = v2.color[i] * (distToV2/allDist) # color from 2 vertex
					colorSet3[i] = v3.color[i] * (distToV3/allDist) # color from 3 vertex
				for i in range(0, 3): 
					colorSet[i] = colorSet1[i] + colorSet2[i] + colorSet3[i]
				color = tuple(int(i) for i in colorSet)
				image.putpixel((x, y), color)
	if not breakLow:
		# hight part of poly
		alpha = (vMiddle.x - vLow.x)/(vMiddle.y - vLow.y)
		beta = (vHight.x - vLow.x)/(vHight.y - vLow.y)
		for dy in range(0, vMiddle.y - vLow.y):
			x1 = int(beta * dy) + vLow.x
			x2 = int(alpha * dy) + vLow.x
			if x1 > x2:
				step = -1
			else:
				step = 1
			for x in range(x1, x2, step):
				y = vLow.y + dy
				distToV1 = math.sqrt(((x - v1.x)**2) + ((y - v1.y)**2))
				distToV2 = math.sqrt(((x - v2.x)**2) + ((y - v2.y)**2))
				distToV3 = math.sqrt(((x - v3.x)**2) + ((y - v3.y)**2))
				allDist = distToV1 + distToV2 + distToV3
				colorSet1 = [0,0,0]
				colorSet2 = [0,0,0]
				colorSet3 = [0,0,0]
				colorSet = [0,0,0]
				for i in range(0, 3): 
					colorSet1[i] = v1.color[i] * (distToV1/allDist) # color from 1 vertex
					colorSet2[i] = v2.color[i] * (distToV2/allDist) # color from 2 vertex
					colorSet3[i] = v3.color[i] * (distToV3/allDist) # color from 3 vertex
				for i in range(0, 3): 
					colorSet[i] = colorSet1[i] + colorSet2[i] + colorSet3[i]
				color = tuple(int(i) for i in colorSet)
				image.putpixel((x, y), color)

# DrawPoly
def DrawPoly(image, v1, v2, v3):
	#DrawLine(image, v1, v2, color)
	#DrawLine(image, v2, v3, color)
	#DrawLine(image, v1, v3, color)
	RasterizationPoly(image, v1, v2, v3)
	return;
#end DrawPoly


image = Image.new("RGBA", (1024,1024), (0,0,0,0))

(width, height) = image.size
# fill image gray color
for i in range(0, width):
	for j in range(0, height):
		image.putpixel((i, j), (100, 100, 100))
#for i in range(0, width):
 # image.putpixel((i, i), (0, 255, 0))

color = (0, 0, 255)
v1 = Vertex(100,100,0,(255, 0, 0))
v2 = Vertex(1000,200,0,(0, 255, 0))
#DrawLine(image, v1, v2, color)
v3 = Vertex(500,500,0,(0, 0, 255))
DrawPoly(image, v1, v2, v3)
#draw = ImageDraw.Draw(image)
#draw. ellipse((10,10,300,300), fill="white", outline="red")
#del draw
#image.save("test.png", "PNG")
image.show()
image.save("C:\img.png", "PNG")
del image
if hasattr(Vertex, "text"):
	print 123