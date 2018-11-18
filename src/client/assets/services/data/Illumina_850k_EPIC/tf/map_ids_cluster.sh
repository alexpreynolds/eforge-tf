#!/bin/bash

#
# map_cluster
#

module add bedops/2.4.35-megarow
module add htslib
module add samtools

ref=$1
map=$2
starch_output=$3
tabix_output=$4

unstarch ${map} | awk '($5 <= 1e-5)' | bedmap --echo --echo-map-id-uniq ${ref} - | starch --omit-signature - > ${starch_output}
unstarch ${starch_output} | bgzip -c > ${tabix_output}
tabix -p bed ${tabix_output}

