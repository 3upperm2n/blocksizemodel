#!/bin/bash

cd ss1024 && make clean && make 
nvprof --print-gpu-trace --csv ./mergeSort 2> trace1024.csv
nvprof --metrics all     --csv ./mergeSort 2> metrics1024.csv 
mv *.csv ../  && cd ../

cd ss512 && make clean && make 
nvprof --print-gpu-trace --csv ./mergeSort 2> trace512.csv
nvprof --metrics all     --csv ./mergeSort 2> metrics512.csv 
mv *.csv ../  && cd ../

cd ss256 && make clean && make 
nvprof --print-gpu-trace --csv ./mergeSort 2> trace256.csv
nvprof --metrics all     --csv ./mergeSort 2> metrics256.csv 
mv *.csv ../  && cd ../

cd ss128 && make clean && make 
nvprof --print-gpu-trace --csv ./mergeSort 2> trace128.csv
nvprof --metrics all     --csv ./mergeSort 2> metrics128.csv 
mv *.csv ../  && cd ../
