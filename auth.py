#!/usr/bin/env python
"""
Authenticates with the "shadow" file in the same directory
"""

import getpass
import hashlib
import os

class auth:
    login = False
    username = ''
    group = ''
    passhash = ''

    def attempt_login(self):
        """
        Perform username and password authentication for a user
        Shadow file format:
            username:password hash:date last pass change:min password age:max pass age:pass warning period:pass inactivity period:account expeiration date:reserved field
            Note: the 'reserved field' contains the roles for each user (used for the XACML permissions)
        @param self The object 
        @return True for successful authentication, False for unsuccessful
        """
        self.username = raw_input("Enter Username: ")
        password = getpass.getpass("Enter Password: ")
        passhash = self.get_hash(password)

        with open('shadow','r') as f:
            for user in f:
                tmp = user.strip()
                if tmp.split(':')[0] == self.username:
                    if tmp.split(':')[1] == passhash:
                        self.passhash = passhash
                        self.login = True
                        self.group = tmp.split(':')[8]
    
        return self.login
    
    def update_password(self,newhash):
        """
        Permit an authenticated user to update a password
        @param self The object 
        @param newhash String containing the hash of the new user password
        """
        # check that user is authenticated
        if self.login:
            # open temporary file to write to
            tmpfile = open('shadow.tmp','w')
            with open('shadow','r+') as f:
                for user in f:
                    if self.username == user.split(':')[0]:
                        # update the password hash value
                        user.split(':')[1] = newhash
                        # update the hash value for the object
                        self.passhash = newhash
                    # write the users to a temp file
                    tmpfile.write(user)
            tmpfile.close()
            # overwrite old shadow file
            os.rename('shadow.tmp','shadow')
            #os.remove('shadow.tmp')

    def get_hash(self,password):
        """
        Gets the SHA512 hash of a specified password
        @param self The object 
        @param password String containing the password to hash
        @return The SHA512 hash string of a given password string
        """
        sha512 = hashlib.sha512()
        sha512.update(password)
        return sha512.hexdigest()

