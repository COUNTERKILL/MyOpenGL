from __future__ import division
import Image, ImageDraw

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
	color = (0, 0, 0)
#end class Vertex	
	
	
	
# Brezencham algorythm
def DrawLine(image, v0, v1, color):
	dx = (v1.x-v0.x)
	dy = (v1.y-v0.y)
	if dx > dy:
		if dx==0:
			for y in range(v0.y, v1.y):
				image.putpixel((v0.x, y), color)
		else:
			s = dy/dx
			for x in range(v0.x, v1.x):
				y = int(s * (x - v0.x) + v0.y);
				image.putpixel((x, y), color)
	else:
		if dy==0:
			for x in range(v0.x, v1.x):
				image.putpixel((x, v0.y), color)
		else:
			s = dx/dy
			for y in range(v0.y, v1.y):
				x = int(s * (y - v0.y) + v0.x);
				image.putpixel((x, y), color)
	return;
#end drawLine


# DrawPoly
def DrawPoly(image, v1, v2, v3, color):
	DrawLine(image, v1, v2, color)
	DrawLine(image, v2, v3, color)
	DrawLine(image, v1, v3, color)
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
v1 = Vertex(100,100,100,(0, 0, 255))
v2 = Vertex(1000,100,100,(0, 0, 255))
#DrawLine(image, v1, v2, color)
v3 = Vertex(500,500,100,(0, 0, 255))
DrawPoly(image, v1, v2, v3, color)
#draw = ImageDraw.Draw(image)
#draw. ellipse((10,10,300,300), fill="white", outline="red")
#del draw
#image.save("test.png", "PNG")
image.show()
image.save("C:\img.png", "PNG")
del image