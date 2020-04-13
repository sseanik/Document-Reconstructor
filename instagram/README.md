# Instagram Engineering Challenge: The Unshredder

In shredder.py:

```python
# Change the number of shreds you wish to split the image into
SHREDS = 20
  
# Change the path to the location of the destination of the shuffled image
path = "../testImages/insta.png"
```


In challenge.py:

```python
# Change the path to the location of the shuffled image
path = "../testImages/insta.png"

# Change the number of shreds from the number you chose in shredder.py
SHREDS = 20

# Change the path to the location of the destination of for the unshuffled image
cv2.imwrite(f"../testImages/instaChal.png", shreds[finalIndex]['image'])

```


**shredder.py** takes an image and shuffles it and outputs it as a jumbled image with x amount of shreds. 

**challenge.py** takes a shuffled image, extracts the shreds based on the x amount of shreds, calculates the similarity between edges and then matches them using the SSIM metric. An unshuffled image is then outputted.

For future extension, in challenge.py, a method could be implemented to automatically determine the shred size, rather than manually receving it. HSV histograms or other similar comparison metrics could be used.
