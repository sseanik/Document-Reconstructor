from PIL import Image
import random
import os
import glob


#https://instagram-engineering.com/instagram-engineering-challenge-the-unshredder-7ef3f7323ab1
def shredImage(sequence, outputPath):
    # Create jumbled shred fiiles
    for i, shred_index in enumerate(sequence):
        # Calculate the dimensions of each shred and it's shuffled order
        shred_x1, shred_y1 = shred_width * shred_index, 0
        shred_x2, shred_y2 = shred_x1 + shred_width, height

        # Crop the shred region and save it
        region = image.crop((shred_x1, shred_y1, shred_x2, shred_y2))
        region.save(f"{outputPath + str(i)}.png")

if __name__ == '__main__':


    # Determine how many shreds to split the image into
    SHREDS = 100
    path = "../testImages/shredThis.png"

    # Open the image
    image = Image.open(path)
    shredded = Image.new('RGBA', image.size)

    # Gather the width, height
    width, height = image.size

    # Shred width must not be lower than 14px
    shred_width = width // SHREDS
    if shred_width < 14:
        shred_width = 14
        SHREDS = width // 14

    # Shuffle a list of a range between 0 and the shred value given
    sequence = list(range(0, SHREDS + 1))
    random.shuffle(sequence)

    # Save the shuffled/shredded file
    outputPath = "../testImages/perf/"

    # Remove all files from output directory
    files = glob.glob(f"{outputPath}*")
    for f in files:
        os.remove(f)

    shredImage(sequence, outputPath)

