from math import pi
import numpy as np
import cv2
import sys
import os

# Usage: 
#     Change main function with ideal arguments
#     then
#     python rotate_3d.py [name of the image] [degree to rotate]
#
# Parameters:
#     image     : the image that you want rotated
#     theta     : the rotation around the x axis
#     phi       : the rotation around the y axis
#     gamma     : the rotation around the z axis (basically a 2D rotation)
#     dx        : translation along the x axis
#     dy        : translation along the y axis
#     dz        : translation along the z axis (distance to the image)
#
# Output:
#     image     : the rotated image
# 
# Reference:
#     1.        : http://stackoverflow.com/questions/17087446/how-to-calculate-perspective-transform-for-opencv-from-rotation-angles
#     2.        : http://jepsonsblog.blogspot.tw/2012/11/rotation-in-3d-using-opencvs.html

""" Wrapper of Rotating a Image """

def rotate_along_axis(image, theta=0, phi=0, gamma=0, dx=0, dy=0, dz=0):
    
    # Get radius of rotation along 3 axes
    rtheta, rphi, rgamma = get_rad(theta, phi, gamma)
    
    # Height, Width, Channel
    height, width = image.shape[:2]
    
    # Get ideal focal length on z axis
    # NOTE: Change this section to other axis if needed
    d = np.sqrt(height**2 + width**2)
    focal = d / (2 * np.sin(rgamma) if np.sin(rgamma) != 0 else 1)
    dz = focal

    # Get projection matrix
    mat = get_M(rtheta, rphi, rgamma, dx, dy, dz, width, height, focal)
    
    return cv2.warpPerspective(image.copy(), mat, (width,height))


""" Get Respective Projection Matrix """

def get_M(theta, phi, gamma, dx, dy, dz, w, h, f):
    
    # Projection 2D -> 3D matrix
    A1 = np.array([ [1, 0, -w/2],
                    [0, 1, -h/2],
                    [0, 0, 1],
                    [0, 0, 1]])
    
    # Rotation matrices around the X, Y, and Z axis
    RX = np.array([ [1, 0, 0, 0],
                    [0, np.cos(theta), -np.sin(theta), 0],
                    [0, np.sin(theta), np.cos(theta), 0],
                    [0, 0, 0, 1]])
    
    RY = np.array([ [np.cos(phi), 0, -np.sin(phi), 0],
                    [0, 1, 0, 0],
                    [np.sin(phi), 0, np.cos(phi), 0],
                    [0, 0, 0, 1]])
    
    RZ = np.array([ [np.cos(gamma), -np.sin(gamma), 0, 0],
                    [np.sin(gamma), np.cos(gamma), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

    # Composed rotation matrix with (RX, RY, RZ)
    R = np.dot(np.dot(RX, RY), RZ)

    # Translation matrix
    T = np.array([  [1, 0, 0, dx],
                    [0, 1, 0, dy],
                    [0, 0, 1, dz],
                    [0, 0, 0, 1]])

    # Projection 3D -> 2D matrix
    A2 = np.array([ [f, 0, w/2, 0],
                    [0, f, h/2, 0],
                    [0, 0, 1, 0]])

    # Final transformation matrix
    return np.dot(A2, np.dot(T, np.dot(R, A1)))


""" Utility Functions """

def get_rad(theta, phi, gamma):
    return (deg_to_rad(theta),
            deg_to_rad(phi),
            deg_to_rad(gamma))

def get_deg(rtheta, rphi, rgamma):
    return (rad_to_deg(rtheta),
            rad_to_deg(rphi),
            rad_to_deg(rgamma))

def deg_to_rad(deg):
    return deg * pi / 180.0

def rad_to_deg(rad):
    return deg * 180.0 / pi


if __name__ == '__main__':

    # Input image
    img = cv2.imread(sys.argv[1])

    # Rotation range
    rot_range = 360 if len(sys.argv) <= 2 else int(sys.argv[2])

    # Make output dir
    if not os.path.isdir('output'):
        os.mkdir('output')

    # Iterate through rotation range
    for ang in xrange(0, rot_range):

        # NOTE: Here we can change which angle, axis, shift
        
        """ Example of rotating an image along y-axis from 0 to 360 degree """
        rotated_img = rotate_along_axis(img, phi = ang, dx = 5)

        """ Example of rotating an image along yz-axis from 0 to 360 degree """
        #rotated_img = rotate_along_axis(img, phi = ang, gamma = ang)

        cv2.imwrite('output/{}.jpg'.format(str(ang).zfill(3)), rotated_img)

