# Usage:
#     Change main function with ideal arguments
#     Then
#     from image_tranformer import ImageTransformer
#
# Parameters:
#     image_path: the path of image that you want rotated
#     shape     : the ideal shape of input image, None for original size.
#     theta     : rotation around the x axis
#     phi       : rotation around the y axis
#     gamma     : rotation around the z axis (basically a 2D rotation)
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

import math
import random
from math import pi

import cv2
import numpy as np


def get_rad(theta, phi, gamma):
    return (deg_to_rad(theta), deg_to_rad(phi), deg_to_rad(gamma))


def get_deg(rtheta, rphi, rgamma):
    return (rad_to_deg(rtheta), rad_to_deg(rphi), rad_to_deg(rgamma))


def deg_to_rad(deg):
    return deg * pi / 180.0


def rad_to_deg(rad):
    return rad * 180.0 / pi


class ImageTransformer:
    """
    Perspective transformation class for image
    with shape (height, width, #channels)
    """

    def load_image(self, img_path, shape=None):
        """ """
        img = cv2.imread(img_path, cv2.IMREAD_UNCHANGED)
        if shape is not None:
            img = cv2.resize(img, shape)
        return img

    def __init__(self, image_path, shape):
        """ """
        self.image_path = image_path
        self.image = self.load_image(image_path, shape)

        self.height = self.image.shape[0]
        self.width = self.image.shape[1]
        self.num_channels = self.image.shape[2]

    def get_rotation_args(self, rotation: str, ang: int):
        """
        Generates the arguments used for 'rotate_along_axis'
        This takes a rotation-mode 'rotation' and an angle
        named 'ang' in (0 - rot_range), and is called from a loop.
        """
        if rotation in ["y"]:
            # y-axis from 0-360 degree, 5 pixel shift in +X
            rotargs = dict(phi=ang, dx=5)
        elif rotation in ["x"]:
            rotargs = dict(gamma=ang)
        elif rotation in ["s", "swivel"]:
            # yz-axis from 0 to 360 degree
            rotargs = dict(phi=ang, gamma=ang)
        elif rotation in ["jitter", "j"]:
            rotargs = dict(
                dx=random.choice([5, 0, 10]),
                phi=random.choice([ang, -ang]),
                gamma=random.choice([0, ang, -ang]),
            )
        elif rotation in ["wobble", "w"]:
            rotargs = dict(
                dx=random.choice([0, 10, 30]),
                dy=random.choice([25, 0, 10]),
                phi=random.choice([ang, -ang, math.sin(ang)]),
                gamma=random.choice([ang, -ang]),
            )
        elif rotation in ["f", "flip"]:
            rotargs = dict(dx=ang, dy=-ang, phi=math.tan(ang), gamma=ang)
        elif rotation.startswith("q"):
            rotargs = dict(
                dx=random.choice([0, 5, 10]),
                dy=random.choice([25, 0, 10]),
                phi=random.choice([ang, -ang, math.sin(ang)]),
                gamma=random.choice([ang, -ang]),
            )
        elif rotation.startswith("exit"):
            direction = rotation.split("-")[1]
            if direction == "ul":
                rotargs = dict(
                    dx=-ang,
                    dy=-ang,
                )
            elif direction == "ur":
                rotargs = dict(
                    dx=ang,
                    dy=-ang,
                )
            elif direction == "lr":
                rotargs = dict(
                    dx=ang,
                    dy=ang,
                )
            elif direction == "ll":
                rotargs = dict(
                    dx=-ang,
                    dy=ang,
                )
            else:
                raise ValueError(f"unknown rotation: {rotation}")
            rotargs.update(phi=math.tan(ang), gamma=math.tan(ang))
        else:
            raise ValueError(f"Not sure how to perform rotation {rotation}")
        return rotargs

    @staticmethod
    def save_image(img_path, img):
        """
        Saves an output image
        This is usually one that's resulted from a rotation, i.e a single frame in a larger animation
        """
        cv2.imwrite(img_path, img)

    def rotate_along_axis(self, theta=0, phi=0, gamma=0, dx=0, dy=0, dz=0):
        """Returns the new image that results from rotating self.image"""

        # Get radius of rotation along 3 axes
        rtheta, rphi, rgamma = get_rad(theta, phi, gamma)

        # Get ideal focal length on z axis
        # NOTE: Change this section to other axis if needed
        d = np.sqrt(self.height**2 + self.width**2)
        self.focal = d / (2 * np.sin(rgamma) if np.sin(rgamma) != 0 else 1)
        dz = self.focal

        # Get projection matrix
        mat = self.get_M(rtheta, rphi, rgamma, dx, dy, dz)
        return cv2.warpPerspective(self.image.copy(), mat, (self.width, self.height))

    def get_M(self, theta, phi, gamma, dx, dy, dz):
        """Get Perspective Projection Matrix"""
        w = self.width
        h = self.height
        f = self.focal

        # Projection 2D -> 3D matrix
        A1 = np.array([[1, 0, -w / 2], [0, 1, -h / 2], [0, 0, 1], [0, 0, 1]])

        # Rotation matrices around the X, Y, and Z axis
        RX = np.array(
            [
                [1, 0, 0, 0],
                [0, np.cos(theta), -np.sin(theta), 0],
                [0, np.sin(theta), np.cos(theta), 0],
                [0, 0, 0, 1],
            ]
        )

        RY = np.array(
            [
                [np.cos(phi), 0, -np.sin(phi), 0],
                [0, 1, 0, 0],
                [np.sin(phi), 0, np.cos(phi), 0],
                [0, 0, 0, 1],
            ]
        )

        RZ = np.array(
            [
                [np.cos(gamma), -np.sin(gamma), 0, 0],
                [np.sin(gamma), np.cos(gamma), 0, 0],
                [0, 0, 1, 0],
                [0, 0, 0, 1],
            ]
        )

        # Composed rotation matrix with (RX, RY, RZ)
        R = np.dot(np.dot(RX, RY), RZ)

        # Translation matrix
        T = np.array([[1, 0, 0, dx], [0, 1, 0, dy], [0, 0, 1, dz], [0, 0, 0, 1]])

        # Projection 3D -> 2D matrix
        A2 = np.array([[f, 0, w / 2, 0], [0, f, h / 2, 0], [0, 0, 1, 0]])

        # Final transformation matrix
        return np.dot(A2, np.dot(T, np.dot(R, A1)))
