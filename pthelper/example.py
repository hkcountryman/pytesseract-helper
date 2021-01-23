#!/usr/bin/env python3

from img_to_txt import *

def main():
    pic = "../images/resize.png"
    success = parse(pic, 90) # 50% seems good for ingredient lists
    print(success) # display text or failure message to user
    if success == "OCR failed.": # now we try our functions
        img = Image.open(pic)

        # pic = "../images/invert.png": try inverting
        #img = invert(img)

        # pic = "../images/resize.png": try resizing
        img = resize(img)

        img.save("temp.jpeg")
        print(parse("temp.jpeg", 50))


if __name__ == "__main__":
    main()

# I need a better way to resize than dpi and a better spell checker