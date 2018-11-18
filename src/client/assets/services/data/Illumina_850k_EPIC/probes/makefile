SHELL:=/bin/bash
all: oneBased sortOneBased sortZeroBased sqlite3db

oneBased:
	awk '{ print $$1"\t"($$2+1)"\t"($$3+1)"\t"$$4; }' MethylationEPIC_v-1-0_B4_tabs_hg19_final.bed > MethylationEPIC_v-1-0_B4_tabs_hg19_final.oneBased.bed

sortOneBased:
	sort -k4,4 MethylationEPIC_v-1-0_B4_tabs_hg19_final.oneBased.bed | awk -vOFS="\t" '{ print $$4, $$1, $$2, $$3; }' > MethylationEPIC_v-1-0_B4_tabs_hg19_final.oneBased.bed.idsort.txt

sortZeroBased:
	sort -k4,4 MethylationEPIC_v-1-0_B4_tabs_hg19_final.bed | awk -vOFS="\t" '{ print $$4, $$1, $$2, $$3; }' > MethylationEPIC_v-1-0_B4_tabs_hg19_final.bed.idsort.txt

sqlite3db:
	awk -vOFS="\t" -vFS="\t" '{ print NR, "1", $$0}' MethylationEPIC_v-1-0_B4_tabs_hg19_final.bed.idsort.txt > MethylationEPIC_v-1-0_B4_tabs_hg19_final.bed.idsort.txt.sql3import
	sqlite3 probes.db < create.sql
	rm MethylationEPIC_v-1-0_B4_tabs_hg19_final.bed.idsort.txt.sql3import
