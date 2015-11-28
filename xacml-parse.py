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
			@root - an xml.etree.ElementTree.parse(xacmlfile).getroot() object
			@group - the name of the group that the user is a member of (from shadow file)
			@action - the action to perform (must be Encrypt/Decrypt, case sensitive)
			return - True if the user is authorized to perform action, False if not
		"""
		eligible = False	# initialize variable to False indicating the user does NOT have sufficient privs to execute action
		print "User's group is " + group
		for element in root.findall('Rule'):
			# action should be permit if the user is authorized to execute the enc/dec operation
			if element.get('Effect') == "Permit":
				action = True
			else:
				action = False
			# get RuleId attribute (will be either Encrypt or Decrypt)
			ruleId =  element.get('RuleId')
			if ruleId == "Encrypt" and action == "Encrypt":
				# Rule -> Target -> Subjects -> Subject -> SubjectMatch -> AttributeValue.text == admin or attacker
				# findall supports XPath syntax
				for attr in element.findall('Target/Subjects/Subject/SubjectMatch/AttributeValue'):
					# assigns the value of the user within the 
					if attr.text == "admin" or attr.text == "attacker":
						print group + " is eligible to encrypt"
						eligible = True
			elif ruleId == "Decrypt" and action == "Decrypt":
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
	execute = x.parse_action(root,"admin","Encrypt")
	print "Execute is " + str(execute)
	


if __name__ == '__main__':
	sys.exit(main())
