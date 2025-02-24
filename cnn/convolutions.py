# import the necessary packages
from skimage.exposure import rescale_intensity
import numpy as np
import argparse
import cv2

def convolve(image, k):
    # grab the spatial dimensions of the image kernel
    (iH, iW) = image.shape[:2]
    (kH, kW) = k.shape[:2]

    # alocate memory to the output image, taking care to pad the borders of the input image so that the spatial size (i.e, width and height are not reduced)
    pad = (kW-1)//2
    image = cv2.copyMakeBorder(image, pad, pad, pad, pad,
                               cv2.BORDER_REPLICATE)
    output = np.zeros((iH, iW), dtype="float")

    # loop over the input image, "sliding" the kernel accross each (x, y)-coordinate from left-to-right and top-to-bottom
    for y in np.arange(pad, iH+pad):
        for x in np.arange(pad, iW+pad):
            # extract the roi of the image by extracting the center region of the current, (x, y) coordinates dimension
            roi = image[y - pad:y+pad+1, x - pad:x+pad+1]

            # perform the actual convolution by taking the element wise multiplication between the ROI and the kernel
            k = (roi*K).sum()

            # store the convolved value in the output (x, y) coordinate of the output image
            output[y - pad, x - pad] = k

    # rescale teh output image to be in the range [0, 255]
    output = rescale_intensity(output, in_range=(0, 255))
    output = (output*255).astype("uint8")

    # return the output image
    return output

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True,
                help="path to input image")
args = vars(ap.parse_args())

# construct average blurring kernels used to smooth image
smallBlur = np.ones((7, 7), dtype="float")*(1.0/(7*7))
largerBlur = np.ones((21, 21), dtype="float")*(1.0/(7*7))

# construct a sharpening filter
sharpen = np.array((
[0, -1, 0],
[-1, 5, -1],
[0, -1, 0]), dtype = "int")

# construct laplacian kernel used to detect edge like regions of an image
laplacian = np.array((
[0, 1, 0],
[1, -4, 1],
[0, 1, 0]), dtype="int")

# construct the sobel x-axis kernel
sobelX = np.array((
[-1, 0, 1],
[-2, 0, 2],
[-1, 0, 1]), dtype="int")

# construct the sobel y-axis kernel
sobelY = np.array((
[-1, -2, -1],
[0, 0, 0],
[1, 2, 1]), dtype="int")

# construct an emboss kernel
emboss = np.array((
[-2, -1, 0],
[-1, 1, 1],
[0, 1, 2]), dtype="int")

# construct the kernel bank, a list of kernels we're going to apply using both our custom 'convolve' function and OpenCCV's 'filter2D' function
kernelBank = (
    ("small_blur", smallBlur),
    ("large blur", largerBlur),
    ("sharpen", sharpen),
    ("laplacian", laplacian),
    ("sobel_x", sobelX),
    ("sobel_y", sobelY),
    ("emboss", emboss))

# load the input image and convert it to grayscale
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# loop over the kernels
for (kernelName, K) in kernelBank:
    # apply the kernel to the grayscale image using both our custom convolve function and OpenCV's 'filter2D' funcction
    print("[INFO] applying {} kernel".format(kernelName))
    convolveOutput = convolve(gray, K)
    openCVOutput = cv2.filter2D(gray, -1, K)

    # show the output image
    cv2.imshow("Original", gray)
    cv2.imshow("{} - convolve".format(kernelName), convolveOutput)
    cv2.imshow("{} - opencv".format(kernelName), openCVOutput)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
