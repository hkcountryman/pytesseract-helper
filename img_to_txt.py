import cv2 as cv
from deskew import determine_skew
import numpy as np
from PIL import Image, ImageFilter, ImageOps
from pytesseract import image_to_string
from skimage import io
from skimage.color import rgb2gray
from skimage.transform import rotate
import traceback

# On Windows, you need to tell it where Tesseract is installed, for example:
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe

def to_text(pic):
    """
    Read and return text from an image.

    Args:
        pic: filename string, pathlib.Path object, or file object to read.

    Returns:
        Text from the image.
    """
    try:
        img = Image.open(pic)
    except FileNotFoundError as e:
        print("File " + pic + " does not exist.")
        return ""
    except PIL.UnidentifiedImageError as e:
        print("That file is not an image.")
        return ""
    except:
        print("Unanticipated error:")
        traceback.print_exc()
        quit()
    text = image_to_string(img)
    return text

#print(to_text("test.jpg"))

def no_alpha(pic):
    """
    Removes the alpha channel from an image, if it exists. Necessary for OCR.

    Args:
        pic: filename string, pathlib.Path object, or file object to read.
    
    Returns:
        The image in RGB format.
    """
    img = Image.open(pic)
    return img.convert("RGB")

def invert(pic):
    """
    Inverts the colors in an image. Useful if OCR doesn't work.

    Args:
        pic: filename string, pathlib.Path object, or file object to read.

    Returns:
        The inverted image.
    """
    img = Image.open(pic)
    img = img.convert("RGB") # convert to RGB
    return ImageOps.invert(img) # negative colors

#print(to_text("ghbio.png"))
#pic = invert("ghbio.png")
#pic.save("inverted.png")
#print(to_text("inverted.png"))

def resize(pic):
    """
    Resizes an image that is less than 300 dpi. Useful if OCR doesn't work.

    Args:
        pic: filename string, pathlib.Path object, or file object to read.

    Returns:
        The resized image.
    """
    img = Image.open(pic)
    res = img.info["dpi"] # fetch tuple of dpi
    lower = min(res) # get the lower of the two entries in the tuple
    factor = 300 / lower # how much should we scale?
    resized = img.resize((round(img.size[0] * factor), round(img.size[1] * factor))) # scale it!
    return resized

#pic = resize("test.jpg")
#pic.save("resized.jpg")
#print(to_text("resized.jpg"))

def threshold(pic, gaussian = True):
    """
    Applies thresholding to the image. Doesn't work.
    (Tesseract already tries the Otsu algorithm.)

    Args:
        pic: filename string, pathlib.Path object, or file object to read.
        gaussian: boolean:
            True: apply adaptive Gaussian thresholding.
            False: apply adaptive mean thresholding.
    
    Returns:
        The image with thresholding.
    """
    img = cv.imread("test2.jpg", 0)
    if gaussian: # adaptive Gaussian thresholding
        img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_GAUSSIAN_C, cv.THRESH_BINARY, 11, 2)
    else: # adaptive mean thresholding
        img = cv.adaptiveThreshold(img, 255, cv.ADAPTIVE_THRESH_MEAN_C, cv.THRESH_BINARY, 11, 2)
    return Image.fromarray(img)

def denoise(pic): # It does not work :(
    """
    Allegedly removes noise? Useful if OCR doesn't work.

    Args:
        pic: filename string, pathlib.Path object, or file object to read.

    Returns:
        The denoised image.
    """
    img = cv.imread(pic)
    img = cv.fastNlMeansDenoising(img)
    return Image.fromarray(img)

#print(to_text("test2.jpg"))
#pic = threshold("test2.jpg", gaussian = True)
#pic.save("anotherTry.png")
#pic = denoise("anotherTry.png")
#pic.save("anotherTry.png")
#print(to_text("anotherTry.png"))
#pic = threshold("test2.jpg", gaussian = False)
#pic.save("anotherTry2.png")
#print(to_text("anotherTry2.png"))
#pic = denoise("anotherTry2.png")
#pic.save("testing123.png")
#print(to_text("testing123.png"))

def dilate(pic, size):
    """
    Dilates the text (grows edges of characters) if it's against a common background.
    Useful if OCR doesn't work.

    Args:
        pic: filename string, pathlib.Path object, or file object to read.
        size: kernel size, in pixels. Recommend starting at 1.

    Returns:
        The dilated image.
    """
    img = Image.open(pic)
    return img.filter(ImageFilter.MaxFilter(size))

#print(to_text("Dilation_original.png"))
#pic = dilate("Dilation_original.png", 1)
#pic.save("Dilation_dilated.png")
#print(to_text("Dilation_dilated.png"))

def erode(pic, size):
    """
    Erodes the text (shrinks edges of characters) if it's against a common background.
    Useful if OCR doesn't work.

    Args:
        pic: filename string, pathlib.Path object, or file object to read.
        size: kernel size, in pixels. Recommend starting at 1.

    Returns:
        The eroded image.
    """
    img = Image.open(pic)
    return img.filter(ImageFilter.MinFilter(size))

def deskew(pic, output):
    """
    Deskews an image. Useful if OCR doesn't work.

    Args:
        pic: filename string, pathlib.Path object, or file object to read.
        output: string to save output as
    """
    # Thanks to Stephane Brunner (https://github.com/sbrunner) for deskew and the code!
    img = io.imread(pic)
    grayscale = rgb2gray(img)
    angle = determine_skew(grayscale)
    rotated = rotate(img, angle, resize = True) * 255
    io.imsave(output, rotated.astype(np.uint8))

#print(to_text("input.jpeg"))
#deskew("input.jpeg", "deskewed.jpeg")
#print(to_text("deskewed.jpeg"))

#print(to_text("Erosion_original.png"))
#pic = erode("Erosion_original.png", val)
#pic.save("Erosion_eroded.png")
#print(to_text("Erosion_eroded.png"))

#To Do:
# borders
# should I not be opening the image in every function?