probes=../probes/MethylationEPIC_v-1-0_B4_tabs_hg19_final.bed
summary=summary.txt.final
samples=../signal/samples.json
filtered_samples=filtered_samples.txt
filtered_samples_json=filtered_samples.json
filtered_sample_aggregates_json=filtered_sample_aggregates.json

all: filter filtered_samples_to_json

filter:
	./filter.py ${samples} ${summary} > ${filtered_samples}

filtered_samples_to_json:
	./fs2json.py ${filtered_samples} > ${filtered_samples_json}

filter_to_sample_aggregates:
	./fs2agg.py ${filtered_samples} > ${filtered_sample_aggregates_json}

map:
	./map.py ${probes} ${summary} ${filtered_samples_json}
