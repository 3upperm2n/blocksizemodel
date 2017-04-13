#!/bin/bash

cd bs128 && make && nvprof --metrics all --csv ./BlackScholes 2> bs128.csv && mv bs128.csv ../  && cd ../
cd bs64 && make && nvprof --metrics all --csv ./BlackScholes 2> bs64.csv && mv bs64.csv ../  && cd ../
cd bs32 && make && nvprof --metrics all --csv ./BlackScholes 2> bs32.csv && mv bs32.csv ../  && cd ../
cd bs16 && make && nvprof --metrics all --csv ./BlackScholes 2> bs16.csv && mv bs16.csv ../  && cd ../
