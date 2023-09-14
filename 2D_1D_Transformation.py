#Variables:
#z - a two-dimensional position
#r - a counter-clockwise rotation from facing along the y-axis
#c - a focal length

#Functions build a camera function step-by-step by starting from the most defined parameters and generalizing.
    #Function 1: Rotation (r), camera position (z) and focal length (c) are defined - solve for given point
    #Function 2: Rotation (r) and camera position (z) are defined - solve for given point, with scalar effects by c
    #Function 3: Rotation (r) is defined - solve for given point and scalar effects, also depending on camera's actual location
    #Function 4: General camera function - solve for given point based on variable scalar effects, camera location, and
        #   camera-facing direction
    #Rotation Function - defines standard 2D rotation matrix

import math
import numpy as np

def camera_r0_z0_c1(xx, xy):
    '''Project a point (x,y) in the 2D world onto a 1D surface (a line), located 1 unit away from the camera (c=1; aka focal length).
        The camera is located at the origin (z=0), and is looking along the y axis (r=0).'''
    x = xx/xy
    return x

def camera_r0_z0(c, xx, xy):
    '''Project a point (x,y) in the 2D world onto a 1D surface (a line), located a variable distance from the camera (c).
        The camera is located at the origin (z=0), and is looking along the y axis (r=0).
        c has the effect of a scalar factor on the projection of point (x,y).'''
    p = camera_r0_z0_c1(c*xx, c*xy)
    x = c * p
    return x

def camera_r0(zx, zy, c, xx, xy):
    '''Project a point (x,y) in the 2D world onto a 1D surface (a line), located a variable distance from the camera (c).
            The camera is located at z, and is looking along the y axis (r=0).'''
    p = camera_r0_z0(c, xx-zx, xy-zy)
    return p

def rotate_x_around_z_by_r(xx, xy, zx, zy, r):
    '''2D rotation matrix (R) defined. Matrices multiplied in steps:
            1) Translate point to origin
            2) Rotate around origin
            3) Translate back (in new frame)
        MULTIPLICATION:  Translate Back * (Rotate * (Translate away * (Camera Matrix)))'''
    F = np.array([[1,0,-zx], [0,1,-zy], [0,0,1]])
    B = np.array([[1,0,zx], [0,1,zy], [0,0,1]])
    R = np.array([[np.cos(r),-np.sin(r),0], [np.sin(r),np.cos(r),0], [0,0,1]])
    P = np.array([[xx], [xy], [1]])
    BRFP = B @ R @ F @ P
    BRFPx = BRFP[0,0]/BRFP[2,0]
    BRFPy = BRFP[1,0]/BRFP[2,0]
    return (BRFPx, BRFPy)

def camera(r, zx, zy, c, xx, xy, h=0):
    '''General camera function. Camera is located at z, facing a direction rotated r degrees from the y axis. For function
        to work, remember: CONVERT DEGREES TO RADIANS. The focal length is c. H is the principal offset - when applying
        pixels to the camera, h is used to help define offset as a result of defining pixel space (Does the edge matter?
        Does the center?).'''
    rotx, roty = rotate_x_around_z_by_r(xx, xy, zx, zy, -r)
    x = camera_r0(zx, zy, c, rotx, roty) + h
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
    #should be: 8

    test4x, test4y = rotate_x_around_z_by_r(2, 3, 1, 1, math.radians(90))
    print(test4x, test4y)
    #should be: -1, 2

    test5 = camera(math.radians(45), 1, 1, math.sqrt(2), 1, 8)
    print(test5)
    print(math.sqrt(2))

    #should be: sqrt(2)


#Read a .csv file with each parameter, and use to solve projection of point (x,y) given the data in the file. 
    with open('input.csv') as csv:
        for line in csv:
            #print(line)
            parameters = []
            dpt = line.split(',')       #Returns list of strings
            if dpt[0]=='cam_x':
                continue

            for element in dpt[:-1]:
                fdpt = float(element)
                parameters.append(fdpt)

            cam_x, cam_y, cam_r, cam_c, cam_h, p_x, p_y, img_x = parameters
            csv_test = camera(math.radians(cam_r), cam_x, cam_y, cam_c, p_x, p_y, cam_h)
            error=csv_test - img_x
            print(csv_test, error)





