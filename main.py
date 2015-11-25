#!/usr/bin/env python

import os
import sys
import argparse
from rc4 import rc4


def get_file_list(directory, recurse):
	"""
	This function returns a list of files based off of the given directory and 
	will recurse, if desired
	"""
	files = []
	print "directory[-1:] = " + directory[-1:]

	# if directory recursion is not requested
	if recurse == False:
		print "Recurse false"
		filenames = os.listdir(directory)
		# if the last character in the directory name is a '/', don't readd it to the file path
		if directory[-1:] == "/":
			for f in filenames:
				if os.path.isdir(f) is not True:
					files.append(directory + f)
		else:
			for f in filenames:
				if os.path.isdir(f) is not True:
					files.append(directory + "/" + f)

	# if directory recursion is requested
	elif recurse == True:
		print "Recurse true"
		for root, dirs, filenames in os.walk(directory):
			#for f in filenames:
			#	print root + f
			if root[-1:] == "/":
				for f in filenames:
					if os.path.isdir(f) is not True:
						files.append(root + f)
			else:
				for f in filenames:
					if os.path.isdir(f) is not True:
						files.append(root + "/" + f)

	else:
		print "Something weird happened."
		sys.exit(1)

	return files

def main():
	parser = argparse.ArgumentParser(description='Encrypt and decrypt specified files')
	parser.add_argument('-D', help='Directory to start encrypting files in', dest="directory", required="True")
	parser.add_argument('-R', help='Specify whether to recurse down directories', dest="recurse", action="store_true", default=False)
	parser.add_argument('-a', help='Action to perform [encrypt/decrypt]', dest="action", required="True")

	args = parser.parse_args()

	# if args.action is neither 'encrypt' nor 'decrypt', throw an error
	if args.action == "encrypt":
		print "Encrypting files..."
		files = get_file_list(args.directory, args.recurse)
		for f in files:
			print f

	elif args.action == "decrypt":
		print "Decrypting files..."
		files = get_file_list(args.directory, args.recurse)

	# else, if neither argument is specified, throw an error
	else:
		print "ERROR: -a must specify either 'encrypt' or 'decrypt' as an argument"
		sys.exit(1)

	return 0


if __name__ == '__main__':
	sys.exit(main())
