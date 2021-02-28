import cv2 as cv
from deskew import determine_skew
import numpy as np
from PIL import Image, ImageFilter, ImageOps
from pytesseract import image_to_string
from skimage import io
from skimage.color import rgb2gray
from skimage.transform import rotate
from spellchecker import SpellChecker
import traceback

# On Windows, you need to tell it where Tesseract is installed, for example:
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe

# OCR Stuff
####################################################################################################
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
        quit()
    except PIL.UnidentifiedImageError as e:
        print("That file is not an image.")
        quit()
    except:
        print("Unanticipated error:")
        traceback.print_exc()
        quit()
    remove_alpha(img)
    text = image_to_string(img)
    return text

def valid_text(ocr, accuracy_pct, language="en", distance=2, case_sensitive=True): # this spellchecker sucks
    """
    Checks that the output of to_text() makes sense. To build your own dictionary, see
    https://pyspellchecker.readthedocs.io/en/latest/quickstart.html#how-to-build-a-new-dictionary

    Args:
        ocr: string to analyze.
        accuracy_pct: percentage of words in ocr that should be in the dictionary.
        language: language of dictionary (default English); see
            https://pyspellchecker.readthedocs.io/en/latest/quickstart.html#changing-language
        distance: Levenshtein distance (default 2 for shorter words); see
            https://pyspellchecker.readthedocs.io/en/latest/quickstart.html#basic-usage
            https://en.wikipedia.org/wiki/Levenshtein_distance
    
    Returns:
        Boolean indicating success of to_text():
            True: to_text() makes sense.
            False: to_text() returned nonsense.
    """
    if ocr == "":
        return False # if it returned nothing

    word_list = ocr.split() # get list of all words in input string
    spell = SpellChecker(language=language, distance=distance, case_sensitive=case_sensitive)
    misspelled = spell.unknown(word_list) # list of unknown words from word_list
    #print(misspelled)
    #print(word_list)
    if (len(word_list) - len(misspelled)) / len(word_list) < accuracy_pct / 100:
        return False # if it returned gibberish
    
    return True # otherwise, all good

def parse(pic, accuracy_pct, language="en", distance=2, case_sensitive=True):
    """
    Attempts OCR with image and decides if processing is needed.
    
    Args:
        pic: filename string, pathlib.Path object, or file object to read.
        accuracy_pct: percentage of words in string that should be in the dictionary.
        language: language of dictionary (default English); see
            https://pyspellchecker.readthedocs.io/en/latest/quickstart.html#changing-language
        distance: Levenshtein distance (default 2 for shorter words); see
            https://pyspellchecker.readthedocs.io/en/latest/quickstart.html#basic-usage
            https://en.wikipedia.org/wiki/Levenshtein_distance

    Returns:
        Text from the image if OCR was successful; otherwise a failure message.
    """
    text = to_text(pic)
    if valid_text(text, accuracy_pct, language=language, distance=distance,
                    case_sensitive=case_sensitive):
        return text
    else:
        return "OCR failed." # time for processing

# Image Processing Stuff
####################################################################################################

def remove_alpha(pic):
    """
    Removes the alpha channel from an image, if it exists. Necessary for OCR.

    Args:
        pic: PIL.Image object to convert.
    
    Returns:
        The PIL.Image object in RGB format.
    """
    return pic.convert("RGB")

def invert(pic):
    """
    Inverts the colors in an image. Useful if OCR doesn't work.

    Args:
        pic: PIL.Image object to invert.

    Returns:
        The inverted PIL.Image object.
    """
    return ImageOps.invert(remove_alpha(pic)) # negative colors

'''def resize(pic): # needs work: possible key error "dpi"
    """
    Resizes an image that is less than 300 dpi. Useful if OCR doesn't work.

    Args:
        pic: PIL.Image object to resize.

    Returns:
        The resized PIL.Image object.
    """
    pic = remove_alpha(pic)
    res = pic.info["dpi"] # fetch tuple of dpi
    lower = min(res) # get the lower of the two entries in the tuple
    factor = 300 / lower # how much should we scale?
    resized = pic.resize((round(pic.size[0]*factor), round(pic.size[1]*factor))) # scale it!
    return resized'''

def threshold(pic, gaussian=True): # needs work
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

def denoise(pic): # needs work
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

def dilate(pic, size):
    """
    Dilates the text (grows edges of characters) if it's against a common background.
    Useful if OCR doesn't work.

    Args:
        pic: PIL.Image object to dilate.
        size: kernel size, in pixels. Recommend starting at 1.

    Returns:
        The dilated PIL.Image object.
    """
    pic = remove_alpha(pic)
    return pic.filter(ImageFilter.MaxFilter(size))

def erode(pic, size):
    """
    Erodes the text (shrinks edges of characters) if it's against a common background.
    Useful if OCR doesn't work.

    Args:
        pic: PIL.Image object to erode.
        size: kernel size, in pixels. Recommend starting at 1.

    Returns:
        The eroded PIL.Image object.
    """
    pic = remove_alpha(pic)
    return pic.filter(ImageFilter.MinFilter(size))

def deskew(pic, output): # needs work
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
    rotated = rotate(img, angle, resize=True) * 255
    io.imsave(output, rotated.astype(np.uint8))
    