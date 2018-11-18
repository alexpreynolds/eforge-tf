#!/bin/bash

#
# convert_cluster
#

#SBATCH --output="conver_run.out"
#SBATCH --error="convert_run.err"
#SBATCH --mem-per-cpu=4000

module add htslib
module add samtools
module add bedops/2.4.32-megarow

src=$1
dest=$2

unstarch ${src} | bgzip -c > ${dest}
tabix -p bed ${dest}
