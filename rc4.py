#!/usr/bin/env python
"""
modified from https://github.com/bozhu/RC4-Python
"""

import binascii

class rc4:
    """ Class for RC4"""

    def __init__(self):
        """
        The constructor
        @param self The object
        """
        self.key = 'Key'    # default key is 'Key'
        self.infile = ''
        self.outfile = ''
    
    def KSA(self,key):
        """
        Completes the key-scheduling algorithm
        @param self The object
        @param key String containing the key to use
        @return list S
        """
        keylength = len(key)
    
        S = range(256)
    
        j = 0
        for i in range(256):
            j = (j + S[i] + key[i % keylength]) % 256
            S[i], S[j] = S[j], S[i]  # swap
    
        # return list S
        return S
    
    def PRGA(self,S):
        """
        Completes the pseudo-random generation algorithm
        @param self The object
        @param S the list created from the key
        @returns a generator K
        """
        i = 0
        j = 0
        while True:
            i = (i + 1) % 256
            j = (j + S[i]) % 256
            S[i], S[j] = S[j], S[i]  # swap
    
            K = S[(S[i] + S[j]) % 256]
            yield K
    
    def RC4(self,key):
        """
        Runs both parts of the RC4 cipher
        @param self The object
        """
        S = self.KSA(key)
        return self.PRGA(S)
    
    def convert_key(self,key):
        """
        Returns the decimal value of the characters in the key
        @param self The object
        @param key The string containing the key
        @return a generator containing values from the key
        """
        return [ord(c) for c in key]

    def rc4main(self,infile,outfile):
        """
        Starts the main processing of RC4 for the specified file (infile)
        Writes out the encrypted result to (outfile)
        @param self The object
        @param infile String containing the input filename
        @param outfile String containing the output filename
        """
        
        # read the infile in
        with open(infile,"rb") as f:
            plaintext = f.read()
        
        # key is a list containing the key
        key = self.convert_key(self.key)
    
        # this is a generator variable
        keystream = self.RC4(key)
    
        # open the file to write the encrypted contents to
        f = open(outfile,"wb")
    
        for c in plaintext:
            val = str(hex(ord(c) ^ keystream.next())).split('x')[1]
            # if the hex value only has one character (ex. 0x9), add a 0 before it
            # this fixes the binascii "odd length string" error
            if 1 == len(val):
                val = "0" + str(val)
            f.write(binascii.a2b_hex(val))

        f.close()
    
