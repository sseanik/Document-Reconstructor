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
