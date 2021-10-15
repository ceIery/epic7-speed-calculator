import cv2
import numpy
from PIL import Image, ImageChops
import pytesseract
import numpy as np


"""
Given an image, preprocesses image and returns a cropped, 16:9 copy
"""
def preprocessing(image):
    TARGET_RATIO = 16 / 9
    img = image

    # Crop black edges (i.e. notch)
    img = crop_borders(img)

    # Get aspect ratio
    w, h = img.size
    aspect_ratio = w / h

    # Crop image to aspect ratio
    if aspect_ratio != TARGET_RATIO:

        # Width too large (horizontal crop)
        if aspect_ratio > TARGET_RATIO:
            new_w = h * TARGET_RATIO
            left = (w - new_w) / 2
            right = (w + new_w) / 2
            img = img.crop((left, 0, right, h))

        # Height too large (vertical crop)
        else:
            new_h = w / TARGET_RATIO
            top = (h - new_h) / 2
            bottom = (h + new_h) / 2
            img = img.crop((0, top, w, bottom))

    # Resize image to 1280x720
    img = img.resize((1280, 720))

    return img


"""
Given an image, returns a copy with all black edges cropped.
Used to remove the notch in phone screenshots.
"""
def crop_borders(image):
    bg = Image.new(image.mode, image.size)
    diff = ImageChops.difference(image, bg)
    diff = ImageChops.add(diff, diff, 2.0, -100)
    bbox = diff.getbbox()
    if bbox:
        return image.crop(bbox)
    return image


"""
Given an image, gets the percentage values from the screenshot and
returns them as a string

Precondition: input image is preprocessed
"""
def get_percents(image):
    # Predetermined location of percentages
    top = 110
    bottom = 616
    left = 302
    right = 360

    # Crop image to only include percentages
    img = image.crop((left, top, right, bottom))
    # img.show()

    cv_img = numpy.array(img)

    # Remove health bars from screenshot
    bg_color = (16, 16, 16)  # background colour
    health_height = 22  # height of health bar
    health_x = (0, 57)  # start and end x of health bar
    curr_y = 423  # first health bar
    dist_y = 64  # the distance between the height of each health bar

    # Remove at most 7 health bars
    for i in range(7):
        start = (health_x[0], curr_y)
        end = (health_x[1], curr_y + health_height)
        # Draw rectangle over health bar
        cv_img = cv2.rectangle(cv_img, start, end, bg_color, -1)
        # Move to next health bar
        curr_y -= dist_y

    # Grayscale and invert image so text is black on white
    cv_img = cv_img[:, :, ::-1].copy()
    cv_img = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
    cv_img = cv2.bitwise_not(cv_img)
    # cv2.imshow("image", cv_img)
    # cv2.waitKey(0)

    # Read percentages and split into array
    text = pytesseract.image_to_string(cv_img,
                                       config='-c tessedit_char_whitelist=0123456789%')
    text = text.replace("%", "")

    # i do not recall why i implemented this in the way that i did
    # TODO: there has to be a more elegant way to do this
    return ("".join([s for s in text.strip().splitlines(True) if
                     s.strip("\r\n")]).splitlines())
