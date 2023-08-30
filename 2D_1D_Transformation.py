#Variables:
#z - a two-dimensional position
#r - a counter-clockwise rotation from facing along the y-axis
#c - a focal length

import math
import numpy as np

def camera_r0_z0_c1(xx, xy):
    x = xx/xy
    return x

def camera_r0_z0(c, xx, xy):
    p = camera_r0_z0_c1(c*xx, c*xy)
    x = c * p
    return x

def camera_r0(zx, zy, c, xx, xy):
    p = camera_r0_z0(c, xx-zx, xy-zy)
    return p

def rotate_x_around_z_by_r(xx, xy, zx, zy, r):
    F = np.array([[1,0,-zx], [0,1,-zy], [0,0,1]])
    B = np.array([[1,0,zx], [0,1,zy], [0,0,1]])
    R = np.array([[np.cos(r),-np.sin(r),0], [np.sin(r),np.cos(r),0], [0,0,1]])
    P = np.array([[xx], [xy], [1]])
    BRFP = B @ R @ F @ P
    BRFPx = BRFP[0,0]/BRFP[2,0]
    BRFPy = BRFP[1,0]/BRFP[2,0]
    return (BRFPx, BRFPy)

def camera(r, zx, zy, c, xx, xy):
    rotx, roty = rotate_x_around_z_by_r(xx, xy, zx, zy, -r)
    x = camera_r0(zx, zy, c, rotx, roty)
    return x



if __name__ == '__main__':
    test1 = camera_r0_z0_c1(10,5)
    print(test1)
    #should be: 2

    test2 = camera_r0_z0(0.5, 10, 5)
    print(test2)
    #should be: 1

    test3 = camera_r0(2, 3, 2, 10, 5)
    print(test3)
    #should be:

    test4x, test4y = rotate_x_around_z_by_r(2, 3, 1, 1, math.radians(90))
    print(test4x, test4y)

    test5 = camera(math.radians(45), 1, 1, math.sqrt(2), 1, 8)
    print(test5)
    print(math.sqrt(2))

    #should be: sqrt(2)



