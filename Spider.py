import argparse
import requests
from bs4 import BeautifulSoup
import pathlib
import os

EXTENSIONS = [".jpg", "jpeg", ".png", ".gif", ".bmp"]
DEFAULT_DEPTH = 5
DEFAULT_PATH = "./data/"
IMG_PATH = []
header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}
count = 0

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
    print(f"	Recursive: {args.recursive}")
    print(f"	Depth: {args.depth}")
    print(f"	Path: {args.path}")
    print(f"	URL: {args.URL}", "\n")

def check_url(args):
    if not args.URL.startswith('http://') and not args.URL.startswith('https://'):
        args.URL = 'http://' + args.URL
    try:
        response = requests.get(args.URL, timeout=10, headers=header)
        if response.status_code != 200:
            print("Error: Incorrect URL.")
            exit(1)
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        exit(1)

def check_path(args):
    if args.path:
        path = pathlib.Path(args.path)
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        elif not path.is_dir():
            print(f"Error: The specified path '{args.path}' is not a directory.")
            exit(1)

def get_image(args, current_depth=1):
    if current_depth > args.depth:
        return

    try:
        response = requests.get(args.URL, timeout=10, headers=header)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            images = soup.find_all('img')

            for img in images:
                src = img.get('src')
                if src and any(src.endswith(ext) for ext in EXTENSIONS):
                    if src not in IMG_PATH:
                        IMG_PATH.append(src)

            if args.recursive:
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    if href.startswith('http'):
                        new_args = argparse.Namespace(URL=href, recursive=args.recursive, depth=args.depth, path=args.path)
                        get_image(new_args, current_depth + 1)
        else:
            print(f"error: HTTP {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"error: {e}")

def save_images(args):
    global count
    for img_url in IMG_PATH:
        try:
            if not img_url.startswith(('http://', 'https://')):
                img_url = 'http://' + img_url.lstrip('//')

            file_name = img_url.split("/")[-1]
            save_path = args.path / file_name

            if not any(file_name.endswith(ext) for ext in EXTENSIONS):
                print(f"Invalid format: {img_url} - Skipping.")
                continue

            if os.path.exists(save_path):
                print(f"File already exists: {save_path} - Skipping.")
                continue

            img_data = requests.get(img_url, timeout=10, headers=header).content
            with open(save_path, 'wb') as handler:
                handler.write(img_data)

            count += 1
            print(f"Image saved: {save_path}")
        except Exception as e:
            print(f"Error: {img_url} could not be saved. {e}")

def main():
    args = parse_args()
    print_arg(args)
    check_path(args)
    check_url(args)
    print("initiating scanning process...")
    get_image(args)
    print("initiating download...")
    save_images(args)
    print ("total downloaded images: " ,count)

if __name__ == "__main__":
    main()
