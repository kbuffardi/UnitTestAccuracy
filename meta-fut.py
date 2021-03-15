#! /usr/bin/python
###############################################################################
# GETTING STARTED
###############################################################################
# PSEUDO-CONSTANTS
# should the script be quiet (no standard output, only file out)
def QUIET():
  return False

def REF():
  return "quizReferences"

def TOTAL():
  return "xTOTAL"

def FALSE_POSITIVE():
  return "FP"

def FALSE_NEGATIVE():
  return "FN"

def TRUE_POSITIVE():
  return "TP"

def TRUE_NEGATIVE():
  return "TN"

def FAILED():
  return '[  FAILED  ]'

def PASSED():
  return '[  PASSED  ]'
###############################################################################
# DEPENDENCIES
import re
import os
import sys
from decimal import *
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

# prints the provided message to standard out as long as the
# QUIET value is not true
def stdout(message):
  if not QUIET():
    print(message)

# finds the id of the tester from the testing file,
# ex. quiz-data/fa2017430-028/PiezasTest.cpp returns fa2017430-028
def getTester(source):
  match = re.findall(r'\/\S+\/\S+\.cpp',source, re.S)[0]
  return re.sub(r'^.*/','',re.sub(r'/\w+\.cpp','',match, 1))

# finds the id of the tester from the testing file,
# ex. quiz-data/fa2017430-028 returns fa2017430-028
def getTesterFolder(source):
  match = re.findall(r'\/\S+',source, re.S)
  return re.sub(r'^.*/','',match[0], 1)

def splitCoverageForFunctions(source):
  match= re.findall(r'Function Name: \S+\n# of statements: \d+\n# of covered statements: \d+\nTotal coverage: [0-9]+\.?[\.0-9]+' \
                    ,source, re.S)
  return match

def getCoverageForOverall(source):
  match= re.findall(r'Overall\n# of statements: \d+\n# of covered statements: \d+\nTotal coverage: [0-9]+\.?[\.0-9]*',source, re.S)
  if match:
    return Decimal(re.split(r'Total coverage: ',match[0])[-1])
  else:
    return None

# builds an array by tester and removes last after splitting by horizontal bar
def splitByTesters(source):
  return re.split(r'-{70}',source)[:-1]

def splitByTestCase(source):
  return re.split(r'\*{32}',source)[:-1]

def getFUT(source):
  calls = re.findall(r'Function = \w+',source, re.S)
  if len(calls) == 0:
    return ""
  else:
    #return name of last function called
    return re.split(r'= ',calls[-1])[-1]

def getUniqueFunctions(source):
  line = re.findall(r'Number of unique functions: .+',source)
  if line:
    return int(re.split(": ",line[0])[-1])
  else:
    return 0

def getAssertions(source):
  assertions = re.findall(r'Number of ASSERT: .+',source)
  if assertions:
    assertions = re.split(r': ',assertions[0])[-1]
  else:
    assertions = 0

  expectations = re.findall(r'Number of EXPECT: .+',source)
  if expectations:
    expectations = re.split(r': ',expectations[0])[-1]
  else:
    expectations = 0
  return int(assertions) + int(expectations)

def getFunctionCalls(source):
  line = re.findall(r'Total number of functions: .+',source)
  if line:
    return int(re.split(r': ',line[0])[-1])
  else:
    return 0

def getTestName(source):
  line = re.findall(r'Test Name: \S+',source)
  if line:
    return re.split(r': ',line[0])[-1]
  else:
    return 0

def getFunctionName(source):
  line = re.findall(r'Function Name: \S+',source)
  if line:
    return re.split(r': ',line[0])[-1]
  else:
    return 0

def getCoverage(source):
  line = re.findall(r'Total coverage: [0-9]+\.?[\.0-9]+',source)
  if line:
    return Decimal(re.split(r': ',line[0])[-1])
  else:
    return None

###############################################################################
# PROCEDURES

if len(sys.argv) != 4:
  stdout("Usage:\n python meta-fut.py <results.csv> <fut.txt> <coverage.txt>")
  sys.exit()

results = sys.argv[1]
fut_output = sys.argv[2]
cov_file = sys.argv[3]
fut_data = {}
fut_id = {}
# Read function under dddtest analysis from text
try:
  with open(fut_output, 'rU') as infile:
    stdout("Loading "+ fut_output + " for function under test analysis...")
    content = infile.read().replace('\r\n', '\n').replace('\r', '\n')
    infile.close()
  stdout("..Read "+str(len(content))+" lines.")
  fut_results=splitByTesters(content)
  stdout("..Found "+str(len(fut_results))+" testers")

  for i, tester in enumerate(fut_results):
      testername = getTester(tester)
      fut_data[testername] = {}
      fut_id[testername] = {}
      cases = splitByTestCase(tester)
      for case in cases:
        fut = getFUT(case)
        unique = getUniqueFunctions(case)
        assertions = getAssertions(case)
        calls = getFunctionCalls(case)
        testname = getTestName(case)
        fut_id[testername][testname] = fut
        if fut not in fut_data[testername]:
          fut_data[testername][fut] = {"cases": 1,
                                       "unique": unique,
                                       "assertions": assertions,
                                       "calls": calls,
                                       "coverage": 0}
        else:
          fut_data[testername][fut] = {"cases":
                                       fut_data[testername][fut]["cases"]+1,
                                       "unique":
                                       fut_data[testername][fut]["unique"]
                                       + unique,
                                       "assertions":
                                       fut_data[testername][fut]["assertions"]
                                       + assertions,
                                       "calls":
                                       fut_data[testername][fut]["calls"]
                                       + calls,
                                       "coverage": 0}

