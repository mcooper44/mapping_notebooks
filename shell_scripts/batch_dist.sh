#!/bin/bash

# uses calc a C-style arbitrary precision calculator (version 2.15.0.4)
# accepts two pairs of longitude latitude pairs separated by 
# a single space and echoes the distance in KM between the two points
# i.e. long lat long lat
# usage is:
# script [filename] > output_file.txt

R=3959.87433

while read -r line; do
	stringarray=($line)
	lon1=${stringarray[0]}
	lat1=${stringarray[1]}
	lon2=${stringarray[2]}
	lat2=${stringarray[3]}
	dLat=$(echo "d2r($lat2 - $lat1)" | calc -p)
	dLon=$(echo "d2r($lon2 - $lon1)" | calc -p)
	lat1=$(echo "d2r($lat1)" | calc -p)
	lat2=$(echo "d2r($lat2)" | calc -p)
	a=$(echo "sin($dLat/2)**2 + cos($lat1)*cos($lat2)*sin($dLon/2)**2" | calc -p)
	c=$(echo "2*asin(sqrt($a))" | calc -p)
	echo "$R * $c" | calc -p
done < "$1"
