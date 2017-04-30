# Motivation
Understanding the block size effect on gpu kernel runtime for a particular gpu architecture.

# Applications in cuda sdk 8.0
Graphics apps are not included since the nature of non-stop rendering.

Applications that take long time (> 1 min) to profiling are not included.

# Classify Kernel
check classify.md

Here is an exmaple.

```
cd eigenvalues

cp ../shell_scripts/*.sh .

cp ../warp_classify_template.ipynb warp_classify.ipynb

# generate trace and metrics
./1_traceGen.sh ./eigenvalues

# run warp_classify.ipynb

# check the unique kernel names

# get the sass of the kernel
./2_kernelsassDump.sh ./eigenvalues bisectKernelLarge

# extract the kernel sass
./3_sassResultGen.sh


# run the rest of warp_classify.ipynb

```
