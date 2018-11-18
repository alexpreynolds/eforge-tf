SHELL:=/bin/bash

probes=../probes/MethylationEPIC_v-1-0_B4_tabs_hg19_final.bed

all: map map_ids

map:
	./map.py ${probes}

generate_ordered_tf_list:
	./generate_ordered_tf_list.py

map_ids:
	./map_ids.py ${probes}

# tbd
map_ids_to_binary_mtx:
	./map_ids_to_binary_mtx.py 

map_ids_to_reduced_binary_mtx:
	./map_ids_to_reduced_binary_mtx.py

import_reduced_binary_mtx_to_sqlite3_db:
	./import_reduced_binary_mtx_to_sqlite3_db.py
