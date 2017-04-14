#!/bin/bash

nvprof --print-gpu-trace --csv ./mm4     2> trace16.csv
nvprof --metrics all     --csv ./mm4     2> metrics16.csv

nvprof --print-gpu-trace --csv ./mm8     2> trace64.csv
nvprof --metrics all     --csv ./mm8     2> metrics64.csv

nvprof --print-gpu-trace --csv ./mm16     2> trace256.csv
nvprof --metrics all     --csv ./mm16     2> metrics256.csv

nvprof --print-gpu-trace --csv ./mm32     2> trace1024.csv
nvprof --metrics all     --csv ./mm32     2> metrics1024.csv

