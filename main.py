import rasterizator
import VertexShader as vs

vs.SetLookAtLH(np.array([0, 2, -5], dtype=float), np.array([0, 0, 2], dtype=float), np.array([0, 1, 0], dtype=float))
vs.SetPerspectiveFovLH(math.pi/4, 1.0, 2.0, 10.0)



vecInView = np.dot(np.array([-1, -2, 5, 1], dtype=float), MATRIX_VIEW)