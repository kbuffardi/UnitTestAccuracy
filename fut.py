# fut.py
#		Python script that goes through a student's test file
#		to look for test and statistics pertaining to that test.
#		Purpose is to analyze what function is being tested for 
#		a single test.

import re
import sys

# PrintDifferentFunctions
#		Iterates through a list to identify
#		unique elements in the list
#
#		param functionList: holds a list of functions as strings
#
#		returns the number of elements in the list
def printDifferentFunctions (functionList = []):
	numOfFunctions = 0
	while len(functionList) > 0:
		name = functionList[0]
		numOfFunctions += 1

		i = 0
		count = 0
		while i < len(functionList):
			if name == functionList[i]:
				count += 1
				del functionList[i]
				i = 0
			else:
				i += 1

		print name + " appears: " + str(count)

	return numOfFunctions
#
#
#
#
#
#	Make sure there are only two command line arguments #
if len(sys.argv) != 2:
	sys.exit("Usage: fut testfile")
#
#	Try to open file command line argument #
#	If we can open the file then we output an error and exit
try:
	my_ifile = open(sys.argv[1],"r")
except IOError:
	print "Error: could not open file"
#
#
#	List of variables used throughout the program
function_regx = re.compile("[a-zA-Z0-9]+[\.][a-zA-Z0-9]+[(].*[)]")
endTest_regx = re.compile(".*[}].*")
beginTest_regx = re.compile(".*[{].*")
assert_regx = re.compile("ASSERT*")
expect_regx = re.compile("EXPECT*")
start_of_test = None
single_comment = False
multi_comment = False
firstBrace = False
functionList = []
assertCount = 0
expectCount = 0
braceCount = 0
#
#
#	While we don't reach the end of the file, read each line #
with my_ifile:
	for cur_line in my_ifile:
		#	Try to find a multi-comment in current string
		#	If we find a multi-comment the we set multi-comment to true
		#	Else try to find a single comment and set to true
		cur_line = cur_line.replace(" ","")
		if cur_line.find("/*") == 0:
			multi_comment = True
			single_comment = False
		elif cur_line.find("//") == 0:
			single_comment = True
		#	If we currently are not in a single/multi comment
		#	then try to find all tests and functions
		if single_comment == False and multi_comment == False:
			#	Try to find the beginning of a test
			#	If we find it then set all values needed to
			#	record all stats for a test
			if cur_line.find("TEST(") >= 0:
				start_of_test = True
				braceCount = 1
				firstBrace = True
				function = ""
				listOfFunctions = []
				assertCount = 0
				expectCount = 0
				string = cur_line[cur_line.find(",")+1:cur_line.find(")")]
				print "Test Name: " + string.replace(" ","")

			#	set variables to find our regex patterns
			pattern = function_regx.search(cur_line)
			assertPattern = assert_regx.search(cur_line)
			expectPattern = expect_regx.search(cur_line)
			openBracePattern = beginTest_regx.search(cur_line)
			closeBracePattern = endTest_regx.search(cur_line)
			#	Start if we are current in a test
			if start_of_test:
				#	if we find a the pattern for a function
				#	then add the function to the listOfFunctions list
				if pattern:
					function = pattern.group()
					function = function[function.find(".")+1:function.find("(")]
					print"Function = " + function
					listOfFunctions.append(function)
				#	if we find the assert pattern 
				#	then we increment the assert counter
				if assertPattern:
					assertCount += 1
				#	if we find the expect pattern
				#	then we increment the expect counter
				if expectPattern:
					expectCount += 1
				
				if openBracePattern and firstBrace:
					braceCount = 1
					firstBrace = False
				elif openBracePattern and firstBrace == False:
					braceCount += 1

				if closeBracePattern:
					braceCount -= 1

			#	if we found the end of test pattern & currently in a test 
			#	then we state all functions,asserts,expects,stats for a test
			if braceCount == 0 and start_of_test:
				start_of_test = False
				#
				#	There are no functions
				if function == "":
					print"Function Tested: None"
					print"********************************"
				#
				#	List all stats for a test
				else:
					print ""
					numFunctions = len(listOfFunctions)
					uniqueFunc = printDifferentFunctions(listOfFunctions)
					print "Number of unique functions: " + str(uniqueFunc)
					print "Number of ASSERT: " + str(assertCount)
					print "Number of EXPECT: " + str(expectCount)
					print "Total number of functions: " + str(numFunctions)
					print "********************************" 
		#	If we currently are in a multi-comment and we find the end of it
		#	then set multi-comment to false
		if multi_comment and cur_line.find("*/") >= 0:
			multi_comment = False
		#	
		#	
		single_comment = False	

