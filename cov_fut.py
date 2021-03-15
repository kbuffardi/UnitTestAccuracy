# cov_fut.py
#		Python script that goes through a student's test coverage
#		of each of their implementations.
#		Purpose is to analyze what function is being tested for
#		a single test.
#
#		Tested with python3

import re
import sys
from decimal import *

# findnth
# Looks for the nth time a pattern is found in a string
#
# param string - A string used to iterate
# param pattern - A string pattern that identifies what to look for
# param n - A integer that tells how many times to iterate
def findnth(string, pattern, n):
    parts= string.split(pattern, n+1)
    if len(parts)<=n+1:
        return -1
    return len(string)-len(parts[-1])-len(pattern)


# Make sure there are only two command line arguments #
if len(sys.argv) != 2:
	sys.exit("Usage: fut testfile")

# Try to open file command line argument #
# If we can open the file then we output an error and exit
try:
	my_ifile = open(sys.argv[1],"r")
except IOError:
	sys.exit("Error: could not open file")



# List of variables used throughout the program
num_statements = 0
num_statements_cov = 0
start_of_test = False
end_of_test = False
overall_num_statements = 0
overall_cov_statements = 0


# While we don't reach the end of the file, read each line #
for cur_line in my_ifile:
		# remove all <space> characters within the string cur_line
		cur_line = cur_line.replace(" ","")
		# Look for the beginning of an implementation
		if cur_line.find("Piezas::") >= 0:
			# Are we currently in a test
			if start_of_test:
				# make sure we dont divide by zero
				# List all coverage stats for each implementation
				if num_statements > 0:
					coverage = (Decimal(num_statements_cov)/num_statements)*100
					print "# of statements: " + str(num_statements)
					print "# of covered statements: "+ str(num_statements_cov)
					print "Total coverage: " + str(coverage) + " %"
					print ""
				else:
					print "# of statements: " + str(num_statements)
					print "# of covered statements: " + str(num_statements_cov)
					print "Total coverage: 0 %"
					print ""
			# Reset all variables for next implementation
			start_of_test = True
			end_of_test = True
			num_statements = 0
			num_statements_cov = 0
			function = ""
			string_index = findnth(cur_line,":",2)
			string = cur_line[string_index+2:cur_line.find("(")]
			print "Function Name: " + string

		# Are we currently in a test
		if start_of_test:
			# Is the current line a statement that was covered
			if cur_line[0].isdigit():
				num_statements_cov += 1
				num_statements += 1
				overall_num_statements += 1
				overall_cov_statements += 1
			# Is the current line a statement that was not covered
			if cur_line[0] == "#":
				num_statements += 1
				overall_num_statements += 1

# make sure we dont divide by zero
# List all coverage stats for each implementation
if num_statements > 0:
	coverage = (Decimal(num_statements_cov)/num_statements)*100
	print "# of statements: " + str(num_statements)
	print "# of covered statements: " + str(num_statements_cov)
	print "Total coverage: " + str(coverage) + " %"
	print ""
else:
	print "# of statements: " + str(num_statements)
	print "# of covered statements: " + str(num_statements_cov)
	print "Total coverage: 0 %"
	print ""

overall_coverage = (Decimal(overall_cov_statements)/overall_num_statements*100)
print "Overall"
print "# of statements: " + str(overall_num_statements)
print "# of covered statements: " + str(overall_cov_statements)
print "Total coverage: " + str(overall_coverage) + " %"
