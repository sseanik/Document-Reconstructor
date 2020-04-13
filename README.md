# Paper-Reconstructor
Tools to reconstruct shredded paper documents as my 'Something Awesome' project for my Security Engineering Course.

My lecturer Richard Buckland, spoke about the aspect of physical security and how he would shred a document, shred the shreds, eat some of them, throw different pieces into different bins and burn the rest. The more common approach would either be to crunch up the paper or just shred it.

I was intrigued, so I wanted to learn about the possibility of programmatically reconstructing a shredded document. I have no computer vision background whatsoever, this was more for my security curiosity.


# Instagram Engineering Challenge
The first tool was derived from the [Instagram Engineering Challenge: The Unshredder](https://instagram-engineering.com/instagram-engineering-challenge-the-unshredder-7ef3f7323ab1), where in 2012 it was posed to prospective to the public to 'unshred' a shuffled image and the prize would be a free T-shirt. Unfortunately I was too late, to the party, but decided to attempt the challenge myself.

Before:


![Instagram Challenge](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/insta.png "Instagram Challenge")


After:


![Instagram Challenge](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/instaChal.png "Instagram Challenge")


# Perfect Digital Shredding
The next tool was an iterative process regarding finding an algorithm and method in shredding a shuffled (horizontally & one side) document. Photoshop slicing was used at the beginning, but a shredding python tool was created to automate the process. These shreds (of no less than 14px) would lose no quality, have a perfect, straight, equal, rectangular shape and more emphasis was given to the algoirthms of 'Mean Squared Error' and 'Structural Similarity'. A solution was made that was able to automatically choose from a directory of 'perfect' shreds and automatically reconstruct the document.

Before:


![Perfect Reconstruction](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/setup.png
 "Perfect Reconstruction")


After:


![Perfect Reconstruction](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/recontructed.png "Perfect Reconstruction")

# Scanned shreds
The next tool was an iterative process regarding scanning in 'imperfect' shreds and was focused on manipulation of the shreds, rather than automating the reconstruction. The process was to use my Keji Strip Cut Shredder (vertical strips) and divide the pile of shreds into two. Half were correctly placed face down on my HP Deskjet F2180 printer/scanner, and a pink piece of paper was placed above. 


![Scanned recontruction](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/photo.png "Scanned recontruction")


Two images of shreds on a pink background were then fed to the extractShreds.py where contours were calculated by filtering out the saturation layer of the image. These shreds would appear curved and distorted, so they were fed into a four point transform algorithm, that when provided with the four corners of a contour, would attempt to unwarp the image and thus straightening it. The shreds were then resized and written to a directory.


deShredScanned.py would then calculate the similarity scores based on the comparison of the left edge of a strip, to a right edge of a strip and then manual checking (automation was not possible due to time limits and constraints of scanner and shredding devices) would be needed to confirm if two shreds (potentially already previously merged) do in fact fit together.


![Scanned recontruction](https://raw.githubusercontent.com/sseanik/Paper-Reconstructor/master/testImages/forreadme.png "Scanned recontruction")

