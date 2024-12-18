import argparse
import requests
from bs4 import BeautifulSoup
import pathlib

EXTENSIONS = [".jpg", "jpeg", ".png", ".gif", ".bmp"]
DEFAULT_DEPTH = 5
DEFAULT_PATH = "./data/"

def parse_args():
    parser = argparse.ArgumentParser(description="SpiderBot")
    parser.add_argument('-r', '--recursive', action='store_true', help='Download images recursively (to depth level 5 by default)')
    parser.add_argument('-l', '--level', dest='depth', type=int, help='Depth level of recursive image search')
    parser.add_argument('-p', '--path', type=pathlib.Path, help='Path to save downloaded images')
    parser.add_argument('URL', help='URL to download images from')
    
    args = parser.parse_args()
    if args.depth is None:
        if args.recursive:
            args.depth = DEFAULT_DEPTH
        else:
            args.depth = 1
    elif args.depth and (args.recursive is False):
        parser.error("argument -l/--level: expected -r/--recursive argument.")
    if args.path is None:
        args.path = pathlib.Path(DEFAULT_PATH)
    args.current_depth = 0
    return args

def print_arg(args):
    print("Arguments:")
    print(f"Recursive: {args.recursive}")
    print(f"Depth: {args.depth}")
    print(f"Path: {args.path}")
    print(f"URL: {args.URL}")

def check_url(args):
    url = args.URL
    if not url.startswith('http://') and not url.startswith('https://'):
        url = 'http://' + url
    try:
        response = requests.get(url)
        if (response.status_code != 200):
            print("error: incorrect url")
            exit(1)
    except requests.exceptions.RequestException as e:
        print(f"error: {e}")
        exit(1)

def check_path(args):
    if args.path:
        path = pathlib.Path(args.path)

        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        elif not path.is_dir():
            print(f"Error: The specified path '{args.path}' is not a directory.")
            exit(1)
        else:
            print(f"Path '{args.path}' is a valid directory.")

def main():
    args = parse_args()
    print_arg(args)
    check_path(args)
    check_url(args)

    print("Scraping işlemleri başlatılıyor...")

if __name__ == "__main__":
    main()
