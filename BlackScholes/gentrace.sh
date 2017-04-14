#!/bin/bash

cd bs128 && make clean && make
nvprof --print-gpu-trace --csv  ./BlackScholes 2> trace128.csv
nvprof --metrics all --csv 		./BlackScholes 2> metrics128.csv 
mv *.csv ../  && cd ../

cd bs64 && make clean && make
nvprof --print-gpu-trace --csv  ./BlackScholes 2> trace64.csv
nvprof --metrics all --csv 		./BlackScholes 2> metrics64.csv 
mv *.csv ../  && cd ../

cd bs32 && make clean && make
nvprof --print-gpu-trace --csv  ./BlackScholes 2> trace32.csv
nvprof --metrics all --csv 		./BlackScholes 2> metrics32.csv 
mv *.csv ../  && cd ../

cd bs16 && make clean && make
nvprof --print-gpu-trace --csv  ./BlackScholes 2> trace16.csv
nvprof --metrics all --csv 		./BlackScholes 2> metrics16.csv 
mv *.csv ../  && cd ../
