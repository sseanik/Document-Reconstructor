# Scanned Shred Reconstructor

In extractShreds.py:

```python
You must input the number of shreds for the first image at path 1, and then for the second image at path 2

# Change the path of the two scanned images
path1 = "../testImages/first.png"
path2 = "../testImages/second.png"

# You may wish to also change the uniform size of the scanned shreds
uniformSize = (228, 6635)
```


In deShredScanned.py:

```python
# Change the path to directory where extracted shreds are present
path = "/home/sean/Desktop/testImages/out/*"

# Change the path to the location of the destination of for the reconstructed image
cv2.imwrite(f"../testImages/unshredded.png", final)
```


**extractShreds.py** takes two scanned image, extracts x and y amount of shreds and stores them into a directory. Each shred will automatically be adjusted to the uniform size given


**deShredScanned.py** takes a directory of x + y amount of shreds, then calcuates similarity scores based on the left edge of a strip compared to the right edge of another strip and then manual input is needed where a combined shred will be shown (press ALT when finished viewing the image) and only input 'y' if the shred is a matching pairing. Once all manual input is finished, a final reconstructed image is outputted.


In deShredPerfect.py:

```python
# Replace X if you would like to set the edge similarity widths greater than 1
leftEdge = image[0:height, 0:X]   
rightEdge = image[0:height, width - X:width]

# If you would like to use Mean Square Error instead, comment this line:
# s = structural_similarity(left, right)
# Uncomment this line:
m = mse(left, right)
# Change return value to m
return m

# Lastly change this line in def unShred() to:
# for j in sorted(similarity, key=lambda d: list(d.keys()), reverse=True):
for j in sorted(similarity, key=lambda d: list(d.keys())):
```
