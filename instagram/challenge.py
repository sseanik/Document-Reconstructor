from skimage.metrics import structural_similarity
from PIL import Image
import cv2
import numpy as np


def displayImage(image, time):
    # Helper function to display an image in a small window
    cv2.namedWindow('Press ALT to close', cv2.WINDOW_NORMAL   )
    cv2.imshow('Press ALT to close', image)
    cv2.waitKey(time)
    cv2.destroyAllWindows()


# https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
def mse(imageA, imageB):
	# The 'Mean Squared Error' between the two images is the sum of the squared 
    # difference between the two images;
	# NOTE: the two images must have the same dimension
	err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
	err /= float(imageA.shape[0] * imageA.shape[1])
	
    # Return the MSE
	return err


# https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
def calcSimilarity(left, right, test1, test2):
    left = cv2.cvtColor(left, cv2.COLOR_BGR2GRAY)
    right = cv2.cvtColor(right, cv2.COLOR_BGR2GRAY)

    #displayImage(left, 10000)
    #displayImage(right, 10000)

    # Compute the structural similarity index
    s = structural_similarity(left, right, multichannel=True)

    # Compute the mean squared error 
    #m = mse(left, right)
    return s


def getSimilarityScores(shreds):
    # Gather the similarity scores for shred comparisons
    similarity = []
    # Compare the left side of a shred with the right side of every other shred
    for index1, i in enumerate(shreds):
        for index2, j in enumerate(shreds):

            # If comparing the same shred, continue
            if i is j:
                continue
            m = calcSimilarity(i['left'], j['right'], i['image'], j['image'])
            similarity.append({m: (index1, index2)})
    return similarity

def combine(leftImage, rightImage):
    # Combine two shreds
    return np.concatenate((rightImage, leftImage), axis=1)

def getShreds(image, shred_width):
    width, height = image.size
    shreds = []
    i = 0
    j = shred_width
    # Crop shred segment from left to right
    while i < width:   
        temp = image.copy()
        temp = temp.crop((i, 0, j, height))

        # Convert to opencv format
        opencvImage = cv2.cvtColor(np.array(temp), cv2.COLOR_RGB2BGR)
        newHeight, newWidth = opencvImage.shape[0:2]
        
        # Set Edge pixel widths
        leftEdge = opencvImage[0:newHeight, 0:1]   
        rightEdge = opencvImage[0:newHeight, newWidth - 1:newWidth]

        info = {'image': opencvImage, 'left': leftEdge, 'right': rightEdge}
        shreds.append(info)

        i += shred_width
        j += shred_width

    return shreds

def unShred(shreds, similarity):
    merged = []
    rMerged = []
    point = {}
    finalIndex = ""

    # Sort the potential pairings by structural similarity score
    for j in sorted(similarity, key=lambda d: list(d.keys()), reverse=True):

        if len(merged) == len(shreds) - 1:
            break
        for tup in j:

            l = j[tup][0]
            r = j[tup][1]

            # If we have already merged shred
            if l in merged or r in rMerged:
                break
            
            # Show the MSE score
            print(f"SSIM: {tup}")

            # If shred is updated, find latest merged shred
            if r in point:
                x = r
                while(x in point):
                    x = point[x]

                # Combine left and right shreds
                shreds[x]['image'] = combine(shreds[l]['image'], shreds[x]['image']) 
                point[l] = r
                finalIndex = x
            else:
                # Combine left and right shreds
                shreds[r]['image'] = combine(shreds[l]['image'], shreds[r]['image'])
                point[l] = r
                finalIndex = r 

            merged.append(l)
            rMerged.append(r)

    return finalIndex


if __name__ == '__main__':
    # Location of jumbled image
    path = "../testImages/insta.png"
    image = Image.open(path).convert('RGB') 

    SHREDS = 10
    width, height = image.size

    # Given shred width of image
    shred_width = 25

    # Crop shreds
    shreds = getShreds(image, shred_width)
    
    # Calculate SSIM scores
    similarity = getSimilarityScores(shreds)

    # Final combined output
    finalIndex = unShred(shreds, similarity)
    cv2.imwrite(f"../testImages/instaChal.png", shreds[finalIndex]['image'])


