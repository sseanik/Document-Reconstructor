# Perfect Shred Reconstructor

In perfShredder.py:

```python
# Change the number of shreds you wish to split the image into
SHREDS = 100
  
# Change the path to the location of the directory for the outputted shreds
outputPath = "../testImages/perf/"
```


In deShredPerfect.py:

```python
# Change the path to directory where extracted shreds are present
path = "../testImages/perf/*"

# Change the path to the location of the destination of for the reconstructed image
cv2.imwrite(f"../testImages/recontructed.png", final)
```


**shredder.py** takes an image, extracts x amount of shreds, shuffles them and stores them into a directory. Each shred will automatically be adjusted to a width of 14px, if width is less than 14px


**challenge.py** takes a directory of x amount of shreds, then calcuates similarity scores based on the left edge of a strip compared to the right edge of another strip and then automatically matches and combines shreds and finally outputs a reconstructed image.


In deShredPerfect.py:

```python
# Replace X if you would like to set the edge similarity widths greater than 1
leftEdge = image[0:height, 0:X]   
rightEdge = image[0:height, width - X:width]


# If you would like to use structural similarity index instead, uncomment this line:
s = structural_similarity(left, right)
# Comment the MSE line and change return value to s
# Compute the mean squared error 
# m = mse(left, right)
return s


# Lastly change this line in def unShred() to:
# for j in sorted(similarity, key=lambda d: list(d.keys())):
for j in sorted(similarity, key=lambda d: list(d.keys()), reverse=True):
```
