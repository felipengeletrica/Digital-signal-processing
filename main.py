from math import *


def main():

    for wn in range(1, 6):

        if wn != 3:
            res = (sin(((2*pi*(8000/44100))*pi) * (wn - 3)))/((wn - 3)*pi)
            print(res)
        else:
            print(0)


if __name__ == '__main__':
    main()