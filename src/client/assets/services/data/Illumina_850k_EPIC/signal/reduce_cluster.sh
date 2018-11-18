#!/bin/bash

#
# reduce_cluster
#

#SBATCH --output="reduce_run.out"
#SBATCH --error="reduce_run.err"
#SBATCH --mem-per-cpu=4000

module add bedops

reduce=$1
map=$2
padding=$3
starch=$4
tabix=$5

module add htslib
module add bedops/2.4.33-megarow
module add samtools

${reduce} ${map} ${padding} | sort-bed - | starch --omit-signature - > ${starch}
unstarch ${starch} | bgzip -c > ${tabix}
tabix -p bed ${tabix}
