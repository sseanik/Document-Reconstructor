from skimage.metrics import structural_similarity
import matplotlib.pyplot as plt
import cv2
import numpy as np
import glob

  
def printImage(image, time):
    final = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    cv2.imshow('cropped', final)
    #wait for 1 second
    k = cv2.waitKey(time)
    #destroy the window
    cv2.destroyAllWindows()


def mse(imageA, imageB):
	# the 'Mean Squared Error' between the two images is the
	# sum of the squared difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
	# return the MSE, the lower the error, the more "similar"
	# the two images are
	return err

def calcSimilarity(left, right, test1, test2):
    # compute the mean squared error and structural similarity
    # index for the images
    left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
    right = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)
    m = mse(left, right)
    #s = structural_similarity(left, right)
    



    return m

def combine(leftImage, rightImage):



    vis = np.concatenate((rightImage, leftImage), axis=1)
    """
    cv2.imshow('cropped', vis)
    k = cv2.waitKey(5000)
    cv2.destroyAllWindows()
    """
    return vis
    

#shreds[0] = {'image': img, L: '
# = [{'shred': img, 'left': hey, 'right': cool}}] 
shreds = []
#select the path
path = "/home/sean/Desktop/images5/*"
for file in glob.glob(path):
    image = cv2.imread(file)

    height, width = image.shape[0:2]
    #print(f"{height} and {width}")
    leftEdge = image[0:height, 0:1]   
    rightEdge = image[0:height, width - 1:width]

    info = {'image': image, 'left': leftEdge, 'right': rightEdge}
    shreds.append(info)

    """
    #conversion numpy array into rgb image to show
    left = cv2.cvtColor(leftEdge, cv2.COLOR_BGR2RGB)
    cv2.imshow('cropped', left)
    right = cv2.cvtColor(rightEdge, cv2.COLOR_BGR2RGB)
    cv2.imshow('cropped', right)

    #wait for 1 second
    k = cv2.waitKey(10000)
    #destroy the window
    cv2.destroyAllWindows()
    """

#print(len(shreds))
similarity = []
for index1, i in enumerate(shreds):
    #print("------------------")
    for index2, j in enumerate(shreds):
        if i is j:
            continue
        m = calcSimilarity(i['left'], j['right'], i['image'], j['image'])
        #similarity.append([m, s])
        #similarity.append({s: (i['left'], j['right'])})
        similarity.append({m: (index1, index2)})


merged = []
rMerged = []
point = {}
z = ""

for j in sorted(similarity, key=lambda d: list(d.keys())):
    if len(merged) == len(shreds) * 2:
        break

    for tup in j:
        if tup <= 10.0:
            continue
        l = j[tup][0]
        r = j[tup][1]

        if l in merged or r in rMerged:
            break
        print(tup)
        print(f"{r} to the left of {l}")

        if r in point:
            x = r
            while(x in point):
                x = point[x]
            shreds[x]['image'] = combine(shreds[l]['image'], shreds[x]['image']) 
            point[l] = r
            printImage(shreds[x]['image'], 1200)    
            z = x    

        else:
            shreds[r]['image'] = combine(shreds[l]['image'], shreds[r]['image'])
            point[l] = r
            printImage(shreds[r]['image'], 1200)
            z = r 
            
        #shreds[r]['image'] = shreds[l]['image'] = combine(shreds[l]['image'], shreds[r]['image'])
        merged.append(l)
        rMerged.append(r)

 
#print(len(shreds))
#print(len(merged))
final = cv2.cvtColor(shreds[z]['image'], cv2.COLOR_BGR2RGB)
cv2.imshow('cropped', final)
#wait for 1 second
k = cv2.waitKey(10000)
#destroy the window
cv2.destroyAllWindows()     