except IOError as e:
  print "Couldn't open " + fut_output

# Get raw coverage results and add to fut_data
try:
  with open(cov_file, 'rU') as infile:
    stdout("Processing " + cov_file + "...")
    cov_raw =infile.read().replace('\r\n', 'n').replace('\r', '\n')
    testers = splitByTesters(cov_raw)
    infile.close()
  for coverage_output in testers:
    cov_tester = getTesterFolder(coverage_output)
    functions = splitCoverageForFunctions(coverage_output)
    for function in functions:
      function_name = getFunctionName(function)
      if cov_tester in fut_data and function_name in fut_data[cov_tester]:
        cov = getCoverage(function)
        if cov:
          cov = Decimal(cov)/100
        fut_data[cov_tester][function_name]["coverage"] = cov
    if fut_data[cov_tester]:
      fut_data[cov_tester][TOTAL()] = {}
      cov = getCoverageForOverall(coverage_output)
      if cov:
        cov = Decimal(cov)/100
      fut_data[cov_tester][TOTAL()]["coverage"] = cov
    else:
        stdout("WARNING "+cov_tester +"is not in: "+','.join(fut_data))

except IOError as e:
  print "Couldn't open " + cov_file

# Convert raw results to categorize by functions
try:
  with open(results, 'rU') as infile:
    stdout("Processing "+ results + "...")
    content = infile.read().replace('\r\n', '\n').replace('\r', '\n')
    lines = content.split('\n')
    infile.close()
  stdout("..Read "+str(len(lines))+" lines.")
  dataframe = {}
  tester = ''
  test = ''
  function = ''
  result = ''
  solution = ''
  header = []
  lines = filter(None, lines) #get rid of empty lines
  all_functions = []
  for i, line in enumerate(lines):
    if i == 0:
      header=line.split(',')
    else:
      values = line.split(',')
      for j, val in enumerate(values):
        if header[j] == "id":
          tester = val
          function = ''
          if tester not in dataframe:
            dataframe[tester] = {}
        elif header[j] == "test_name":
          test = val
        else:
          result = val
          solution = header[j]
          if test in fut_id[tester]:
            function = fut_id[tester][test]
          if solution not in dataframe[tester]:
            dataframe[tester][solution] = {}
          if function not in dataframe[tester][solution]:
            dataframe[tester][solution][function] = {}
          if function and function != 'constructor' and \
             function not in all_functions:
            all_functions.append(function)
            stdout("Added "+function)
          if '' not in [tester, solution, function, test]:
            dataframe[tester][solution][function][test] = result
  stdout("..Dataframe built.")
  # Analyze whether function implementations are correct or incorrect
  correctness = {}
  for func in dataframe[tester][solution]:
    if func and func != 'constructor':
      stdout("Collecting results for "+func+" correctness")
      correctness[func] = { "positive":[], "negative":[] }
      for student in dataframe[REF()]:
        pass_all = True
        if FAILED() in dataframe[REF()][student][func].values():
          pass_all = False
        if pass_all:
          correctness[func]["positive"].append(student)
        else:
          correctness[func]["negative"].append(student)
      stdout("  ...found "+str(len(correctness[func]["positive"]))+"+, "
             +str(len(correctness[func]["negative"]))+"-")

  # Identify False/True Positives and Negatives
  for tester in dataframe:
    for solution in dataframe[tester]:

      ############## TO REMOVE other functions not needing to be tested #######
      if 'print' in all_functions:
        all_functions.remove('print')
      if 'reset' in all_functions:
        all_functions.remove('reset')
      if 'toggleTurn' in all_functions:
        all_functions.remove('toggleTurn')
      if 'placePiece' in all_functions:
        all_functions.remove('placePiece')
      if 'switchTurn' in all_functions:
        all_functions.remove('switchTurn')
      if 'what' in all_functions:
        all_functions.remove('what')
      #########################################################################
      for function in all_functions:
        if function not in dataframe[tester][solution]:
          if solution in correctness[function]["positive"]:
            dataframe[tester][solution][function] = {"outcome":TRUE_POSITIVE()}
          else:
            dataframe[tester][solution][function] = {"outcome":FALSE_POSITIVE()}
        else:
          if solution in correctness[function]["positive"]:
            if FAILED() in dataframe[tester][solution][function].values():
              dataframe[tester][solution][function]["outcome"] = FALSE_NEGATIVE()
            else:
              dataframe[tester][solution][function]["outcome"] = TRUE_POSITIVE()
          else:
            if FAILED() in dataframe[tester][solution][function].values():
              dataframe[tester][solution][function]["outcome"] = TRUE_NEGATIVE()
            else:
              dataframe[tester][solution][function]["outcome"] = FALSE_POSITIVE()

  # Summarize test accuracy
  with newCSVFile(results+".accuracy") as output:
    accuracy_file = output.name
    sorted_solutions = dataframe[REF()].keys()
    sorted_solutions.sort()
    output.write("id,function_under_test,true_positives,true_negatives,false_positives," \
                 +"false_negatives,positive_verification_rate,bug_finding_rate,accuracy," \
                 +"ref_tests_passed,ref_tests_failed,fut_cases,fut_unique_functions," \
                 +"fut_assertions,fut_function_calls,coverage\n")
    for tester in dataframe:
      all_tp = 0
      all_tn = 0
      all_fp = 0
      all_fn = 0
      all_ref_pass = 0
      all_ref_fail = 0
      all_cases = 0
      all_unique = 0
      all_assertions = 0
      all_calls = 0
      for function in all_functions:
        fp = 0
        fn = 0
        tp = 0
        tn = 0
        for solution in sorted_solutions:
          outcome = dataframe[tester][solution][function]["outcome"]
          if outcome == TRUE_POSITIVE():
            tp = tp + 1
          elif outcome == TRUE_NEGATIVE():
            tn = tn + 1
          elif outcome == FALSE_POSITIVE():
            fp = fp + 1
          else:
            fn = fn + 1
        positives = tp + fp
        negatives = tn + fn
        if positives > 0:
          positive_verification_rate = Decimal(tp)/(tp+fn)
        else:
          positive_verification_rate = 0
        if negatives > 0:
          bug_finding_rate = Decimal(tn)/(tn+fp)
        else:
          bug_finding_rate = 0
        accuracy = Decimal(tp+tn)/(tp+fp+tn+fn)

        fut_ref_pass = sum(value == PASSED() for value in dataframe[REF()][tester][function].values())
        fut_ref_fail = sum(value == FAILED() for value in dataframe[REF()][tester][function].values())
        all_ref_pass += fut_ref_pass
        all_ref_fail += fut_ref_fail
        if function not in fut_data[tester]:
          cases = 0
          unique = 0
          assertions = 0
          calls = 0
          coverage = None
        else:
          cases = fut_data[tester][function]["cases"]
          unique = fut_data[tester][function]["unique"]
          assertions = fut_data[tester][function]["assertions"]
          calls = fut_data[tester][function]["calls"]
          coverage = fut_data[tester][function]["coverage"]
        all_cases += cases
        all_unique += unique
        all_assertions += assertions
        all_calls += calls

        output.write(tester+","+function+","+str(tp)+","+str(tn)+","+str(fp) \
                     +","+str(fn)+","+str(positive_verification_rate)+","+str(bug_finding_rate) \
                     +","+str(accuracy)+","+str(fut_ref_pass)+","+str(fut_ref_fail)+"," \
                     +str(cases)+","+str(unique)+","+str(assertions)+","+str(calls)+"," \
                     +str(coverage)+"\n")

        all_fn += fn
        all_tp += tp
        all_tn += tn
        all_fp += fp

      # tally outcomes of ALL functions together for the student
      positives = all_tp + all_fp
      negatives = all_tn + all_fn
      if positives > 0:
        positive_verification_rate = Decimal(all_tp)/(all_tp+all_fn)
      else:
        positive_verification_rate = 0
      if negatives > 0:
        bug_finding_rate = Decimal(all_tn)/(all_tn+all_fp)
      else:
        bug_finding_rate = 0
      accuracy = Decimal(all_tp+all_tn)/(all_tp+all_fp+all_tn+all_fn)
      coverage = fut_data[tester][TOTAL()]["coverage"]

      output.write(tester+","+TOTAL()+","+str(all_tp)+","+str(all_tn)+"," \
                   +str(all_fp)+","+str(all_fn)+","+str(positive_verification_rate)+"," \
                   +str(bug_finding_rate)+","+str(accuracy)+","+str(all_ref_pass)+"," \
                   +str(all_ref_fail)+","+str(all_cases)+","+str(all_unique)+"," \
                   +str(all_assertions)+","+str(all_calls)+","+str(coverage)+"\n")
    output.close()

  file = os.path.basename(file)
  os.system("touch /output/" + file)
  os.system("cp " + file + " /output/" + file)

except IOError as e:
  print "Couldn't open " + results
