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
	#print "directory[-1:] = " + directory[-1:]

	# if directory recursion is not requested
	if recurse == False:
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
		for root, dirs, filenames in os.walk(directory):
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
	parser.add_argument('-V', help='Verbose output', dest="verbose", action="store_true", default=False)

	args = parser.parse_args()
	r = rc4()
	r.key = 'Key2'

	# if args.action is neither 'encrypt' nor 'decrypt', throw an error
	if args.action == "encrypt":
		if args.verbose:
			print "Encrypting files..."
		files = get_file_list(args.directory, args.recurse)
		for f in files:
			# add ".enc" to the end of each encrypted file
			if args.verbose:
				print "Encrypting " + f
			enc_file = f + ".enc"
			r.rc4main(f,enc_file)

	elif args.action == "decrypt":
		if args.verbose:
			print "Decrypting files..."
		files = get_file_list(args.directory, args.recurse)
		for f in files:
			if f[-4:] == ".enc":
				if args.verbose:
					print "Decrypting " + f
				r.rc4main(f,f[-4:])

	# else, if neither argument is specified, throw an error
	else:
		print "ERROR: -a must specify either 'encrypt' or 'decrypt' as an argument"
		sys.exit(1)

	return 0


if __name__ == '__main__':
	sys.exit(main())
