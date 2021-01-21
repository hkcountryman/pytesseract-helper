#!/usr/bin/env python3

from img_to_txt import *

def main():
    print(parse("../images/test.jpg", 50)) # 50% seems good for ingredient lists

if __name__ == "__main__":
    main()