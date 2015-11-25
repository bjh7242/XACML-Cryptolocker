#!/usr/bin/env python
# modified from https://github.com/bozhu/RC4-Python
# test vectors are from http://en.wikipedia.org/wiki/RC4

import sys
import binascii

def KSA(key):
	keylength = len(key)

	S = range(256)

	j = 0
	for i in range(256):
		j = (j + S[i] + key[i % keylength]) % 256
		S[i], S[j] = S[j], S[i]  # swap

	return S


def PRGA(S):
	i = 0
	j = 0
	while True:
		i = (i + 1) % 256
		j = (j + S[i]) % 256
		S[i], S[j] = S[j], S[i]  # swap

		K = S[(S[i] + S[j]) % 256]
		yield K


def RC4(key):
	S = KSA(key)
	return PRGA(S)


def convert_key(s):
	return [ord(c) for c in s]


if __name__ == '__main__':
	# add .enc to filename to write the encrypted file to
	enc_file = sys.argv[1] + ".enc"
	key = 'Key'		# key for RC4

	with open(sys.argv[1],"rb") as f:
		plaintext = f.read()
	

	# key is a list containing the key
	key = convert_key(key)

	# this is a generator variable
	keystream = RC4(key)

	# open the file to write the encrypted contents to
	f = open(enc_file,"wb")

	for c in plaintext:
		val = str(hex(ord(c) ^ keystream.next())).split('x')[1]
		# if the hex value only has one character (ex. 0x9), add a 0 before it
		# this fixes the binascii "odd length string" error
		if 1 == len(val):
			val = "0" + str(val)
		f.write(binascii.a2b_hex(val))
	

	f.close()

