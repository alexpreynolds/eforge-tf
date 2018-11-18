#!/usr/bin/env python

import sys
import os
import subprocess
import shutil

fimo_dir = "/net/seq/data/projects/motifs/fimo"
fimo_dbs = {
    "xfac" :     "hg19.xfac.1e-4",
    "uniprobe" : "hg19.uniprobe.1e-4",
    "jaspar" :   "hg19.jaspar.1e-4",
    "taipale" :  "hg19.taipale.1e-4"
}
fimo_scan_fn = "fimo.combined.1e-4.parsed.starch"

cwd = os.getcwd()
mem_per_cpu = 2000
partition = "queue0"

def generate_ordered_list(dbs):
    dest_dir = os.path.join(cwd, "lists")
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
    for k in dbs.keys():
        fimo_fn = os.path.join(fimo_dir, dbs[k], fimo_scan_fn)
        if not os.path.exists(fimo_fn):
            raise SystemError("could not find FIMO hits [%s]\n" % (fimo_fn))
        work_dir = os.path.join(cwd, "lists")
        job_name = "ordered_tf_list_%s" % (k)
        dest_fn = os.path.join(dest_dir, "%s.txt" % (k))
        wrap_cmd = "module add bedops && unstarch %s | awk '(\$5<=1e-5)' | cut -f4 | sort | uniq > %s" % (fimo_fn, dest_fn)
        cmd = "sbatch --parsable --mem-per-cpu=%d --partition=\"%s\" --workdir=\"%s\" --job-name=\"%s\" --wrap=\"%s\"" % (mem_per_cpu, partition, work_dir, job_name, wrap_cmd)
        try:
            result = subprocess.check_output(cmd, shell=True)
        except subprocess.CalledProcessError as cpe:
            sys.stderr.write("Something went wrong [%s]\n" % (cpe))
            raise SystemError(cpe)

def main():
    generate_ordered_list(fimo_dbs)

if __name__ == "__main__":
    main()
