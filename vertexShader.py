from __future__ import division
import numpy as np
import math

np.set_printoptions(1)

MATRIX_VIEW = np.eye(4, dtype=float) # identity matrix
MATRIX_PROJECTION = np.eye(4, dtype=float)





# right = vUp * vLook

# yScale = cot(view angle)
# xScale = yScale/(width/heigth of screen)

def Normilize(vec):
	dim = 0.0
	for i in range(0, 3):
		dim = dim + vec[i] * vec[i]
	dim = math.sqrt(dim)
	vec[0] = vec[0]/dim
	vec[1] = vec[1]/dim
	vec[2] = vec[2]/dim
	return vec

def NormilizeFromW(vec):
	for i in range(0, 4):
		vec[i] = vec[i]/vec[3]
	return vec

	
def SetPerspectiveFovLH(angleOfView, aspectRatio, zNearPlane, zFarPlane):
	yScale = 1.0/math.tan(angleOfView)
	xScale = yScale/aspectRatio
	MATRIX_PROJECTION[0][0] = xScale
	MATRIX_PROJECTION[1][1] = yScale
	MATRIX_PROJECTION[2][2] = zFarPlane/(zFarPlane - zNearPlane)
	MATRIX_PROJECTION[3][2] = -1.0 * (zFarPlane * zNearPlane)/(zFarPlane - zNearPlane)
	MATRIX_PROJECTION[2][3] = 1 # 1/d: d - from (0,0,0) to projection plane
	MATRIX_PROJECTION[3][3] = 0

def SetLookAtLH(vPos, vAt, vUp):
	vLook = Normilize(vAt - vPos)
	# get right local vector
	vRight = np.cross(vUp, vLook)
	vRight = Normilize(vRight)
	#print("vRight: ")
	#print(vRight)
	vUp = np.cross(vLook, vRight)
	global MATRIX_VIEW
	
	# set view matrix
	for i in range(0, 3):
		MATRIX_VIEW[i][0] = vRight[i]
		print(i)
		MATRIX_VIEW[i][1] = vUp[i]
		MATRIX_VIEW[i][2] = vLook[i]
		
	dotProduct = np.dot(vRight, vPos)
	MATRIX_VIEW[3][0] = -1.0 * dotProduct
	#print("dotProduct: ")
	#print(dotProduct)
	dotProduct = np.dot(vUp, vPos)
	MATRIX_VIEW[3][1] = -1.0 * dotProduct
	
	dotProduct = np.dot(vLook, vPos)
	MATRIX_VIEW[3][2] = -1.0 * dotProduct
	

SetLookAtLH(np.array([0, 2, -5], dtype=float), np.array([0, 0, 2], dtype=float), np.array([0, 1, 0], dtype=float))
#print("Matrix projection: ")

SetPerspectiveFovLH(math.pi/4, 1.0, 2.0, 10.0)
#print(MATRIX_PROJECTION)

#print("Matrix view: ")
#print(MATRIX_VIEW)

#print("Vector in view: ")
vecInView = np.dot(np.array([-1, -2, 5, 1], dtype=float), MATRIX_VIEW)
#print(vecInView)

#print("Vector in projection: ")

#print(NormilizeFromW(np.dot(vecInView, MATRIX_PROJECTION)))

