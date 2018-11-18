SHELL:=/bin/bash

fasta_dir=/net/seq/data/genomes/informatics/hg19
probe_fn=/net/seq/data/projects/eForge/www/tf/browser/src/client/assets/services/data/illumina_850k_epic/probes/MethylationEPIC_v-1-0_B4_tabs_hg19_final.bed
out_fasta_fn=sequences.probe.fa
out_fasta_gz_fn=sequences.probe.fa.gz
out_starch_fn=sequences.probe.starch
out_tabix_fn=sequences.probe.gz
padding=500

all: seq reformat compress

seq:
	module add bedops
	module add samtools
	module add htslib
#	if [ ! -f ${out_fasta_gz_fn} ]; then bedops --range ${padding} --everything ${probe_fn} | ./bed2faidxsta.pl --fastaDir=${fasta_dir} > ${out_fasta_fn}; else gunzip -c ${out_fasta_gz_fn} > ${out_fasta_fn}; fi
	bedops --range ${padding} --everything ${probe_fn} | ./bed2faidxsta.pl --fastaDir=${fasta_dir} > ${out_fasta_fn}

reformat: reformat_starch reformat_tabix

reformat_starch:
	awk -vpadding=${padding} -vOFS="\t" '{ print padding,($$2-padding),($$3+padding); }' ${probe_fn} > .reformat-md
	awk '(NR%2==0)' ${out_fasta_fn} > .reformat-seq
	paste ${probe_fn} .reformat-md .reformat-seq | starch --omit-signature - > ${out_starch_fn}
	rm .reformat-md .reformat-seq

reformat_tabix:
	awk -vpadding=${padding} -vOFS="\t" '{ print padding,($$2-padding),($$3+padding); }' ${probe_fn} > .reformat-md
	awk '(NR%2==0)' ${out_fasta_fn} > .reformat-seq
	paste ${probe_fn} .reformat-md .reformat-seq | bgzip -c > ${out_tabix_fn}
	tabix -p bed ${out_tabix_fn}
	rm .reformat-md .reformat-seq

compress:
	gzip -c ${out_fasta_fn} > ${out_fasta_gz_fn}
	rm ${out_fasta_fn}
