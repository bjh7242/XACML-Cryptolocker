#!/usr/bin/env python

import os
import sys
import argparse


def encrypt(files):
	"""
	This function encrypts the specified file using RC4
	Args: list of files to encrypt
	"""
	pass

def decrypt(files):
	"""
	This function decrypts the specified file that was encrypted using RC4
	Args: list of files to decrypt
	"""
	pass

def get_file_list(directory, recurse):
	"""
	This function returns a list of files based off of the given directory and 
	will recurse, if desired
	"""
	files = []
	
	if recurse == False:
		print "Recurse false"

	elif recurse == True:
		print "Recurse true"

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
		encrypt(get_file_list(args.directory, args.recurse))

	elif args.action == "decrypt":
		print "Decrypting files..."
		decrypt(get_file_list(args.directory, args.recurse))

	# else, if neither argument is specified, throw an error
	else:
		print "ERROR: -a must specify either 'encrypt' or 'decrypt' as an argument"
		sys.exit(1)

	return 0


if __name__ == '__main__':
	sys.exit(main())
