#!/bin/bash

nvprof --metrics all --csv ./vectorAdd_bs32  2> bs32.csv
nvprof --metrics all --csv ./vectorAdd_bs64  2> bs64.csv
nvprof --metrics all --csv ./vectorAdd_bs128  2> bs128.csv
nvprof --metrics all --csv ./vectorAdd_bs256  2> bs256.csv
nvprof --metrics all --csv ./vectorAdd_bs512 2> bs512.csv
nvprof --metrics all --csv ./vectorAdd_bs1024 2> bs1024.csv
