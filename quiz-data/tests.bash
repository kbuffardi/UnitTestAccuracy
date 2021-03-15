LINE_NUMBER=1;
NUM_FINISHED=0;
rm results.txt &> trash.txt

for dir in */
do
	cd $dir
	echo "WORKING ON STUDENT ----------> $dir"
	make -s &> ../trash.txt
	MAKEFAILED=$?
	if [[ $MAKEFAILED == 0 ]]
	then
		# Creating list of tests from current directory
		echo "" >> ../results.txt
		echo "---------------Testing $dir Against Other Students Solutions-------------" >> ../results.txt
		echo "" >> ../results.txt
		touch tests.txt
		./PiezasTest --gtest_list_tests > tests.txt
		make clean &> ../trash.txt
		sed -i '1,2 d' tests.txt
		sed -r 's/\s+//g' tests.txt > new.txt
		rm tests.txt
		mv new.txt tests.txt
		mv tests.txt ../
		cp PiezasTest.cpp ../
		cd ../

		# Testing Students tests with every other student
		for dirTwo in */
		do
			echo "WORKING WITH $dirTwo"
			echo "///////////////////////////////////////////////////////////////////////////////////" >> results.txt
			echo "-------------------------- WORKING WITH $dirTwo ----------------------------" >> results.txt
			echo "///////////////////////////////////////////////////////////////////////////////////" >> results.txt
			mkdir $dirTwo/temp
			mv $dirTwo/PiezasTest.cpp $dirTwo/temp
			cp PiezasTest.cpp $dirTwo
			cp tests.txt $dirTwo
			cd $dirTwo
			make clean
			make -s &> ../trash.txt
			MAKEFAILED=$?
			while IFS= read -r var
			do
				echo "-----------------------------------------------------------------------------------" >> ../results.txt
				echo  "TESTING $var FROM $dir WITH STUDENT $dirTwo" >> ../results.txt
				if [[ $MAKEFAILED == 0 ]]
				then
					timeout 15 ./PiezasTest --gtest_filter=PiezasTest.$var > ../trash.txt
					TESTPASSED=$?
					if [[ $TESTPASSED == 0 ]]
					then
						echo "[  PASSED  ]" >> ../results.txt
						echo "-----------------------------------------------------------------------------------" >> ../results.txt
					else
						echo "[  FAILED  ]" >> ../results.txt
						echo "-----------------------------------------------------------------------------------" >> ../results.txt
					fi
				else
					echo  "BuildError" >> ../results.txt
				fi
			done < tests.txt
			rm PiezasTest.cpp
			rm tests.txt
			mv temp/PiezasTest.cpp ./
			rmdir temp
			make clean &> ../trash.txt
			cd ../
		done
		rm tests.txt
		rm trash.txt
		rm PiezasTest.cpp
	else
		make clean &> ../trash.txt
		cd ../
	fi
done

# Simple way of just copying results.txt into the output folder
# maybe better way to do this?
touch /output/results.txt
cp results.txt /output/results.txt
