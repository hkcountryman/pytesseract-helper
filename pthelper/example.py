#!/usr/bin/env python3

import os
from typing import Callable

from img_to_txt import *

def testFun(name:str, fun:Callable, spellCheck:int):
    pic = os.path.join(os.getcwd(), "images", name)
    success = parse(pic, spellCheck) # 50% seems good for ingredient lists
    print(success) # display text or failure message to user
    if success == "OCR failed.": # now we try our functions
        img = Image.open(pic)
        if fun == invert:
            img = invert(img)
        img.save("temp.jpeg")
        print(parse("temp.jpeg", 50))

def main():
    testFun("invert.png", invert, 100)


if __name__ == "__main__":
    main()

# I need a better way to resize than dpi and a better spell checker