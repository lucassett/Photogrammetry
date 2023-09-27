#Extending the 2D camera into 3D, using matrix form rewrite from 2D_1D_Transformation.py

import math
import numpy as np
rad = math.radians

def Rx(roll):
    return np.array([
        [1, 0, 0],
        [0, np.cos(roll), -np.sin(roll)],
        [0, np.sin(roll), np.cos(roll)],
    ])

def Ry(pitch):
    return np.array([
        [np.cos(pitch), 0, np.sin(pitch)],
        [0, 1, 0],
        [-np.sin(pitch), 0, np.cos(pitch)],
    ])

def Rz(yaw):
    return np.array([
        [np.cos(yaw), -np.sin(yaw), 0],
        [np.sin(yaw), np.cos(yaw), 0],
        [0, 0, 1],
    ])

def R(roll, pitch, yaw):
    rotx = Rx(roll)
    roty = Ry(pitch)
    rotz = Rz(yaw)
    return rotx @ roty @ rotz

def extrinsic(zx, zy, zz, roll, pitch, yaw):
    '''
    With 0 rotation, the camera points along the object x-axis, and down is the positive z-axis. The camera rotates:
    1) around the z axis
    2) around the y' axis
    3) around the x'' axis
    :param zx: x position of camera
    :param zy: y position of camera
    :param zz: z position of camera
    :param theta: angle the camera is rotated
    :return: Extrinsic matrix in form:
        [R -Rz]
        [0 0 0 1]
        where R is a 3x3 matrix formed from Rx @ Ry @ Rz, and -Rz is a 3x1 vector of position in x, y, and z.
        Final result: 4x4 extrinsic matrix
    '''
    rot_mtx = R(roll, pitch, yaw)
    pos_vec = rot_mtx @ np.array([[zx], [zy], [zz]])
    ext_mtx = np.block([
        [rot_mtx, -pos_vec],
        [0, 0, 0, 1],
    ])
    return ext_mtx

def intrinsic(focal_length, principal_offset_x, principal_offset_y):
    return np.array([
        [focal_length, 0, principal_offset_x],
        [0, focal_length, principal_offset_y],
        [0, 0, 1],
    ])
def hc(inhomogeneous_coord):
    return np.append(np.asarray(inhomogeneous_coord), 1)

#Inhomogeneous Coordinates
def ic(homogeneous_coord):
    return homogeneous_coord[:-1] / homogeneous_coord[-1]

def CAMERA(cx, cy, cz, roll, pitch, yaw, c, hx, hy):
    return intrinsic(c, hx, hy) @ np.eye(3,4) @ extrinsic(cx, cy, cz, roll, pitch, yaw)



if __name__ == '__main__':
    ext_test = extrinsic(0, 0, 0, rad(0), rad(0), rad(0))
    stophere=1

    with open('HW3_input.csv') as csv:
        for line in csv:
            #print(line)
            parameters = []
            dpt = line.split(',')       #Returns list of strings
            if dpt[0]=='cam_x':
                continue

            for element in range(len(dpt)):
                fdpt = float(dpt[element])
                parameters.append(fdpt)

            cam_x, cam_y, cam_z, yaw, pitch, roll, cam_c, pp_x, pp_y, p_x, p_y, p_z, img_x, img_y = parameters
            #csv_test = CAMERA(cam_x, cam_y, cam_z, 'R', cam_c, pp_x, pp_y)

            ext_mtx = extrinsic(cam_x, cam_y, cam_z, roll, pitch, yaw)
            img_point = hc([p_x, p_y, p_z])
            test_ext = ext_mtx @ img_point
            reduced = np.eye(3,4) @ test_ext
            int_mtx = intrinsic(cam_c,pp_x, pp_y)
            homogeneous_ans = int_mtx @ reduced
            stophere = 1
            #unit_cam_ans = ic(reduced)

