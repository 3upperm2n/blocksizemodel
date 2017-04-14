#!/bin/bash

cd bs1024 && make clean && make 
nvprof --print-gpu-trace --csv ./convolutionFFT2D 2> trace1024.csv
nvprof --metrics all --csv ./convolutionFFT2D 2> metrics1024.csv 
mv *.csv ../  && cd ../

cd bs512 && make clean && make 
nvprof --print-gpu-trace --csv ./convolutionFFT2D 2> trace512.csv
nvprof --metrics all --csv ./convolutionFFT2D 2> metrics512.csv 
mv *.csv ../  && cd ../

cd bs256 && make clean && make 
nvprof --print-gpu-trace --csv ./convolutionFFT2D 2> trace256.csv
nvprof --metrics all --csv ./convolutionFFT2D 2> metrics256.csv 
mv *.csv ../  && cd ../

cd bs128 && make clean && make 
nvprof --print-gpu-trace --csv ./convolutionFFT2D 2> trace128.csv
nvprof --metrics all --csv ./convolutionFFT2D 2> metrics128.csv 
mv *.csv ../  && cd ../

cd bs64 && make clean && make 
nvprof --print-gpu-trace --csv ./convolutionFFT2D 2> trace64.csv
nvprof --metrics all --csv ./convolutionFFT2D 2> metrics64.csv 
mv *.csv ../  && cd ../

cd bs32 && make clean && make 
nvprof --print-gpu-trace --csv ./convolutionFFT2D 2> trace32.csv
nvprof --metrics all --csv ./convolutionFFT2D 2> metrics32.csv 
mv *.csv ../  && cd ../

cd bs16 && make clean && make 
nvprof --print-gpu-trace --csv ./convolutionFFT2D 2> trace16.csv
nvprof --metrics all --csv ./convolutionFFT2D 2> metrics16.csv 
mv *.csv ../  && cd ../
