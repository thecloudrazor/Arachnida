import requests
from bs4 import BeautifulSoup
import sys

option_r = False
option_l = 5
option_p = "./data/"
url = ""

def ft_err(msg):
    print(msg)
    exit(1)

def check_arg(ac,av):
    global option_l, option_p, option_r

    i = 1
    while i < ac:
        arg = av[i]
        if arg == "-r":
            option_r = True
        elif arg == "-l":
            if i + 1 < ac and av[i + 1].isdigit():
                option_l = int(av[i + 1])
                i += 1
            else:
                ft_err("Option -l requires a number after it.")
        elif arg == "-p":
            if i + 1 < ac:
                option_p = av[i + 1]
                i += 1
        else:
            ft_err(f"Invalid option {arg}")
        i += 1
    print("option_l:", option_l)
    print("option_p:", option_p)
    print("option_r:", option_r)


def main():
    if (len(sys.argv) < 2):
        ft_err("Usage: python3 spider.py [-r] [-l] [depth level] [-p] [path] [URL]")
    check_arg(len(sys.argv) - 1 , sys.argv)

if (__name__ == "__main__"):
    main()