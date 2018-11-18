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
lists_dir = os.path.join(cwd, "lists")

def map_ids_to_binary_mtx(dbs):
    for k in dbs.keys():
        # read in list
        tfs = {}
        with open(os.path.join(lists_dir, "%s.txt" % (k)), "r") as lfh:
            idx = 0
            for line in lfh:
                tfs[line.rstrip()] = idx
                idx += 1
            tfs_length = len(tfs.keys())
        for p in paddings:
            sys.stderr.write("%s | %d\n" % (k, p))
            with open(os.path.join(cwd, "%s_ids" % (k), "probe.db.%d.starch.mtx" % (p)), "w") as pfh:
                arch_fn = os.path.join(cwd, "%s_ids" % (k), "probe.db.%d.starch" % (p))
                if not os.path.exists(arch_fn):
                    raise SystemError("could not find archive fn [%s]\n" % (arch_fn))
                try:
                    proc = subprocess.Popen("unstarch %s" % (arch_fn), stdout=subprocess.PIPE, shell=True)
                except OSError as ose:
                    raise SystemError("arch_fn: [%s]\n" % (arch_fn))
                while True:
                    line = proc.stdout.readline()
                    if line != b'':
                        (chrom, start, stop, id_str) = line.decode('utf-8').rstrip().split('\t')
                        (probe, probe_tf_overlaps) = id_str.split('|')
                        probe_tfs = probe_tf_overlaps.split(';')
                        probe_tfs_bins = [0] * tfs_length
                        if len(probe_tf_overlaps) == 0:
                            continue
                        for probe_tf in probe_tfs:
                            try:
                                probe_tfs_bins[tfs[probe_tf]] = 1
                            except KeyError as ke:
                                raise SystemError("could not find key [%s|%d] in tfs object [%s]\n" % (probe_tf, len(probe_tf_overlaps), str(probe_tf_overlaps)))
                        pfh.write("%s\t%s\n" % (probe, '\t'.join([str(x) for x in probe_tfs_bins])))
                    else:
                        break

def main():
    map_ids_to_binary_mtx(dbs)

if __name__ == "__main__":
    main()
