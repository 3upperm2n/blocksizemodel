#!/bin/bash

nvprof --metrics all --csv ./mm4     2> bs16.csv
nvprof --metrics all --csv ./mm8     2> bs64.csv
nvprof --metrics all --csv ./mm16    2> bs256.csv
nvprof --metrics all --csv ./mm32    2> bs1024.csv
