# Unit Test Accuracy

A tool for assessing students' unit tests by running their tests against all other students' solutions. Created by [Kevin Buffardi](https://github.com/kbuffardi), [Pedro Valdivia](https://github.com/pvaldivia), [Juan Aguirre-Ayala](https://github.com/jaguirreayala), and [Destiny Rogers](https://github.com/drogers14) as described in the following research publications:

[Unit Test Smells and Accuracy of Software Engineering Student Test Suites](https://doi.org/10.1145/3430665.3456328)
```
Kevin Buffardi and Juan Aguirre-Ayala. 2021. Unit Test Smells and Accuracy of Software Engineering Student Test Suites. In Proceedings of Innovation and Technology in
Computer Science Education (ITiCSE '21). Association for Computing Machinery, New York, NY, USA. DOI:https://doi.org/10.1145/3430665.3456328
```

[Measuring Unit Test Accuracy](https://doi.org/10.1145/3287324.3287351)
```
Kevin Buffardi, Pedro Valdivia, and Destiny Rogers. 2019. Measuring Unit Test Accuracy. In Proceedings of the 50th ACM Technical Symposium on Computer Science Education (SIGCSE '19). Association for Computing Machinery, New York, NY, USA, 578–584. DOI:https://doi.org/10.1145/3287324.3287351
```



## Requirements

To run this application, the following dependencies are required:
* [Docker](www.docker.com)

## Getting Started

First, build the docker image with the command:

```
docker build . -t pairwise-tester
```

After successful build, run the container:

```
docker run \
--mount type=bind,source="$(pwd)",target=/read-src,readonly \
--mount type=bind,source="$(pwd)/output",destination=/output \
-it pairwise-tester
```

Within the container, `/read-src` will have a synchronized, read-only reference to the host's repo and `/output` is a writable directory for data persistence (written to this repo's `/output` subdirectory) even after terminating a container.

## File Structure

`/read-src` is a *read only* mount of this repository. It is linked to the directory on the host so that script editing can be done on the host machine and then within the container, the edited files can be copied into their appropriate locations in the ephemeral environment.

`/output` is bound to the repository's `output` subdirectory with both *read and write* permissions. This directory is meant to hold data output from the scripts so it can persist after the container terminates. In other words, it allows data from the container to be stored on the host.

`/data` contains a copy of all files and subdirectories in the repository's `quiz-data` directory. The copy has write permissions but it is ephemeral.

`/usr/src/pairwise-tester` is the working directory, where the python scripts are copied and stored. This is where the scripts should be executed. It is also referenced by the environmental variable `WORKDIR`.


## All Function Pairs Analysis

### Step 1: Function-under-test (FUT) and Coverage (COV) Analysis

To analyze each unit test for its FUT and each test suite for its coverage, invoke the following scripts from the working directory and specify the directory containing students' subdirectories (e.g. `/data`) and the path that contains the reference Makefile that will be copied into each student subdirectory (e.g. `/data/quizReference`):

```
python run_fut.py /data
python run_cov_fut.py /data /data/quizReferences
```

This generates files `fut_results` and `cov_fut_results` in the working directory.

### Step 2: All Pairs analysis

To run the all pairs testing analysis, invoke the `tests.bash` script:

```
source /data/tests.bash
```

**WARNING!** this process takes a very long time when there is more than just a few students. It grows exponentially with each additional student and may take hours to complete. It creates a `results.txt` file in the same directory, which summarizes each pairwise test result.

### Step 3: All Pairs spreadsheet

To convert the all pairs results into comma-separated format (CSV) spreadsheet, invoke the following script from the working directory and specify the location of the `results.txt` file:

```
python csvbytestcase.py /data/results.txt
```

When successful, this produces a CSV file of the same name (e.g. `results.txt.csv`).


### Step 4: Aggregate analyses

Gather all the analyses into a spreadsheet with the following command, given the *output files* from steps 2 and 3 as the three arguments:

```
python meta-fut.py results.txt.csv fut_results cov_fut_results
```

This generates a file `results.txt.csv.accuracy.csv` (by appending `.accuracy.csv`) to the file name of the script's first argument. The spreadsheet summarizes results according to the FUT for each student.