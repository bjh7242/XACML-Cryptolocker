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
	enc_file = sys.argv[1] + ".enc"

	with open(sys.argv[1],"rb") as f:
		plaintext = f.read()
	
	#print data
	# ciphertext should be BBF316E8D940AF0AD3
	key = 'Key'
	#plaintext = 'Plaintext'

	# key is a list containing the key
	key = convert_key(key)

	# this is a generator variable
	keystream = RC4(key)
	f = open(enc_file,"wb")
	#hexval = []
	for c in plaintext:
		#print "ord(c) = " + str(ord(c))
		#print "keystream.next() = " + str(keystream.next())
		val = str(hex(ord(c) ^ keystream.next())).split('x')[1]
		if 1 == len(val):
			val = "0" + str(val)
		#hexval.append(val)
		f.write(binascii.a2b_hex(val))
	
	#f.write(binascii.unhexlify(''.join(hexval)))

	#print hexval
	f.close()

#	for c in plaintext:
#		sys.stdout.write("%02X" % (ord(c) ^ keystream.next()))
#	print
