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

According to [microbenchmarks](https://github.com/3upperm2n/gpuBenchmarking), we know that,

For integer SASS, besides IMUL (86 clocks) and IMAD (101 clocks), others are 15 clocks.

SP are all 15 clocks.

Fo DP, DADD, DMUL and DMNMX are 48 clocks,  DFMA is 51 clocks.

* **Understand the dynamic SASS**

We extract info from profile metrics for the application. 
```
instruction per warp
integer instrucitons numbers
fp 32 instruction numbers
fp 64 instruction numbers
ld st instruction numbers
```

Here is a list of trace.
```
Total running threads : 50016.0

thread_fp_32: 0.999680102367
thread_fp_64: 0.0
thread_integer: 11.9974408189
thread_bit_convert: 0.0
thread_control: 1.0
thread_compute_ld_st: 2.9990403071
thread_thread_misc: 3.0
instructions per thread : 19.9961612284
instructions per warp   : 21.0
gld transaction  / gst transaction = 2.00000025008

ld sass = 1 , st sass = 1
thread_compute_ld_st: 2.9990403071
gld inst num = 2.0
Global load inst. (per warp) = 1300.0 (clocks)
gst inst num = 1.0
Global store inst. (per warp) = 15.0 (clocks)
=> Memory inst. (per warp) = 1315.0 (clocks)

Int inst. number (before)    = 11.9974408189
Int inst. number (round up)  = 12.0
Integer inst. (per warp) = 180.0 (clocks)
FP32 inst. number (before)    = 0.999680102367
FP32 inst. number (round up)  = 1.0
FP32 inst. (per warp) = 15.0 (clocks)
FP64 inst. number (before)    = 0.0
FP64 inst. number (round up)  = 0.0
FP64 inst. (per warp) = 0.0 (clocks)
=> Compute inst. (per warp) = 195.0 (clocks)
```
