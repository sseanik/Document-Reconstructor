import cv2
import numpy as np


def viewImage(image):
    # Helper function to display an image in a small window
    cv2.namedWindow('Display', cv2.WINDOW_NORMAL)
    cv2.imshow('Display', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# https://stackoverflow.com/questions/47899132/edge-detection-on-colored-background-using-opencv
# Step 1: Convert the image from BGR (blue,green,red) into HSV (hue,saturation,value)
# Step 2: We threshold the saturation channel (contains the colour background)
# Step 3: Find the max size contour (i.e. ignore the small occurances of edge detection)
def getContours(image, numShreds):

    # Convert to hsv-space, then split the channels
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)

    # Threshold the S channel using adaptive method(`THRESH_OTSU`) or fixed thresh
    th, threshed = cv2.threshold(s, 50, 255, cv2.THRESH_BINARY_INV)

    # Find all the external contours on the threshed S
    contours = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    contours = sorted(contours, key = cv2.contourArea, reverse=True)
    
    # Return all the shred contours (ignores the bigger rectangle and smaller particles)
    return contours[1:numShreds + 1]


def getShredContour(shred):
    # Helper function used in case a shred needs to generate a new contour
    hsv = cv2.cvtColor(shred, cv2.COLOR_BGR2HSV)
    h,s,v = cv2.split(hsv)
    th, threshed = cv2.threshold(s, 50, 255, cv2.THRESH_BINARY_INV)
    contours = cv2.findContours(threshed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
    contours = sorted(contours, key = cv2.contourArea, reverse=True)    
    return contours[0]


# https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
def order_points(pts):
	# First entry in the list is the top-left, second entry is the top-right, 
    # third is the bottom-right, and the fourth is the bottom-left
	rect = np.zeros((4, 2), dtype = "float32")
	
    # The top-left point will have the smallest sum, whereas the bottom-right 
    # point will have the largest sum
	s = pts.sum(axis = 1)
    # Point offset is to attempt to stretch content to edges
	rect[0] = pts[np.argmin(s)] + 5
	rect[2] = pts[np.argmax(s)]

	# Compute the difference between the points, the top-right point will have 
    # the smallest difference, the bottom-left will have the largest difference
	diff = np.diff(pts, axis = 1)
    # Point offset is to attempt to stretch content to edges
	rect[1] = pts[np.argmin(diff)] + 5
	rect[3] = pts[np.argmax(diff)]

	# Return the reordered coordinates
	return rect


# https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
def four_point_transform(image, pts):
    # Set points to a specific order
	rect = order_points(pts)
	(tl, tr, br, bl) = rect

	# Compute width of the new image, which contains a maximum distance between 
    # bottom-right and bottom-left x-coordiates or the top-right and top-left 
    # x-coordinates
	widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
	widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
	maxWidth = max(int(widthA), int(widthB))

	# Compute height of the new image, which contains a maximum distance between 
    # the top-right and bottom-right y-coordinates or the top-left and 
    # bottom-left y-coordinates
	heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
	heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
	maxHeight = max(int(heightA), int(heightB))

	# With the dimensions of the new image, construct the set of destination 
    # points to obtain a top down/unwarped view of the image specifying points
	# in the top-left, top-right, bottom-right, and bottom-left order
    # Width offset is to attempt to stretch content to edges
	dst = np.array([[0, 0],
		            [maxWidth + 10, 0],
		            [maxWidth + 10, maxHeight - 2],
		            [0, maxHeight - 2]], dtype = "float32")

	# Compute the perspective transform matrix and then apply it
	M = cv2.getPerspectiveTransform(rect, dst)
	unwarped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
	
    # Return the unwarped image
	return unwarped


def getShreds(image, contours):
    shreds = []
    # Iterater over each shred edge outline
    for i in contours:
        # Generate the points for each of the four corners of the contour
        rc = cv2.minAreaRect(i)
        box = cv2.boxPoints(rc)
        pts = np.float32([(box[1][0],box[1][1]),(box[2][0],box[2][1]), \
              (box[0][0],box[0][1]),(box[3][0],box[3][1])])
        crop  = image.copy()
        # Perspective transform (straighen) the shred and crop it
        unwarped = four_point_transform(crop, pts)
        shreds.append(unwarped)    
    return shreds


if __name__ == '__main__':
    # Get the count for the amount of shreds on each scanned sheet
    print("How many shreds for the first image: ", end="")
    first = int(input())
    print("How many shreds for the second image: ", end="")
    second = int(input())

    # Set the path to the scanned sheets
    path1 = "../testImages/first.png"
    path2 = "../testImages/second.png"

    # Read both of the images
    image1 = cv2.imread(path1)
    image2 = cv2.imread(path2)

    # Using edge detection, generate the contours around each shred
    contours1 = getContours(image1, first)
    contours2 = getContours(image2, second)

    demo1 = image1.copy()
    cv2.drawContours(demo1, contours1, -1, (0, 255, 0), 10)
    cv2.imwrite(f"../testImages/demoContour1.png", demo1) 

    demo2 = image2.copy()
    cv2.drawContours(demo2, contours2, -1, (0, 255, 0), 10) 
    cv2.imwrite(f"../testImages/demoContour2.png", demo2) 

    # Unwarp and separate each shred into its own image
    shreds1 = getShreds(image1, contours1)
    shreds2 = getShreds(image2, contours2)

    # Resize each shread to a uniform size and write each shred as a file 
    uniformSize = (228, 6635)
    count = 0
    for i in shreds1:
        resized = cv2.resize(i, uniformSize, interpolation = cv2.INTER_AREA)
        cv2.imwrite(f"../testImages/out/{count}.png", resized)
        count += 1
    for j in shreds2:
        resized = cv2.resize(j, uniformSize, interpolation = cv2.INTER_AREA)
        cv2.imwrite(f"../testImages/out/{count}.png", resized)
        count += 1

