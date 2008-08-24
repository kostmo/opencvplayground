from opencv import cv

#############################################################################
# some useful functions

def hsv2rgb (hue):
    # convert the hue value to the corresponding rgb value

    sector_data = [[0, 2, 1],
                   [1, 2, 0],
                   [1, 0, 2],
                   [2, 0, 1],
                   [2, 1, 0],
                   [0, 1, 2]]
    hue *= 0.1 / 3
    sector = cv.cvFloor (hue)
    p = cv.cvRound (255 * (hue - sector))
    if sector & 1:
        p ^= 255

    rgb = {}
    rgb [sector_data [sector][0]] = 255
    rgb [sector_data [sector][1]] = 0
    rgb [sector_data [sector][2]] = p

    return cv.cvScalar (rgb [2], rgb [1], rgb [0], 0)

