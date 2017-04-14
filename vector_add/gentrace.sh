#!/bin/bash

nvprof --print-gpu-trace --csv ./vectorAdd_bs32  2> trace32.csv
nvprof --metrics all --csv ./vectorAdd_bs32  2> metrics32.csv

nvprof --print-gpu-trace --csv ./vectorAdd_bs64  2> trace64.csv
nvprof --metrics all --csv ./vectorAdd_bs64  2> metrics64.csv

nvprof --print-gpu-trace --csv ./vectorAdd_bs128  2> trace128.csv
nvprof --metrics all --csv ./vectorAdd_bs128  2> metrics128.csv

nvprof --print-gpu-trace --csv ./vectorAdd_bs256  2> trace256.csv
nvprof --metrics all --csv ./vectorAdd_bs256  2> metrics256.csv

nvprof --print-gpu-trace --csv ./vectorAdd_bs512 2> trace512.csv
nvprof --metrics all --csv ./vectorAdd_bs512 2> metrics512.csv

nvprof --print-gpu-trace --csv ./vectorAdd_bs1024 2> trace1024.csv
nvprof --metrics all --csv ./vectorAdd_bs1024 2> metrics1024.csv
