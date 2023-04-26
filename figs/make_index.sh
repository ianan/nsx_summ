#!/bin/bash

# Make an index.md file with table of each pointing obsid, ltc and map

maindir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
echo "$maindir"

for dd in ns_20*
do
	# cd $dd
	# echo "|  LtC |  Map & Eph |" | tee index.md
	# echo "|:---:|:---:|" | tee -a index.md
	# for d in ltc*
	# do
	# 	# echo "$dd - $d"
	# 	fname=${d:4:29}
	# 	obsid=${d:18:11}
	# 	echo "|![]($d)|$obsid<br/>![](map_$fname.png)<br/>![](orbeph_$fname.png)|" | tee -a index.md
	# done

	cd $dd
	echo "## $dd" | tee index.md
	echo " " | tee -a index.md
	echo "|  Lightcurves |  Map | Orbit |" | tee -a index.md
	echo "|:---:|:---:|:---:|" | tee -a index.md
	for d in ltc*
	do
		# echo "$dd - $d"
		fname=${d:4:29}
		obsid=${d:18:11}
   		# echo "|$obsid|![]($d)|![](map_$fname.png)|![](eph_$fname.png)|" | tee -a index.md
		echo "|[![]($d)]($d)|**$obsid [hk plot](hkltc_$fname.png)**<br/>[![](map_$fname.png)](map_$fname.png)|[![](orbeph_$fname.png)](orbeph_$fname.png)|" | tee -a index.md
	done
	cd $maindir
done