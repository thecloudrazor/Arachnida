import argparse
import requests
from bs4 import BeautifulSoup
import pathlib
import os
from urllib.parse import urlparse, urljoin
from time import sleep

EXTENSIONS = [".jpg", "jpeg", ".png", ".gif", ".bmp"]
DEFAULT_DEPTH = 5
DEFAULT_PATH = "./data/"
IMG_PATH = []
visited_urls = []
count = 0

RED = "\033[31m"
YELLOW = "\033[33m"
GREEN = "\033[32m"
RESET = "\033[0m"

header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0'}

def parse_args():
    parser = argparse.ArgumentParser(description="SpiderBot")
    parser.add_argument('-r', '--recursive', action='store_true', help='Download images recursively (to depth level 5 by default)')
    parser.add_argument('-l', '--level', dest='depth', type=int, help='Depth level of recursive image search')
    parser.add_argument('-p', '--path', type=pathlib.Path, help='Path to save downloaded images')
    parser.add_argument('URL', help='URL to download images from')
    
    args = parser.parse_args()

    if args.depth is None and not args.recursive:
        args.depth = DEFAULT_DEPTH
    elif args.depth and not args.recursive:
        parser.error("argument -l/--level: expected -r/--recursive argument.")
    elif args.recursive and args.depth is None:
        args.depth = DEFAULT_DEPTH

    if args.path is None:
        args.path = pathlib.Path(DEFAULT_PATH)
    
    args.current_depth = 0
    return args

def print_arg(args):
    print(f"{GREEN}Arguments:{RESET}")
    print(f"  {YELLOW}Recursive:{RESET} {args.recursive}")
    print(f"  {YELLOW}Depth:{RESET} {args.depth}")
    print(f"  {YELLOW}Path:{RESET} {args.path}")
    print(f"  {YELLOW}URL:{RESET} {args.URL}", "\n")

def check_url(args):
    if not args.URL.startswith('http://') and not args.URL.startswith('https://'):
        args.URL = 'http://' + args.URL
    try:
        response = requests.get(args.URL, timeout=10, headers=header)
        if response.status_code != 200:
            print(f"{RED}Error: Incorrect URL.{RESET}")
            exit(1)
    except requests.exceptions.RequestException as e:
        print(f"{RED}Error: {e}{RESET}")
        exit(1)

def check_path(args):
    if not args.path.exists():
        args.path.mkdir(parents=True, exist_ok=True)
    elif not args.path.is_dir():
        print(f"{RED}Error: The specified path '{args.path}' is not a directory.{RESET}")
        exit(1)

def is_visited(url):
    return url in visited_urls


def mark_as_visited(url):
    visited_urls.append(url)

def get_image(args, current_depth=0):
    if current_depth >= args.depth:
        return

    if is_visited(args.URL):
        return
    mark_as_visited(args.URL)

    try:
        response = requests.get(args.URL, timeout=10, headers=header)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            images = soup.find_all('img')

            for img in images:
                src = img.get('src')
                if src:
                    img_url = urljoin(args.URL, src)
                    if any(img_url.endswith(ext) for ext in EXTENSIONS) and img_url not in IMG_PATH:
                        IMG_PATH.append(img_url)

            if args.recursive:
                base_url = urlparse(args.URL).netloc
                links = soup.find_all('a', href=True)
                for link in links:
                    href = link['href']
                    href_parsed = urlparse(href)
                    if href_parsed.netloc == base_url and not is_visited(href):
                        new_args = argparse.Namespace(URL=href, recursive=args.recursive, depth=args.depth, path=args.path)
                        print(f"{YELLOW}Following URL [Depth: {current_depth + 1}]:{RESET}{GREEN} {href} {RESET}")
                        sleep(0.1)
                        get_image(new_args, current_depth + 1)

        else:
            print(f"{RED}Error: HTTP {response.status_code}{RESET}")
    except requests.exceptions.RequestException as e:
        print(f"{RED}Error: {e}{RESET}")



def save_images(args):
    global count
    for img_url in IMG_PATH:
        try:
            file_name = img_url.split("/")[-1]
            save_path = args.path / file_name

            if os.path.exists(save_path):
                print(f"{YELLOW}File already exists: {save_path} - Skipping.{RESET}")
                continue

            img_data = requests.get(img_url, timeout=10, headers=header).content
            with open(save_path, 'wb') as handler:
                handler.write(img_data)

            count += 1
            print(f"{GREEN}Image saved: {save_path}{RESET}")
            sleep(0.1)
        except Exception as e:
            print(f"{RED}Error: {img_url} could not be saved. {e}{RESET}")

def main():
    args = parse_args()
    print_arg(args)
    check_path(args)
    check_url(args)
    print(f"{GREEN}Initiating scanning process...{RESET}")
    sleep(1)
    get_image(args)
    print(f"{GREEN}Initiating download...{RESET}")
    sleep(1)
    save_images(args)
    print(f"{GREEN}Total downloaded images: {count}{RESET}")

if __name__ == "__main__":
    main()
