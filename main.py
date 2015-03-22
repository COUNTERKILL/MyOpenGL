import rasterizator
import vertexShader as vs
import numpy as np
import Image, ImageDraw, math

vs.SetLookAtLH(np.array([-5, 2, -5], dtype=float), np.array([0, -2, 10], dtype=float), np.array([0, 1, 0], dtype=float))
vs.SetPerspectiveFovLH(math.pi/4, 1.0, 2.0, 20.0)



#vecInView = np.dot(np.array([-1, -2, 5, 1], dtype=float), vs.MATRIX_VIEW)


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


Vs = []
Vs.append(Vertex(-10,10,15, 0, 0))
Vs.append(Vertex(10,8,15, 0.9766, 0.1953))
Vs.append(Vertex(0,-5,15, 0.4882, 0.9766))

a = []
for i in range(0, 3):
	a.append(np.array([Vs[i].x, Vs[i].y, Vs[i].z, 1]))
	a[i] = np.dot(a[i], vs.MATRIX_VIEW)
	a[i] = vs.NormilizeFromW(np.dot(a[i], vs.MATRIX_PROJECTION))

	Vs[i].x = a[i][0]
	Vs[i].y = a[i][1]
	Vs[i].z = a[i][2]
	print(Vs[i].x, Vs[i].y, Vs[i].z)
	Vs[i].x = int((Vs[i].x + 1) * 200)
	Vs[i].y = int((Vs[i].y + 1) * 200)
	print(Vs[i].x, Vs[i].y, Vs[i].z)
image = Image.new("RGBA", (1024,1024), (0,0,0,0))

rasterizator.DrawPoly(image, Vs[0], Vs[1], Vs[2])
for x in range(0, rasterizator.SCREEN.shape[0]):
	for y in range(0, rasterizator.SCREEN.shape[1]):
		image.putpixel((x, 1023-y), tuple(rasterizator.SCREEN[x, y]))
image.show()
image.save("C:\img.png", "PNG")
del image

# 