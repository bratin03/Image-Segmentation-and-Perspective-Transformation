import cv2
import numpy as np

def canny(image):
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    canny = cv2.Canny(blur, 50, 150)
    return canny
#draw line
def display_lines(image,lines):
    line_image=np.zeros_like(image)
    if lines is not None:
        for line in lines:
            x1,y1,x2,y2=line.reshape(4)
            cv2.line(line_image,(x1,y1),(x2,y2),(255,255,255),5)
            tan=(y2-y1)/(x2-x1)
            if tan>0:
               for h1 in range(y1,256):
                   if (x1 + (h1 - y1) / tan)<512:
                       line_image[int(h1),int(x1+(h1-y1)/tan)]=(255,255,255)
            if tan<0:
               for h1 in range(y1,256):
                   if (x1+(h1-y1)/tan)>-512:
                       line_image[int(h1),int(x1+(h1-y1)/tan)]=(255,255,255)



    return line_image

#Region of interest
def region_of_interest(image):
    height=image.shape[0]
    width=image.shape[1]
    polygons=np.array([[(0,height),(width,height),(width,225),(0,225)],[(0,225),(width,225),(240,0),(260,0)]])
    mask=np.zeros_like(image)
    cv2.fillPoly(mask,polygons,255)
    masked_image=cv2.bitwise_and(image,mask)
    return masked_image

image=cv2.imread('raw_images/aachen_000064_000019_leftImg8bit.png')
lane_image=np.copy(image)
canny=canny(lane_image)
cropped_image=region_of_interest(canny)
#line detection
lines=cv2.HoughLinesP(cropped_image,2,np.pi/180,100,None,40,5)
line_image=display_lines(lane_image, lines)
#fill space between line
for h in range (0,256):
    flag=0
    left=512
    right=0
    for w in range(0,512):
        B,G,R=line_image[h,w]
        if flag==0:
            if(B==255):
             left=w
             flag=1
        else:
            if(B==255):
                if((w-left)>20):
                    right=w
                    flag=2
    if flag==2:
        for num in range(left,right):
            for h1 in range(h,256):
                line_image[h1,num]=(255,255,255)
                if (num-h1+h)>0:
                 line_image[h1, num-h1+h] = (255, 255, 255)
                if(num+h1-h)<512:
                 line_image[h1, num + h1 - h] = (255, 255, 255)

cv2.imwrite('aachen_000064_000019_leftImg8bit_segmented.png',line_image)