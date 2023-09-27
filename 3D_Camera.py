#Extending the 2D camera into 3D, using matrix form rewrite from 2D_1D_Transformation.py

import math
import numpy as np
rad = math.radians

def extrinsic(zx, zy, zz, theta):
    Rx = np.array([
        [1, 0, 0],
        [0, np.cos(theta), -np.sin(theta)],
        [0, np.sin(theta), np.cos(theta)],
    ])
    Ry = np.array([
        [np.cos(theta), 0, np.sin(theta)],
        [0, 1, 0],
        [-np.sin(theta), 0, np.cos(theta)],
    ])
    Rz = np.array([
        [np.cos(theta), -np.sin(theta), 0],
        [np.sin(theta), np.cos(theta), 0],
        [0, 0, 1],
    ])
    R = Rx @ Ry @ Rz
    Rpos = R @ np.array([[zx], [zy], [zz]])
    ext_mtx = np.block([
        [R, -Rpos],
        [0, 0, 0, 1],
    ])

    return ext_mtx

if __name__ == '__main__':
    ext_test = extrinsic(0, 0, 0, rad(0))
    stophere=1