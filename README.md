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


**Visual Demonstration (with merging shown):**


![Instagram Challenge](https://im2.ezgif.com/tmp/ezgif-2-41ab05aa28c7.gif)



# Perfect Digital Shredding
The next tool was an iterative prototype, regarding finding an algorithm and a method in shredding a shuffled (horizontally & one side) document. Photoshop slicing was used to begin with, but perfShredder.py was created to automate the process. These shreds (of no less than 14px) would lose no quality, have a perfect, straight, equal, rectangular shape and more emphasis was given to explore the algorithms of 'Mean Squared Error' and 'Structural Similarity'. deShredPerfect.py takes a directory of 'perfect' shreds and automatically reconstructs the document based on the ascending Mean Squared Error comparisons of the left edge of a shred with the right edge of a shred. 

**Note:**
* Pre-cropping is done to eliminate as many blank side shreds as possible

**Before:**


![Perfect Reconstruction](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/setup.png
 "Perfect Reconstruction")


**After:**


![Perfect Reconstruction](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/recontructed.png "Perfect Reconstruction")


**Visual Demonstration (with merging shown):**


![Perfect Reconstruction](https://im7.ezgif.com/tmp/ezgif-7-c4703a8cebbb.gif)


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


something


**Structural Similarity**


something


**Edge Detection**


something


**Four Point Transform**


something


# Appendix
Mean Squared Error and Structural Similarity - https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/


Shuffling an Image - https://github.com/sseanik/Paper-Reconstructor/blob/master/instagram/shredder.py


Generate the contours of a subimage on a coloured background - https://stackoverflow.com/questions/47899132/edge-detection-on-colored-background-using-opencv


Perspective transform an image using four point transform - https://www.pyimagesearch.com/2014/08/25/4-point-opencv-getperspective-transform-example/
