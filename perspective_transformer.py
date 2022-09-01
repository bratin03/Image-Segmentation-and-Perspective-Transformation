import cv2
import numpy as np

img1=cv2.imread('raw_images/aachen_000064_000019_leftImg8bit.png')
img2=cv2.imread('segmented_images/aachen_000064_000019_gtFine_color.png')
#detecting roads
for h in reversed((range (256))):
    for w in reversed(range (512)):
        B, G, R = img2[h,w]
        if(B==255):
            top_left_x=w
            top_left_y=h

for h in reversed(range (256)):
    for w in (range (512)):
        B, G, R = img2[h,w]
        if(B==255):
            top_right_x=w
            top_right_y=h

for h in range (256):
    for w in reversed(range (512)):
        B, G, R = img2[h,w]
        if(B==255):
            bottom_left_x=w
            bottom_left_y=h

for h in (range (256)):
    for w in (range (512)):
        B, G, R = img2[h,w]
        if(B==255):
            bottom_right_x=w
            bottom_right_y=h

pts1=np.float32([[bottom_left_x+150,top_left_y+30],[bottom_left_x,bottom_left_y],[bottom_right_x-150,top_right_y+30],[bottom_right_x,bottom_right_y]])
width=640
height=480
pts2=np.float32(([0,0],[0,height],[width,0],[width,height]))
#perspective_transform
matrix=cv2.getPerspectiveTransform(pts1,pts2)
imgOutput=cv2.warpPerspective(img1,matrix,(width,height))


cv2.imwrite('aachen_000064_000019_perspective_transformed.png',imgOutput)