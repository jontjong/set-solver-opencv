''' test document '''
import cv2
import numpy as np

RED_THRESH = [195,90,80]
PURPLE_THRESH = [125,80,120]
GREEN_THRESH = [90,180,70]
COLOUR_IDENTITY = [RED_THRESH,PURPLE_THRESH,GREEN_THRESH]

def findShape(contour):
    peri = cv2.arcLength(contour,True)
    approx = cv2.approxPolyDP(contour,0.02*peri,True)
    if len(approx) == 4:
        return("diamond")
    elif len(approx) == 8:
        return("rounded rectangle")
    elif len(approx) == 10:
        return("squiggly")
    else:
        return("unknown")

def numOfChildren(parent):
    num = 0
    while parent != -1:
        parent = hierarchy[0][parent][0]
        num += 1
    return num

for i in range(16):
    im = cv2.imread('set_card'+str(i)+'.png')
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(1,1),1000)
    flag, thresh = cv2.threshold(blur, 165, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    mask = np.zeros(im.shape[:2], np.uint8)
    cv2.drawContours(mask, contours[1:], -1, 255, -1)
    cv2.imshow('image',mask)
    cv2.imwrite('mask'+str(i)+'.png', mask)
    mean = cv2.mean(im, mask=mask)
    rgbColour = np.array([(mean[2], mean[1], mean[0])])

    cv2.imshow('routine',im)
    cv2.imshow('image',thresh)
    cv2.imwrite('cardex'+str(i)+'.png', thresh)
    cv2.drawContours(im, contours[1:], -1, (255,0,0), 5)
    cv2.imshow('thresh', im)
    cv2.imwrite('cardcon'+str(i)+'.png', im)
    cv2.waitKey(0)
    print(rgbColour)
    minDist = (np.inf, None)

    for colour in COLOUR_IDENTITY:
        dist = np.linalg.norm(rgbColour[0]-colour)

        if dist < minDist[0]:
            minDist = (dist,colour)
    if minDist[1] == RED_THRESH:
        colour = 'red'
    elif minDist[1] == PURPLE_THRESH:
        colour = 'purple'
    elif minDist[1] == GREEN_THRESH:
        colour = 'green'
    else:
        colour = 'indeterminate'
    
    #cv2.imshow('image',mask)
    #cv2.waitKey(0)

    num = 0
    firstChild = hierarchy[0][0][2]
    shadingChild = hierarchy[0][firstChild][2]

    #print shape
    shape = findShape(contours[firstChild])
    #find shading
    shadeShape = findShape(contours[shadingChild])

    if shadingChild != -1 and shadeShape == shape:
        print('blank')
        shading = 'blank'
    
    elif numOfChildren(shadingChild) > 5:
        print('striped')
        shading = 'striped'

    else:
        print('solid')
        shading = 'solid'

    while firstChild != -1:
        firstChild = hierarchy[0][firstChild][0]
        num += 1






    for i in range(len(contours)):
        contour = contours[i]
        peri = cv2.arcLength(contour,True)
        approx = cv2.approxPolyDP(contour,0.02*peri,True)
        #print(len(approx))

    print('There are/is '+str(num)+' '+shading+' '+colour+' '+shape)


    #cv2.imshow('image',thresh)
    #cv2.waitKey(0)

    #cv2.drawContours(im, contours, -1, (0,255,0),8)
   # print('hierarcy')
    #print(hierarchy)
    print("new card")

    cv2.imshow('image',im)
    cv2.waitKey(0)