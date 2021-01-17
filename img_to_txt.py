from PIL import Image
import PIL.Image
from pytesseract import image_to_string
import pytesseract

# On Windows, you need to tell it where Tesseract is installed, for example:
# pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe

def to_text(pic):
    img = Image.open(pic)
    text = pytesseract.image_to_string(img)
    return text

print(to_text("test.jpg"))