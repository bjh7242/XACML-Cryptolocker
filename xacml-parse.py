#!/usr/bin/env python
"""
Parses an xacml file for permissions to determine whether a user can encrypt or decrypt files, based on their role
"""

import xml.etree.ElementTree
import sys

class xacmlparser:
	def parse_file(self):
		pass
	
	def parse_encrypt(self,root,group):
		"""
			Determines whether a user is authorized to encrypt files
			@root - an xml.etree.ElementTree.parse(xacmlfile).getroot() object
			@group - the name of the group that the user is a member of (from shadow file)
		"""
		eligible = False	# initialize variable to False indicating the user does NOT have sufficient privs to encrypt
		print "User's group is " + group
		for element in root.findall('Rule'):
			# action should be permit if the user is authorized to execute the enc/dec operation
			if element.get('Effect') == "Permit":
				action = True
			else:
				action = False
			ruleId =  element.get('RuleId')
			if ruleId == "Encrypt":
				# Rule -> Target -> Subjects -> Subject -> SubjectMatch -> AttributeValue.text == admin or attacker
				for attr in element.findall('Target/Subjects/Subject/SubjectMatch/AttributeValue'):
					# assigns the value of the user within the 
					if attr.text == "admin" or attr.text == "attacker":
						print group + " is eligible to encrypt"
						eligible = True
			elif ruleId == "Decrypt":
				pass
			else:
				# if someone modified the XACML file and added another rule, throw error and exit
				print "Error: unknown rule ID"
				sys.exit(1)
			#print action
		# return false by default so that the user is not eligible to perform the operation
		if action == True and eligible == True:
			return True
		else:
			return False

def main():
	e = xml.etree.ElementTree.parse('rights.xacml')
	x = xacmlparser()
	root = e.getroot()
	x.parse_encrypt(root,"admin")
	


if __name__ == '__main__':
	sys.exit(main())
