SHELL:=/bin/bash

samples=samples.json
filtered_samples=../fp/filtered_samples.txt
#filtered_samples=./rerun.txt
padding=500
probes=../probes/MethylationEPIC_v-1-0_B4_tabs_hg19_final.bed
chopped_probes=../probes/MethylationEPIC_v-1-0_B4_tabs_hg19_final.chopped.bed
chopped_probes_archive=../probes/MethylationEPIC_v-1-0_B4_tabs_hg19_final.chopped.bed.starch

all: link map

link:
	./link.py > ${samples}

map:
	module add bedops
	./map.py ${samples} ${filtered_samples} ${padding} ${probes} ${chopped_probes} ${chopped_probes_archive}

convert:
	module add htslib
	./convert.py ${samples} ${filtered_samples}
