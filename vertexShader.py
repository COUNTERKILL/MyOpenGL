import numpy as np

matWorld = np.eye(4)
matWorld[3, 0] = 5
matWorld[3, 1] = 6
matWorld[3, 2] = 7
vector = np.ones((1, 4))
print(vector)
print(matWorld)
print('Multiple: ')
print(np.dot(vector, matWorld))

