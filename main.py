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
	parser.add_argument('-A', help='Action to perform [encrypt/decrypt]', dest="action", required="True")
	parser.add_argument('-K', help='The key to use with the RC4 cipher', dest="key", required="True")
	parser.add_argument('-C', help='Clean up (delete) the original unencrypted files (default no)', dest="cleanup", action="store_true", default=False)
	parser.add_argument('-V', help='Verbose output', dest="verbose", action="store_true", default=False)

	args = parser.parse_args()
	r = rc4()			# initialize the rc4 class object (r)
	r.key = args.key	# set the key for the object to be the value from the command line

	# if args.action is neither 'encrypt' nor 'decrypt', throw an error
	if args.action == "encrypt":
		if args.verbose:
			print "Encrypting files..."
		files = get_file_list(args.directory, args.recurse)
		for f in files:
			# don't run on already encrypted files, it will decrypt them
			if f[-4:] != ".enc":
				# add ".enc" to the end of each encrypted file
				if args.verbose:
					print "Encrypting " + f
				enc_file = f + ".enc"
				# encrypt the files
				r.rc4main(f,enc_file)
				# if requested, delete the original files
				if args.cleanup:
					if args.verbose:
						print "Deleting " + f
					os.remove(f)

	elif args.action == "decrypt":
		if args.verbose:
			print "Decrypting files..."
		files = get_file_list(args.directory, args.recurse)
		for f in files:
			if f[-4:] == ".enc":
				if args.verbose:
					print "Decrypting " + f
				r.rc4main(f,f[:-4])

	# else, if neither argument is specified, throw an error
	else:
		print "ERROR: -a must specify either 'encrypt' or 'decrypt' as an argument"
		sys.exit(1)

	return 0


if __name__ == '__main__':
	sys.exit(main())
