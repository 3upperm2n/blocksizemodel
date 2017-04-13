#!/bin/bash

cd ss1024 && make clean && make && nvprof --metrics all --csv ./mergeSort 2> ss1024.csv && mv ss1024.csv ../  && cd ../
cd ss512 && make clean && make && nvprof --metrics all --csv ./mergeSort 2> ss512.csv && mv ss512.csv ../  && cd ../
cd ss256 && make clean && make && nvprof --metrics all --csv ./mergeSort 2> ss256.csv && mv ss256.csv ../  && cd ../
cd ss128 && make clean && make && nvprof --metrics all --csv ./mergeSort 2> ss128.csv && mv ss128.csv ../  && cd ../
