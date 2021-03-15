#! /usr/bin/python
###############################################################################
# GETTING STARTED
#  This script uses python 2.7. Untested on python 3+
#  Usage:
#   $python csvbytestcase.py <filename.txt>
#  This will create a Comma Separated Value (CSV) spreadsheet of the pairwise
#  testing results. The CSV file is named (and located) as <filename.txt.csv>
#  but will not overwrite files with that name.
###############################################################################
# DEPENDENCIES
import re
import os
import sys

###############################################################################
# PSEUDO-CONSTANTS
# should the script be quiet (no standard output, only file out)
def QUIET():
  return False

def NEW_SOLUTION_LINE():
  return "-------------------------- WORKING WITH "

def NEW_TESTER_LINE():
  return "---------------Testing "

def NEW_TEST_CASE():
  return "TESTING"

def NEW_RESULT_LINE():
  return "(\[|B)"

def NEW_SEPARATOR_LINE():
  return "/"

def NEW_EMPTY_LINE():
  return "\s\B"

###############################################################################
# FUNCTIONS
# newCSVFile(name) - creates a new csv file with a unique name (as provided)
# with an increasing integer suffix if that file already exists
def newCSVFile(name):
  pwd = os.getcwd()
  global file
  file = pwd+"/"+os.path.basename(name)
  suffix = ""
  while os.path.isfile(file+str(suffix)+".csv"):
    if suffix == "":
      suffix = -1
    else:
      suffix = int(suffix)-1
  file = file + str(suffix) + ".csv"
  stdout("Creating file " + file)
  return open(file, "a") #opened file for appending

# stdout(message) - prints the provided message to standard out as long as the
# QUIET value is not true
def stdout(message):
  if not QUIET():
    print message

def next_tester(input):
  #regex = "---------------Testing (?:fa|spr){1}[0-9]{7}-[0-9]{3}"
  regex = "---------------Testing [^\s]+"
  search = re.search(regex,input,re.S).group()
  if search:
    return search.split(' ')[1].rstrip('/')
  else:
    return ""

def next_solution(input):
  #regex = "-------------------------- WORKING WITH (?:fa|spr){1}[0-9]{7}-[0-9]{3}"
  regex = "-------------------------- WORKING WITH [^\s]+"
  search = re.search(regex,input,re.S).group()
  if search:
    return search.split("WORKING WITH ")[1].rstrip('/')
  else:
    return ""

def next_test_case(input):
  regex = "TESTING [^\s]+"
  search = re.search(regex,input,re.S).group()
  if search:
    return search.split(' ')[1]
  else:
    return ""

def next_result(input):
  regex = "(\[  PASSED  \]|\[  FAILED  \]|BuildError)"
  return re.search(regex,input,re.S).group()

###############################################################################
# PROCEDURES

if len(sys.argv) != 2:
  stdout("Usage:\n python csvbytestcase.py <filename.txt>")
  sys.exit()

results = sys.argv[1]

try:
  with open(results, 'r') as infile:
    stdout("Processing "+ results + "...")
    lines = [line.rstrip('\n') for line in infile]
    stdout("Read "+str(len(lines))+" lines.")
    dataframe = {}
    tester = ''
    test = ''
    result = ''
    solution = ''
    for line in lines:
      if re.search('^'+NEW_TESTER_LINE(),line,re.S):
        tester = next_tester(line)
        dataframe[tester] = {}
      elif re.search('^'+NEW_TEST_CASE(),line,re.S):
        test = next_test_case(line)
        if( test not in dataframe[tester] ):
          dataframe[tester][test] = {}
      elif re.search('^'+NEW_SOLUTION_LINE(),line,re.S):
        solution = next_solution(line)
      elif re.search('^'+NEW_RESULT_LINE(),line,re.S):
        result = next_result(line)
        dataframe[tester][test][solution] = result

    # Create CSV summary
    students = dataframe.keys()
    students.sort()

    with newCSVFile(results) as csv:
      # Write header row
      csv.write("id,test_name")
      for current_student in students:
        csv.write(","+current_student)
      csv.write("\n")


      # Write each data row. Very inefficient.
      for tester_k in dataframe:
        for test_k in dataframe[tester_k]:
          csv.write(tester_k+","+test_k)
          for student in students:
            if student in dataframe[tester_k][test_k]:
              csv.write(","+dataframe[tester_k][test_k][student])
            else:
              stdout("Didn't find " + student + " in " + tester_k)
              csv.write(",")
          csv.write("\n")

  file = os.path.basename(file)
  os.system("touch /output/" + file)
  os.system("cp " + file + " /output/" + file)

except IOError as e:
  print "Couldn't open " + results
