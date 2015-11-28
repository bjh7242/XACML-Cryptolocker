#!/usr/bin/env python
"""
Parses an xacml file for permissions to determine whether a user can encrypt or decrypt files, based on their role
"""

import xml.etree.ElementTree
import sys

class xacmlparser:
	def parse_file(self):
		pass
	
	def parse_encrypt(self,xmlobj,group):
		print "User's group is " + group
		#for tag in 

def main():
	e = xml.etree.ElementTree.parse('rights.xacml')
	root = e.getroot()
	
	for element in root.findall('Rule'):
		# action should be permit if the user is authorized to execute the enc/dec operation
		action = element.get('Effect')
		ruleId =  element.get('RuleId')
		if ruleId == "Encrypt":
			pass
		elif ruleId == "Decrypt":
			pass
		else:
			# if someone modified the XACML file and added another rule, throw error and exit
			print "Error: unknown rule ID"
			sys.exit(1)
		print action


if __name__ == '__main__':
	sys.exit(main())
