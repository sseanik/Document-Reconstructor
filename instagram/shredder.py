from PIL import Image
import random

#https://instagram-engineering.com/instagram-engineering-challenge-the-unshredder-7ef3f7323ab1
def shredImage(sequence, outputPath):
    # Create shredded image using shuffled sequence of segments
    for i, shred_index in enumerate(sequence):
        # Calculate the dimensions of each shred
        shred_x1, shred_y1 = shred_width * shred_index, 0
        shred_x2, shred_y2 = shred_x1 + shred_width, height

        # Crop the shred region and then paste it on the output image moving
        # i * shred_width each time
        region = image.crop((shred_x1, shred_y1, shred_x2, shred_y2))
        shredded.paste(region, (shred_width * i, 0))
        shredded.save(outputPath)

if __name__ == '__main__':

    # Determine how many shreds to split the image into
    SHREDS = 20

    path = "../testImages/insta.png"

    # Open the image
    image = Image.open(path)
    shredded = Image.new('RGBA', image.size)

    # Gather the width, height and the shred width depending on the shred value
    SHREDS //= 2
    width, height = image.size
    shred_width = width // SHREDS

    # Shuffle a list of a range between 0 and the shred value given
    sequence = list(range(0, SHREDS))
    random.shuffle(sequence)

    # Save the shuffled/shredded file
    outputPath = "../testImages/instaout.png"
    shredImage(sequence, outputPath)

