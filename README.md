# Paper-Reconstructor
Tools to reconstruct shredded paper documents, as my 'Something Awesome' project, for my Security Engineering Course.

My lecturer, Richard Buckland, spoke about the aspect of physical security and how he would shred a document, shred the shreds, eat some of them, throw different pieces into different bins and burn the rest. Since not everyone is Richard Buckland, most of the world resorts to either scrunching up the paper and tossing it away, or using a paper shredder.

I was intrigued, so I wanted to learn about the possibility of programmatically reconstructing a shredded document. I have no computer vision background whatsoever and this was more for my security curiosity. These tools are broken into three different methods/prototypes.


# Instagram Engineering Challenge
The first tool was derived from the [Instagram Engineering Challenge: The Unshredder](https://instagram-engineering.com/instagram-engineering-challenge-the-unshredder-7ef3f7323ab1), where in 2012 it was posed to the public to 'unshred' a shuffled image. The winner(s) earned a free T-shirt prize, but unfortunately I was a bit late to the party. shredder.py takes a source image, and shuffles it with a shred output number. challenge.py takes a shuffled image and a given a number of shreds, unshuffles the image. Descending order of structural similarity was used to determine if two shreds should be merged.

**Before:**


![Instagram Challenge](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/instaout2.png "Instagram Challenge")


**After:**


![Instagram Challenge](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/instaChal.png "Instagram Challenge")


**Visual Demonstration (with merging shown):** ~ [**Youtube Link**](https://youtu.be/kNKJNT0cA0A)


![Instagram Challenge](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/gif1.gif)


# Perfect Digital Shredding
The next tool was an iterative prototype, regarding finding an algorithm and a method in shredding a shuffled (horizontally & one side) document. Photoshop slicing was used to begin with, but perfShredder.py was created to automate the process. These shreds (of no less than 14px) would lose no quality, have a perfect, straight, equal, rectangular shape and more emphasis was given to explore the algorithms of 'Mean Squared Error' and 'Structural Similarity'. deShredPerfect.py takes a directory of 'perfect' shreds and automatically reconstructs the document based on the ascending Mean Squared Error comparisons of the left edge of a shred with the right edge of a shred. 

**Note:**
* Pre-cropping is done to eliminate as many blank side shreds as possible

**Before:**


![Perfect Reconstruction](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/setup.png
 "Perfect Reconstruction")


**After:**


![Perfect Reconstruction](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/recontructed.png "Perfect Reconstruction")


**Visual Demonstration (with merging shown):** ~ [**Youtube Link**](https://youtu.be/-rDarDJEVzc)


![Perfect Reconstruction](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/gif2.gif)


# Scanned shreds
_Proof of Concept. Faster than permutation confirmation matching, but slower than human physically matching. More knowledge in computer vision needed to create a better algorithm to extract shreds as well as finding a different algorithm for shred matching._


The next tool was an iterative prototype, regarding scanning in 'imperfect' shreds and focused on the manipulation of the shreds, rather than the reconstruction. The process was to use my Keji Strip Cut Shredder (vertical strips) and divide the pile of shreds into two. Each half of the pile was correctly placed face down on my HP Deskjet F2180 printer/scanner, and a pink piece of paper was placed on top of the shreds. 



**Devices & Equipment used:**


![Scanned reconstruction](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/photo.png "Scanned reconstruction")


**Note:**
* Paper must be almost A4, cut off the top or bottom of empty bits if possible
* Keji Strip Cut Shredder outputs approx 20 shreds
* Blank side strips can be thrown away
* Images scanned to 600 DPI, Colour and PNG file type


Two images of shreds on a pink background were then fed to the extractShreds.py where contours were calculated by filtering out the saturation layer of the image. These shreds would appear curved and distorted, so they were fed into a four point transform algorithm, that when provided with the four corners of a contour, would attempt to unwarp the image and thus straightening it. The shreds were then resized and written to a directory.


deShredScanned.py would then calculate the similarity scores based on the comparison of the left edge of a strip, to a right edge of a strip and then through manual confirmation (automation was not possible due to time limits and constraints of scanner and shredding devices), where a 'merged' strip is shown, the user needs to verify if two shreds (potentially already previously merged) do in fact fit together. Once all manual confirmations are complete, a reconstructed image is outputted. This is NOT based on permutations, but uses the descending similarity score of the edges. This method does indeed NOT work well enough for automation, but with a better algorithm based on text detection and horizontal structure matching, automation is possible. More computer vision research and time is needed to reach automation.


**Edge Detection with contour outlines:**


![Scanned document 1](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/countourShow1.png "Scanned reconstruction")

![Scanned document 2](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/countourShow2.png "Scanned reconstruction")


**Manual confirmation constructed Image:**


![Scanned reconstruction](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/forreadme.png "Scanned reconstruction")


[**Timelapse Demonstration**](https://www.youtube.com/watch?v=QCrJ-T9hO8o)


# Methods Used
**Mean Squared Error**


The mean squared error calculates how close a 'regression line' is to a set of points. How this works, is the function takes the distances from the points to the regression line, which are called 'errors' and then they are squared. You can also classify these 'errors' as deviations from an expected value or point. We square it in order to remove any negative signs. Overall, we are finding the average of a set of errors. We get closer the line of best fit (or in this case similarity between images) when the mean squared error is smaller.


**Structural Similarity**


The structural similarity (SSIM) index is a way of predicting the perceived quality of images. SSIM is used to measure the similarity between two images, and acts as a measurement. Structural similarity in this instance, works more as a perception-based model which considers image degradation as a perceived change in structural information. It also involves both luminance masking and contrast masking. Structural information itself, is the notion that pixels have strong 'inter-dependencies', especially when they have neighbours. These dependencies carry important information about the visual structure. 


**Image Segmentation**


Segmentation involves separating an image into different regions containing pixels with similar attributes. The regions need to be strongly related to specific objects or features. Thresholding is a segmentation technique where an image is transformed into a binary image which is viewed as a binary region map. This map contains different disjoint regions, one containing pixels with input data values smaller than a threshold and another relating to the input values equal to or above the threshold.

Colour segmentation can be more accurate because of more information present at the pixel level compared to greyscale images. RGB colour representations have strongly interrelated colour components and furthermore, HSV is able to exclude redundancy and helps when attempting to determine actual objects or background colours irrespective of illumination. 


**Perspective Transform**

In Perspective Transformation, we can alter the perspective of an image and attempt to 'straighten' or 'unwarp' the image information. We provide the points of the image for which we want to gather information, by changing the perspective. In the four-point transform case, we provide the 4 corners of a distorted rectangle which allows us to alter the image. Before altering, the destination image needs to have pre-determined dimensions which are calculated based on the largest distance between the bottom-right and bottom-left x-coordinates or the top-right and top-left x-coordinates, and similarly for the y-coordinates. A transformation matrix is applied where the image and the destination dimensions are given to output the altered image.


# Appendix
Mean Squared Error and Structural Similarity - https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/


Shuffling an Image - https://github.com/sseanik/Paper-Reconstructor/blob/master/instagram/shredder.py


Generate the contours of a subimage on a coloured background - https://stackoverflow.com/questions/47899132/edge-detection-on-colored-background-using-opencv


Perspective transform an image using four point transform - https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/


Structural Similarity - https://en.wikipedia.org/wiki/Structural_similarity


Mean Squared Error - https://www.statisticshowto.com/mean-squared-error/


Image Segmentation - https://www.cs.auckland.ac.nz/courses/compsci773s1c/lectures/ImageProcessing-html/topic3.htm


Perspective Transform - https://www.geeksforgeeks.org/perspective-transformation-python-opencv/
