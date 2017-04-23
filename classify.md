# Methodology
Based on the SASS clocks [git](https://github.com/3upperm2n/gpuBenchmarking), 
we study the SASS trace from cuobjdump (static).

From the profiled metrics using nvprof, we know the instructions per warp and the portion of each data type.


### Demo 1 : **Vector Add**
* **Dump sass from your compiled gpu binary.**
```bash
cuobjdump -sass  -arch=sm_52 ./vectorAdd_bs64 > vectorAdd_bs64.sm52.sass 2>&1
```

* Script to understand the SASS instruction
The script will remove the headers, lines with prediction (such as, "@P0 EXIT;"), empty lines, NOP and EXIT lines.
(vectorAdd_bs64.sm52.sass)
```
$./sassResultGen.sh
```

Only the SASS instructions are saved, as shown below. (vectorAdd_bs64.sm52.sass.result)
```
MOV
S2R
S2R
XMAD.MRG
XMAD
XMAD.PSL.CBCC
ISETP.GE.AND
SHL
SHR
IADD
IADD.X
IADD
LDG.E
IADD.X
LDG.E
IADD
IADD.X
FADD
STG.E
BRA
```

* **Understand static SASS**

According to [microbenchmarks](https://github.com/3upperm2n/gpuBenchmarking), 
we know that,besides IMUL (86 clocks) and IMAD (101 clocks), other interger SASSes are 15 clocks.

SP are all 15 clocks.

Fo DP, DADD, DMUL and DMNMX are 48 clocks,  DFMA is 51 clocks.
