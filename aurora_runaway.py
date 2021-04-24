import argparse
import cv2
import numpy as np
import matplotlib.pyplot as plt

def resize_image(img, imgbg):
    imgori = img.shape[0]/img.shape[1]
    bgori = imgbg.shape[0]/imgbg.shape[1]
    rotate = False
    if imgori < 1 :
        if bgori < 1:
            if imgori > bgori:
                rotate=True
    else:
        if not bgori > 1:
            rotate= True
    if rotate:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        imgbg = cv2.rotate(imgbg, cv2.ROTATE_90_CLOCKWISE)
    ratio = img.shape[1]/imgbg.shape[1]
    dims = (int(imgbg.shape[1]*ratio), int(imgbg.shape[0]*ratio))
    imgbg = cv2.resize(imgbg, dims, interpolation = cv2.INTER_AREA)
    if rotate:
        img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
        imgbg = cv2.rotate(imgbg, cv2.ROTATE_90_COUNTERCLOCKWISE)
    return img, imgbg


ap = argparse.ArgumentParser()

# Add the arguments to the parser

ap.add_argument("-o", "--original", required=True,
   help="original image")
ap.add_argument("-b", "--background", required=True,
   help="second operand")
args = vars(ap.parse_args())

image = cv2.imread(args['original'])
imagebg = cv2.imread(args['background'])

newimg, newimgbg = resize_image(image,imagebg)

gray = cv2.cvtColor(newimg,cv2.COLOR_BGR2GRAY)

mask = gray < 128

final_img = np.zeros_like(newimg)
final_img[~mask] = newimgbg[:newimg.shape[0],:newimg.shape[1]][~mask]

plt.imshow(final_img)
plt.show()

cv2.imwrite('final_img.jpg', final_img)