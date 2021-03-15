# run_cov_fut.py
#		Python script that applies cov_fut.py to all
#		students
#
#		Tested with python
import os
import sys
import shlex
import shutil
from subprocess import Popen, PIPE

#	Make sure there are only two command line arguments
if len(sys.argv) != 3:
	sys.exit("Usage: python run_cov_fut.py path/to/directoy/holding/student/directories path/to/directory/holding/master/Makefile")

#	Shows that path we are trying to walk/traverse through
walk_dir = sys.argv[1]
make_dir = sys.argv[2]
print("walk_dir =",walk_dir)
print("walk_dir(abs) = ",os.path.abspath(walk_dir))
print("make_dir = ",make_dir)
print("make_dir(abs) = ",os.path.abspath(make_dir))
print("")

#	Source Makefile (100% exists)
makefile_source = make_dir + "/Makefile"

#	A for loop that recursively traverses through all subdirectories
#	and files starting at the given root in command line argument
#	Root must be directory that contains all student subdirectories
for root, subdir, files in os.walk(walk_dir):

	#	For loop that loops over all subdirectories
	#	of the students
	for i in range(len(subdir)):

		# Make sure the only root traversed is the command-line argument
		if root == sys.argv[1]:
			# This is the path to each subdirectory
			path = sys.argv[1] + "/" + subdir[i]

			# The following lines are bash commands to run cov_fut.py
			# for all students
			os.system("touch cov_fut_results")
			command = "echo " + path + " >> cov_fut_results"
			os.system(command)

			# Set a destination Makefile and copy over the master Makefile
			# into current student directory
			makefile_destination = path + "/Makefile"
			try:
			 	shutil.copyfile(makefile_source, makefile_destination)
			except shutil.Error:
			 	print("Student Makefile already similar to master Makefile, no worry")
			
			# Make sure to clean the files before trying to make. 
			os.system("make clean")

			# Try to build student files and retrieve the exit status
			# cmd = "make -s -C " + path
			cmd = "make -C " + path
			process = Popen(shlex.split(cmd), stdout=PIPE)
			err = process.communicate()
			exit_code = process.wait()
			# Did the files build correctly
			if exit_code == 0:
				command = path + "/PiezasTest"
				os.system(command)
				command = "cp " + path + "/*.cpp ./"
				os.system(command)
				command = "gcov " + path + "/Piezas.cpp"
				os.system(command)
				command = "python cov_fut.py Piezas.cpp.gcov >> cov_fut_results"
				os.system(command)
				command = "rm *.cpp *.gcov"
				os.system(command)
				command = "make clean -s -C " + path
				os.system(command)
			else:
				command = "echo \"Make error\": " + str(err[0]) + "Output: " + str(err[1]) + " >> cov_fut_results"
				os.system(command)
			command = "echo \"----------------------------------------------------------------------\" >> cov_fut_results"
			os.system(command)

os.system("touch /output/cov_fut_results")
os.system("cp cov_fut_results /output/cov_fut_results")
