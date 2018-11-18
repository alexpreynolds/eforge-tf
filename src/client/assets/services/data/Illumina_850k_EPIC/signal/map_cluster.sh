#!/bin/bash

#
# map_cluster
#

#SBATCH --output="map_run.out"
#SBATCH --error="map_run.err"
#SBATCH --mem-per-cpu=6000

module add bedops

ref=$1
map=$2
output=$3

bedmap --count --echo --echo-map-score --prec 0 --delim '\t' ${ref} ${map} | awk '{ if ($1=="0") { print $0"0"; } else { print $0; } }' | cut -f2- | starch --omit-signature - > ${output}
