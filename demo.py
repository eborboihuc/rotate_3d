from image_transformer import ImageTransformer
from util import save_image
import sys
import os

# Usage: 
#     Change main function with ideal arguments
#     then
#     python demo.py [name of the image] [degree to rotate] ([ideal width] [ideal height])
#     e.g.,
#     python demo.py images/000001.jpg 360
#     python demo.py images/000001.jpg 45 500 700
#
# Parameters:
#     img_path  : the path of image that you want rotated
#     shape     : the ideal shape of input image, None for original size.
#     theta     : the rotation around the x axis
#     phi       : the rotation around the y axis
#     gamma     : the rotation around the z axis (basically a 2D rotation)
#     dx        : translation along the x axis
#     dy        : translation along the y axis
#     dz        : translation along the z axis (distance to the image)
#
# Output:
#     image     : the rotated image


# Input image path
img_path = sys.argv[1]

# Rotation range
rot_range = 360 if len(sys.argv) <= 2 else int(sys.argv[2])

# Ideal image shape (w, h)
img_shape = None if len(sys.argv) <= 4 else (int(sys.argv[3]), int(sys.argv[4]))

# Instantiate the class
it = ImageTransformer(img_path, img_shape)

# Make output dir
if not os.path.isdir('output'):
    os.mkdir('output')

# Iterate through rotation range
for ang in xrange(0, rot_range):

    # NOTE: Here we can change which angle, axis, shift
    
    """ Example of rotating an image along y-axis from 0 to 360 degree 
        with a 5 pixel shift in +X direction """
    rotated_img = it.rotate_along_axis(phi = ang, dx = 5)

    """ Example of rotating an image along yz-axis from 0 to 360 degree """
    #rotated_img = it.rotate_along_axis(phi = ang, gamma = ang)

    """ Example of rotating an image along z-axis(Normal 2D) from 0 to 360 degree """
    #rotated_img = it.rotate_along_axis(gamma = ang)

    save_image('output/{}.jpg'.format(str(ang).zfill(3)), rotated_img)


