#!/bin/bash

if [ "$#" -ne 2 ]; then
  echo "Usage: $0 ./app_name kernel_name" >&2
  exit 1
fi

app=$1
#echo $app

app_name=${app:2} # remove ./
#echo $app_name

out_file="$app_name.sm52.sass"

cuobjdump -sass  -arch=sm_52 $app > $out_file 2>&1

echo "SASS are dumped. => $out_file"

kernelName=$2
echo "Target Kernel Name : " "$kernelName"

#search the out_file for the sass of the target kernel



#
#  in some case, a kernel name may have other suffix 
#  kernelA, kernelA_modex, kernelA_modey
#  directly search for kernelA will cause error

# fix2: change to 'Pf' instead of 'PfS'
# fix3: change to 'P' instead of 'PfS' or 'Pf'

kern_pfs='P'
pat=$kernelName$kern_pfs
echo $pat

kern_begin=`awk "/$pat/{print NR}" $out_file`
echo "kernel sass begin at line :"  "$kern_begin"

# line with ......  as the sass block ending sign
ending_lines=`awk '/^\s+\.\.\.\.+/{print NR}' $out_file`
#echo $ending_lines


kern_end=''  
for currentline in $ending_lines
do
	#echo $currentline
	#echo $kern_begin
	if [ $currentline -gt $kern_begin ] ; then
		kern_end=$currentline
		break
	fi
done

echo "kernel sass end at line :"  "$kern_end"


### save the sass code between kern_begin and kern_end
suffix='.sm_52.sass'
kernel_sass_out=$kernelName$suffix
awk -v s="$kern_begin" -v e="$kern_end" 'NR>=s&&NR<=e' $out_file  > $kernel_sass_out

echo "Done! Check $kernel_sass_out"
