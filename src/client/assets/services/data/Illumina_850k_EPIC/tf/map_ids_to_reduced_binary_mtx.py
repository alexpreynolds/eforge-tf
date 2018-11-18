#!/usr/bin/env python

import sys
import os
import subprocess
import shutil

dbs = {
    "xfac" :     "hg19.xfac.1e-4",
    "uniprobe" : "hg19.uniprobe.1e-4",
    "jaspar" :   "hg19.jaspar.1e-4",
    "taipale" :  "hg19.taipale.1e-4"
}

paddings = [0]

cwd = os.getcwd()

def map_ids_to_reduced_binary_mtx(dbs):
    for k in dbs.keys():
        for p in paddings:
            sys.stderr.write("%s | %d\n" % (k, p))
            with open(os.path.join(cwd, "%s_ids" % (k), "probe.db.%d.starch.mtx" % (p)), "r") as infh, open(os.path.join(cwd, "%s_ids" % (k), "probe.db.%d.starch.reduced.mtx" % (p)), "w") as outfh:
                for line in infh:
                    elems = line.rstrip().split('\t')
                    probe = elems[0]
                    bins = elems[1:]
                    outfh.write("%s\t%s\n" % (probe, ''.join(bins)))

def main():
    map_ids_to_reduced_binary_mtx(dbs)

if __name__ == "__main__":
    main()
