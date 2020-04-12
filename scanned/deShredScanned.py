from skimage.metrics import structural_similarity
import cv2
import numpy as np
import glob

  
def displayImage(image, time):
    # Helper function to display an image in a small window
    cv2.namedWindow('Press ALT to close', cv2.WINDOW_NORMAL   )
    cv2.resizeWindow('Press ALT to close', 800, 10000)
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

    # Compute the mean squared error 
    #m = mse(left, right)

    # Compute the structural similarity index
    s = structural_similarity(left, right)
    return s


def combine(leftImage, rightImage):
    # Combine two shreds
    return np.concatenate((rightImage, leftImage), axis=1)


def getShreds(path):
    # Gather the extracted shreds from a directory and store their edge info
    shreds = []
    for file in glob.glob(path):
        image = cv2.imread(file)
        height, width = image.shape[0:2]
        # Width offsets used to ignore background elements
        leftEdge = image[0:height, 10:50]   
        rightEdge = image[0:height, width - 60:width - 20]
        info = {'image': image, 'left': leftEdge, 'right': rightEdge}
        shreds.append(info)
    return shreds


def getSimilarityScores(shreds):
    # Gather the similarity scores for shred comparisons
    similarity = []
    # Compare the left side of a shred with the right side of every other shred
    for index1, i in enumerate(shreds):
        overall = []
        for index2, j in enumerate(shreds):
            # If comparing the same shred, continue
            if i is j:
                continue
            m = calcSimilarity(i['left'], j['right'], i['image'], j['image'])
            overall.append({m: (index1, index2)})
        similarity.append(overall)
    return similarity


def unShred(shreds, similarity):
    merged = []
    rMerged = []
    point = {}
    finalIndex = ""

    # Loop over each shred chronologically
    for i in similarity:
        # Sort the potential pairings by structural similarity score
        for j in sorted(i, key=lambda d: list(d.keys()), reverse=True):
            # If the number of shred x 2 is equal to the amount of merged shreds
            if len(merged) == len(shreds) * 2:
                break
            for tup in j:
                l = j[tup][0]
                r = j[tup][1]

                # If we have already merged shred
                if l in merged or r in rMerged:
                    break
                
                # Show the structural similarity score
                print(f"Structural Similarity Index: {tup}")

                # If shred is updated, find latest merged shred
                if r in point:
                    x = r
                    while(x in point):
                        x = point[x]

                    # Combine left and right shreds
                    temp = combine(shreds[l]['image'], shreds[x]['image'])

                    # Display the merged shreds and ask for manual input
                    # Non-merged shred should always be on far right
                    displayImage(temp, 100000)
                    print("Enter 'y' if this is correct or any key to go next: ", end="")
                    check = str(input())
                    if check != "y":
                        continue
           
                    shreds[x]['image'] = temp 
                    point[l] = r
                    finalIndex = x
                else:
                    # Combine left and right shreds
                    temp = combine(shreds[l]['image'], shreds[r]['image'])

                    # Display the merged shreds and ask for manual input
                    # Non-merged shred should always be on far right
                    displayImage(temp, 100000)
                    print("Enter 'y' if this is correct or any key to go next: ", end="")
                    check = str(input())
                    if check != "y":
                        continue

                    shreds[r]['image'] = temp
                    point[l] = r
                    finalIndex = r 

                merged.append(l)
                rMerged.append(r)
                # When we merge shred, go to next left shred
                break

    return finalIndex
    

if __name__ == '__main__':
    # Path to directory where extracted shreds are present
    path = "/home/sean/Desktop/testImages/out/*"

    # Gather extracted shreds
    shreds = getShreds(path)

    # Calculate similarity scores based on checks between each shred's left
    # edge with a different shred's right edge
    similarity = getSimilarityScores(shreds)

    # Gather the final index pointing to the combined shred
    finalIndex = unShred(shreds, similarity)

    # Save the unshredded document
    final = cv2.cvtColor(shreds[finalIndex]['image'], cv2.COLOR_BGR2RGB)
    cv2.imwrite(f"../testImages/unshredded.png", final)
  
