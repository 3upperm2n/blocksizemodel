#!/bin/bash

cd bs1024 && make && nvprof --metrics all --csv ./convolutionFFT2D 2> bs1024.csv && mv bs1024.csv ../  && cd ../
cd bs512 && make && nvprof --metrics all --csv ./convolutionFFT2D 2> bs512.csv && mv bs512.csv ../  && cd ../
cd bs256 && make && nvprof --metrics all --csv ./convolutionFFT2D 2> bs256.csv && mv bs256.csv ../  && cd ../
cd bs128 && make && nvprof --metrics all --csv ./convolutionFFT2D 2> bs128.csv && mv bs128.csv ../  && cd ../
cd bs64 && make && nvprof --metrics all --csv ./convolutionFFT2D 2> bs64.csv && mv bs64.csv ../  && cd ../
cd bs32 && make && nvprof --metrics all --csv ./convolutionFFT2D 2> bs32.csv && mv bs32.csv ../  && cd ../
