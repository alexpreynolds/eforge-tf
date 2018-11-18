.mode tabs
.header off

PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS arrays (
  array_id INTEGER PRIMARY KEY,
  array_name TEXT NOT NULL UNIQUE
);

INSERT INTO arrays(array_id, array_name) SELECT 1, 'MethylationEPIC_v-1-0_B4_tabs_hg19_final.bed.idsort.txt' WHERE NOT EXISTS (SELECT * FROM arrays WHERE array_id = 1);

CREATE TABLE IF NOT EXISTS probes (
  probe_id INTEGER PRIMARY KEY,
  array_id INTEGER,
  probe_name TEXT NOT NULL UNIQUE,
  chr TEXT NOT NULL,
  start INTEGER NOT NULL,
  stop INTEGER NOT NULL,
  FOREIGN KEY (array_id) REFERENCES arrays(array_id) ON DELETE CASCADE
);

CREATE INDEX probe_names ON probes(probe_name);

.import MethylationEPIC_v-1-0_B4_tabs_hg19_final.bed.idsort.txt.sql3import probes

.dump
.exit
