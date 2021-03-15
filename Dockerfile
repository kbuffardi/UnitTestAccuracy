FROM ubuntu:bionic
MAINTAINER Kevin Buffardi (kbuffardi@csuchico.edu)
LABEL title="Pairwise Tester"
LABEL version=0.3
WORKDIR /usr/src/pairwise-tester
ENV GTEST_REPO=/googletest
ENV GTEST_DIR=${GTEST_REPO}/googletest
ENV DATA_DIR=/data/
ENV DEBIAN_FRONTEND=noninteractive
ENV WORKDIR=/usr/src/pairwise-tester

# Gather ephemeral copies of data and application
COPY quiz-data/ ${DATA_DIR}
COPY *.py ./

# Install dependencies
RUN apt-get update &&  \
    apt-get install -y \
            python \
            python3.8 \
            build-essential \
            g++ \
            cmake \
            git-all \
            dos2unix \
            pmccabe

# Setup GoogleTest and return to working directory
RUN git clone https://github.com/google/googletest ${GTEST_REPO} && \
    mkdir ${GTEST_REPO}/build && \
    cd ${GTEST_REPO}/build && \
    cmake ${GTEST_REPO} && \
    make && \
    make install && \
    cd ${WORKDIR}
