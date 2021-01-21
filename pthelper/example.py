#!/usr/bin/env python3

from img_to_txt import *

def main():
    text = to_text("../images/test.jpg")
    if valid_text(text, 75):
        print(text)
    else:
        print("OCR failed.")

if __name__ == "__main__":
    main()