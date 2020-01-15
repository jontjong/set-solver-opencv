''' test document '''
import cv2
import numpy as np

RED_THRESH = [195,90,80]
PURPLE_THRESH = [125,80,120]
GREEN_THRESH = [90,180,70]
COLOUR_IDENTITY = [RED_THRESH,PURPLE_THRESH,GREEN_THRESH]

POTENTIAL_COLOURS = ['red','purple','green']
POTENTIAL_SHAPES = ['diamond','squiggly','rounded rectangle']
POTENTIAL_NUMBERS = [1,2,3]
POTENTIAL_SHADES = ['blank','striped','solid']

RED_HIGHLIGHT = [255,0,0]
GREEN_HIGHLIGHT = [0,255,0]
BLUE_HIGHLIGHT = [0,0,255]
YELLOW_HIGHLIGHT = [255,255,0]
PINK_HIGHLIGHT = [255,0,255]
LIGHTBLUE_HIGHLIGHT = [0,255,255]

COLOUR_HIGHLIGHT = [RED_HIGHLIGHT,GREEN_HIGHLIGHT,BLUE_HIGHLIGHT,YELLOW_HIGHLIGHT,PINK_HIGHLIGHT,LIGHTBLUE_HIGHLIGHT]



class setCard:
    def __init__(self, number, shapes, colours, shade, location):
        self.number = number
        self.shape = shapes
        self.colour = colours
        self.shade = shade
        self.contour = location

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

cv2.namedWindow('image',cv2.WINDOW_NORMAL)
cv2.resizeWindow('image', 1100,600)

im = cv2.imread('set9.jpg')
gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray,(1,1),1000)
flag, thresh = cv2.threshold(blur, 135, 255, cv2.THRESH_BINARY)

contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#take largest 16 contours, temporary code
contourCards = sorted(contours, key = cv2.contourArea, reverse = True)[:16]

cv2.imshow('image',thresh)
cv2.waitKey(0)
cv2.imwrite('black.png',thresh)

cv2.drawContours(im, contourCards, -1, (255,0,0),8)

cv2.imshow('image',im)
cv2.imwrite('cardsidentity.png',im)
cv2.waitKey(0)

listSets =[]
i =0

for card in contourCards:
    peri = cv2.arcLength(card,True)
    approx = cv2.approxPolyDP(card,0.02*peri,True)

    src = np.array(approx, np.float32)
    #print(src)

    if src[0][0][0] < src[2][0][0]:
        src[0][0][0], src[2][0][0] = src[2][0][0], src[0][0][0]
        src[0][0][1], src[2][0][1] = src[2][0][1], src[0][0][1]
    #print(src)

    h = np.array([ [0,0],[649,0],[649,449],[0,449] ],np.float32)
    transform = cv2.getPerspectiveTransform(src,h)
    warp = cv2.warpPerspective(im,transform,(650,450))
    #cv2.imshow('warp',warp)
    #cv2.waitKey(0)
    #cv2.imwrite('set_card'+str(i)+'.png',warp)
    #i += 1
    gray = cv2.cvtColor(warp,cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray,(1,1),1000)
    flag, thresh = cv2.threshold(blur, 165, 255, cv2.THRESH_BINARY)

    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    mask = np.zeros(warp.shape[:2], np.uint8)
    cv2.drawContours(mask, contours[1:], -1, 255, -1)
    mean = cv2.mean(warp, mask=mask)
    rgbColour = np.array([(mean[2], mean[1], mean[0])])

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
        shading = 'blank'

    elif numOfChildren(shadingChild) > 10:
        shading = 'striped'

    else:
        shading = 'solid'

    while firstChild != -1:
        firstChild = hierarchy[0][firstChild][0]
        num += 1

    pair = setCard(num, shape, colour, shading, card)
    listSets.append(pair)

completeSets = []

for x in range(16):
    for y in range(16):
        if x != y:
            colourMatch = [listSets[x].colour, listSets[y].colour]
            shapeMatch = [listSets[x].shape, listSets[y].shape]
            shadeMatch = [listSets[x].shade, listSets[y].shade]
            numberMatch = [listSets[x].number, listSets[y].number]

            if colourMatch[0]==colourMatch[1]:
                colourSearch = listSets[x].colour
            else:
                for colour in POTENTIAL_COLOURS:
                    if colour != colourMatch[0] and colour != colourMatch[1]:
                        colourSearch = colour

            if shapeMatch[0]==shapeMatch[1]:
                shapeSearch = listSets[x].shape
            else:
                for shape in POTENTIAL_SHAPES:
                    if shape != shapeMatch[0] and shape != shapeMatch[1]:
                        shapeSearch = shape

            if shadeMatch[0]==shadeMatch[1]:
                shadeSearch = listSets[x].shade
            else:
                for shade in POTENTIAL_SHADES:
                    if shade != shadeMatch[0] and shade != shadeMatch[1]:
                        shadeSearch = shade
            
            if numberMatch[0]==numberMatch[1]:
                numberSearch = listSets[x].number
            else:
                for number in POTENTIAL_NUMBERS:
                    if number != numberMatch[0] and number != numberMatch[1]:
                        numberSearch = number
            for z in range(9):
                if z != x and z !=y:
                    if listSets[z].colour == colourSearch and listSets[z].shade == shadeSearch and listSets[z].shape == shapeSearch and listSets[z].number == numberSearch:
                        combo = [x,y,z]
                        combo.sort()
                        if combo not in completeSets:
                            completeSets.append(combo)
for i in range(len(completeSets)):
    contourSet = []

    for index in completeSets[i]:
        contourSet.append(listSets[index].contour)
    copy = im.copy()
    cv2.drawContours(copy, contourSet, -1, (0,0,255),20)                
    cv2.imshow('image',copy)
    cv2.imwrite('solvedset'+str(i)+'.png',copy)
    cv2.waitKey(0)