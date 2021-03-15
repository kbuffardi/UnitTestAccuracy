# Building GoogleTest and running exercise-gtest unit tests against
# This Makefile is based on the sample Makefile provided in the
# official GoogleTest GitHub Repo v1.7

# GTEST_DIR = /usr/local/src/googletest/googletest

# Flags passed to the preprocessor and compiler
CPPFLAGS += --coverage -isystem $(GTEST_DIR)/include
CXXFLAGS += -g -Wall -Wextra -pthread -fno-stack-protector

# All tests produced by this Makefile.
TESTS = PiezasTest

# All Google Test headers. Adjust only if you moved the subdirectory
GTEST_HEADERS = $(GTEST_DIR)/include/gtest/*.h \
                $(GTEST_DIR)/include/gtest/internal/*.h

# House-keeping build targets.

all : $(TESTS)

clean :
	rm -f $(TESTS) gtest.a gtest_main.a *.o *.gcov *.gcda *.gcno *.gch

test:
	./PiezasTest
	gcov -fbc Piezas.cpp

# Builds gtest.a and gtest_main.a.
GTEST_SRCS_ = $(GTEST_DIR)/src/*.cc $(GTEST_DIR)/src/*.h $(GTEST_HEADERS)

gtest-all.o : $(GTEST_SRCS_)
	$(CXX) $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c \
            $(GTEST_DIR)/src/gtest-all.cc

gtest_main.o : $(GTEST_SRCS_)
	$(CXX) $(CPPFLAGS) -I$(GTEST_DIR) $(CXXFLAGS) -c \
            $(GTEST_DIR)/src/gtest_main.cc

gtest.a : gtest-all.o
	$(AR) $(ARFLAGS) $@ $^

gtest_main.a : gtest-all.o gtest_main.o
	$(AR) $(ARFLAGS) $@ $^

# Builds the Piezas class and associated PiezasTest
Piezas.o : Piezas.h $(GTEST_HEADERS)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c Piezas.cpp

PiezasTest.o : PiezasTest.cpp \
                     Piezas.h $(GTEST_HEADERS)
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -c PiezasTest.cpp

PiezasTest : Piezas.o PiezasTest.o gtest_main.a
	$(CXX) $(CPPFLAGS) $(CXXFLAGS) -lpthread $^ -o $@
