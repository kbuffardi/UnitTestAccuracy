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
#  return "Reference-Fall2017"

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
  file = pwd+"/"+name
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
###############################################################################
# PROCEDURES

if len(sys.argv) != 3:
  stdout("Usage:\n python meta.py <results.csv> <groups.csv>")
  sys.exit()

results = sys.argv[1]
groups = sys.argv[2]

# Read groups from CSV and store in grouping
try:
  with open(groups, 'rU') as infile:
    stdout("Loading "+ groups + " for participant grouping...")
    content = infile.read().replace('\r\n', '\n').replace('\r', '\n')
    lines = content.split('\n')
    infile.close()
  stdout("..Read "+str(len(lines))+" lines.")
  grouping = {}
  for row in lines:
    part = row.split(',')
    grouping[part[0]]=part[1]
  del grouping['id'] # get rid of header row entry

except IOError as e:
  print "Couldn't open " + groups

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
  all_functions = []
  for i, line in enumerate(lines):
    if i == 0:
      header=line.split(',')
    else:
      values = line.split(',')
      for j, val in enumerate(values):
        if j == 0:
          tester = val
          if tester not in dataframe:
            dataframe[tester] = {}
        elif j == 1:
          test = val
        elif j == 2:
          function = val
        else:
          result = val
          solution = header[j]
          if solution not in dataframe[tester]:
            dataframe[tester][solution] = {}
          if function not in dataframe[tester][solution]:
            dataframe[tester][solution][function] = {}
          if function != 'constructor' and function not in all_functions:
            all_functions.append(function)
          dataframe[tester][solution][function][test] = result
  stdout("..Dataframe built.")
  # Analyze whether function implementations are correct or incorrect
  correctness = {}
  stdout("Tester: "+tester+" Solution: "+solution)
  for func in dataframe[tester][solution]:
    if func != 'constructor':
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
  with newCSVFile("accuracy") as output:
    accuracy_file = output.name
    sorted_solutions = dataframe[REF()].keys()
    sorted_solutions.sort()
    output.write("id,function,true_positives,true_negatives,false_positives," \
                 +"false_negatives,sensitivity,specificity,accuracy\n")
    for tester in dataframe:
      all_tp = 0
      all_tn = 0
      all_fp = 0
      all_fn = 0
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
          sensitivity = Decimal(tp)/(tp+fn)
        else:
          sensitivity = 0
        if negatives > 0:
          specificity = Decimal(tn)/(tn+fp)
        else:
          specificity = 0
        accuracy = Decimal(tp+tn)/(tp+fp+tn+fn)
        output.write(tester+","+function+","+str(tp)+","+str(tn)+","+str(fp) \
                     +","+str(fn)+","+str(sensitivity)+","+str(specificity) \
                     +","+str(accuracy)+"\n")
        
        all_fn += fn
        all_tp += tp
        all_tn += tn
        all_fp += fp
      # tally outcomes of ALL functions together for the student
      positives = all_tp + all_fp
      negatives = all_tn + all_fn
      if positives > 0:
        sensitivity = Decimal(all_tp)/(all_tp+all_fn)
      else:
        sensitivity = 0
      if negatives > 0:
        specificity = Decimal(all_tn)/(all_tn+all_fp)
      else:
        specificity = 0
      accuracy = Decimal(all_tp+all_tn)/(all_tp+all_fp+all_tn+all_fn)

      output.write(tester+","+TOTAL()+","+str(all_tp)+","+str(all_tn)+"," \
                   +str(all_fp)+","+str(all_fn)+","+str(sensitivity)+"," \
                   +str(specificity)+","+str(accuracy)+"\n")
    output.close()

except IOError as e:
  print "Couldn't open " + results

# Edit accuracy csv file to 
try:
  with open(accuracy_file, 'r') as infile:
    stdout("Adding implementation data to "+ accuracy_file + "...")

    #load file contents into dictionary [row][col] dataframe
    lines = infile.read().replace('\r\n', '\n').replace('\r', '\n').split('\n')
    infile.close()
    accuracy_data = {}
    for index, line in enumerate(lines):
      if index == 0:
        header_col = line.split(',')
      elif len(line)>0:
        cells = line.split(',')
        line_id = cells[0]
        line_function = cells[1]
        if line_id not in accuracy_data:
          accuracy_data[line_id] = {}
        accuracy_data[line_id][line_function] = cells[2:]
    with newCSVFile("summary") as outfile:
      header_str = ','.join(str(col) for col in header_col)
      outfile.write(header_str+",confederate,implementation\n")
      for curr_id in accuracy_data:
        id_pass = 0
        id_fail = 0
        for curr_func in sorted(accuracy_data[curr_id]):
          implementation=0
          is_confederate = (curr_id in grouping and grouping[curr_id] == curr_func)
          func_pass = 0
          func_fail = 0
          if curr_func == TOTAL():
            implementation = Decimal(id_pass)/(id_pass+id_fail)
          else:
            for curr_test in dataframe[REF()][curr_id][curr_func]:
              if dataframe[REF()][curr_id][curr_func][curr_test] == FAILED():
                func_fail += 1
                if not is_confederate:
                  id_fail += 1
              elif dataframe[REF()][curr_id][curr_func][curr_test] == PASSED():
                func_pass += 1
                if not is_confederate:
                  id_pass += 1
            implementation = Decimal(func_pass)/(func_pass+func_fail)
          acc_str = ','.join(str(a) for a in accuracy_data[curr_id][curr_func])
          outfile.write(curr_id+","+curr_func \
                        +","+acc_str \
                        +","+str(is_confederate) \
                        +","+str(implementation) \
                        +"\n")
      outfile.close()

except IOError as e:
  print "Couldn't open " + accuracy_file + " because " + str(e)

try:
  with newCSVFile("confederates") as outfile:
    trick = []
    outfile.write("confederate_id,confederate_function,specificity\n")
    # looking through existing dataframe[tester][solution][function][test]
    for solution in dataframe[REF()]:
      if solution != REF():
        for conf in dataframe[REF()][solution]:
          fp = 0
          tn = 0
          for tester in dataframe:
            if conf == grouping[solution] \
               and solution in correctness[conf]["negative"] \
               and tester != REF() \
               and tester != solution:
              if FAILED() in dataframe[tester][solution][conf].values():
                tn += 1
              else:
                fp += 1
          if conf == grouping[solution] \
             and solution in correctness[conf]["negative"]:
            specificity = Decimal(tn)/(tn+fp)
            outfile.write(solution+","+conf+","+str(specificity)+"\n")
    outfile.close()

except IOError as e:
  print "Couldn't write " + outfile.name + " because " + str(e)
