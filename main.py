#!/usr/bin/env python

import os
import sys
import argparse
import xml.etree.ElementTree
from rc4 import rc4
from auth import auth
from xacmlparser import xacmlparser

def get_file_list(directory, recurse):
    """
    This function returns a list of files based off of the given directory and will recurse, if desired
    @param directory String containing the path to the directory in which to perform the requested operation
    @param recurse Boolean value indicating whether recursion down the directory structure is requested (True) or not (False)
    @return list containing full path to files
    """
    files = []

    # if directory recursion is not requested
    if recurse == False:
        filenames = os.listdir(directory)
        # if the last character in the directory name is a '/', don't readd it to the file path
        if directory[-1:] == "/":
            for f in filenames:
                if os.path.isdir(directory + f) is not True:
                    files.append(directory + f)
        else:
            for f in filenames:
                if os.path.isdir(directory + "/" + f) is not True:
                    files.append(directory + "/" + f)

    # if directory recursion is requested
    elif recurse == True:
        for root, dirs, filenames in os.walk(directory):
            if root[-1:] == "/":
                for f in filenames:
                    if os.path.isdir(directory + f) is not True:
                        files.append(root + f)
            else:
                for f in filenames:
                    if os.path.isdir(directory + "/" + f) is not True:
                        files.append(root + "/" + f)

    else:
        print "Something weird happened."
        sys.exit(1)

    return files

def perform_action(args):
    """
    Parses the command line args and executes the encryption or decryption process
    @param args The argparse object of command line args
    """
    r = rc4()            # initialize the rc4 class object (r)
    r.key = args.key    # set the key for the object to be the value from the command line

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
                # method call to decrypt the files
                r.rc4main(f,f[:-4])
                if args.cleanup:
                    if args.verbose:
                        print "Deleting " + f
                    os.remove(f)

    # else, if neither argument is specified, throw an error
    else:
        print "ERROR: -a must specify either 'encrypt' or 'decrypt' as an argument"
        sys.exit(1)

def main():
    """
    The main function
    """
    parser = argparse.ArgumentParser(description='Encrypt and decrypt specified files')
    parser.add_argument('-D', help='Directory to start encrypting files in', dest="directory", required="True")
    parser.add_argument('-R', help='Specify whether to recurse down directories', dest="recurse", action="store_true", default=False)
    parser.add_argument('-A', help='Action to perform [encrypt/decrypt]', dest="action", required="True")
    parser.add_argument('-K', help='The key to use with the RC4 cipher', dest="key", required="True")
    parser.add_argument('-C', help='Clean up (delete) the input files (default no)', dest="cleanup", action="store_true", default=False)
    parser.add_argument('-V', help='Verbose output', dest="verbose", action="store_true", default=False)

    args = parser.parse_args()

    # perform authentication
    login = auth()
    login.attempt_login()
    
    # if the login creds were not correct, exit the program
    if login.login == False:
        print "Unsuccessful login."
        sys.exit(1)

    # check if the action is either "encrypt" or "decrypt"
    if args.action == "encrypt":
        action = "Encrypt"
    elif args.action == "decrypt":
        action = "Decrypt"
    else:
        print "ERROR: the -A flag should have an argument of either encrypt or decrypt (case sensitive)"
        sys.exit(1)

    # check authorization for requested action here (attacker can encrypt, admin can enc/dec, etc)
    x = xacmlparser()
    e = xml.etree.ElementTree.parse('rights.xacml')
    root = e.getroot()

    # parse_action will return True if the user is authorized to perform the requested action
    execute = x.parse_action(root,login.group,action)

    if execute:
        perform_action(args)
    else:
        print "User is not authorized to perform the requested action"
        sys.exit(1)

if __name__ == '__main__':
    sys.exit(main())
