#!/usr/bin/env python3

from img_to_txt import *

def main():
    success = parse("../images/test.jpg", 50) # 50% seems good for ingredient lists
    print(success) # display text or failure message to user
    #if success == "OCR failed.": # now we try our functions
        #

if __name__ == "__main__":
    main()