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


def main():
	parser = argparse.ArgumentParser(description='Encrypt and decrypt specified files')
	parser.add_argument('-D', help='Directory to start encrypting files in', dest="directory", required="True")
	parser.add_argument('-R', help='Specify whether to recurse down directories', dest="recurse", default=False)
	parser.add_argument('-a', help='Action to perform [encrypt/decrypt]', dest="action", required="True")

	args = parser.parse_args()

	# if args.action != 'encrypt' and args.action != 'decrypt', throw an error


if __name__ == '__main__':
	sys.exit(main())
