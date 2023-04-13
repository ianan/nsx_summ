#!/bin/bash

echo "| ObsID  |  LTC |  Map |"
echo "|---|---|---|"
for d in ltc*; do
	fname=${d:4:29}
	obsid=${d:18:11}
	echo "|$obsid|![]($d)|![](map_$fname.png)|"
	# echo "$fname"".png"
done
