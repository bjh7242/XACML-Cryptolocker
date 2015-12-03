#!/usr/bin/env python
"""
Parses an xacml file for permissions to determine whether a user can encrypt or decrypt files, based on their role
"""

import xml.etree.ElementTree
import sys

class xacmlparser:
    
    def parse_action(self,root,group,action):
        """
        Determines whether a user is authorized to encrypt files
        @param root an xml.etree.ElementTree.parse(xacmlfile).getroot() object
        @param group the name of the group that the user is a member of (from shadow file)
        @param action the action to perform (must be Encrypt/Decrypt, case sensitive)
        @return True if the user is authorized to perform action, False if not
        """
        enc_groups = ['admin','attacker']    # groups that are allowed to encrypt files
        dec_groups = ['admin','user']        # groups that are allowed to decrypt files

        eligible = False    # initialize variable to False indicating the user does NOT have sufficient privs to execute action

        for element in root.findall('Rule'):
            # effect should be permit if the user is authorized to execute the enc/dec operation
            if element.get('Effect') == "Permit":
                authorized = True
            else:
                authorized = False

            # get RuleId attribute (will be either Encrypt or Decrypt)
            # we might need a for loop and a findall to get the rule ID, this might be an issue with decrypt (since it is second)
            ruleId =  element.get('RuleId')
            
            if ruleId == "Encrypt" and action == "Encrypt":
                #print "RuleId and action are both ENCRYPT"
                # Rule -> Target -> Subjects -> Subject -> SubjectMatch -> AttributeValue.text == admin or attacker
                # findall supports XPath syntax
                for attr in element.findall('Target/Subjects/Subject/SubjectMatch/AttributeValue'):
                    # assigns the value of the user within the 
                    if group in enc_groups and group == attr.text:
                        #print group + " is eligible to encrypt"
                        # user is eligible to perform the requested encryption operation
                        eligible = True
                        if authorized == True and eligible == True:
                            return True
            elif ruleId == "Decrypt" and action == "Decrypt":
                #print "RuleId and action are both DECRYPT"
                # Rule -> Target -> Subjects -> Subject -> SubjectMatch -> AttributeValue.text == admin or attacker
                # findall supports XPath syntax
                for attr in element.findall('Target/Subjects/Subject/SubjectMatch/AttributeValue'):
                    # assigns the value of the user within the 
                    if group in dec_groups and group == attr.text:
                        #print group + " is eligible to decrypt"
                        # user is eligible to perform the requested decryption operation
                        eligible = True
                        if authorized == True and eligible == True:
                            return True
            else:
                # if the ruleId and action do not match, pass
                pass

        # return false by default so that the user is not eligible to perform the operation
        #print "User in group " + group + " is not eligible to " + action
        return False

