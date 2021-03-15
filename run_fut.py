# run_fut.py
#		Python script that applies fut.py to all
#		students
#

import os
import sys

#
#	Make sure there are only two command line arguments
if len(sys.argv) != 2:
	sys.exit("Usage: python run_fut.py path/to/directoy/holding/student/directories")
#
#	Shows that path we are trying to walk/traverse through
walk_dir = sys.argv[1]

print("walk_dir =",walk_dir)
print("walk_dir(abs) = ",os.path.abspath(walk_dir))
print("")
walk_dir_abs=os.path.abspath(walk_dir)

#	A for loop that recursively traverses through all subdirectories
#	and files starting at the given root in command line argument
#	Root must be directory that contains all student subdirectories
for root, subdir, files in os.walk(walk_dir_abs):
	#	For loop that loops over all subdirectories
	#	of the students
	for i in range(len(subdir)):
		if root == walk_dir_abs:
			path = walk_dir_abs + "/" + subdir[i] + "/PiezasTest.cpp"
			os.system("touch fut_results")
			command = "echo " + path + " >> fut_results"
			os.system(command)
			if os.path.isfile(path):
				command = "python fut.py " + path + " >> fut_results"
				os.system(command)
			command = "echo \"----------------------------------------------------------------------\" >> fut_results"
			os.system(command)

os.system("touch /output/fut_results")
os.system("cp fut_results /output/fut_results")