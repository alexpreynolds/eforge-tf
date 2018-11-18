#!/usr/bin/env python

import sys
import os
import subprocess
import shutil

try:
    probe_fn = sys.argv[1]
except IndexError as ie:
    raise SystemError("specify arguments")

fimo_dir = "/net/seq/data/projects/motifs/fimo"

dbs = {
    "xfac" :     "hg19.xfac.1e-4",
    "uniprobe" : "hg19.uniprobe.1e-4",
    "jaspar" :   "hg19.jaspar.1e-4",
    "taipale" :  "hg19.taipale.1e-4"
}

paddings = [0]

cwd = os.getcwd()
map_prefix = "probe.db"
map_starch_suffix = "starch"
map_tabix_suffix = "gz"
fimo_scan_fn = "fimo.combined.1e-4.parsed.starch"
partition = "queue0"
mem_per_cpu = 12000

def fimo(dbs):
    job_ids = []
    for k in dbs.keys():
        for p in paddings:
            sys.stderr.write("searching IDs against [%s] with padding [%d]\n" % (k, p))
            fimo_fn = os.path.join(fimo_dir, dbs[k], fimo_scan_fn)
            if not os.path.exists(fimo_fn):
                raise SystemError("could not find FIMO hits [%s]\n" % (fimo_fn))
            dest_dir = os.path.join(cwd, "%s_ids" % (k))
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            os.makedirs(dest_dir)
            dest_starch_fn = os.path.join(dest_dir, "%s.%d.%s" % (map_prefix, p, map_starch_suffix))
            dest_tabix_fn = os.path.join(dest_dir, "%s.%d.%s" % (map_prefix, p, map_tabix_suffix))
            fq_probe_fn = os.path.join(cwd, probe_fn)
            work_dir = os.path.join(cwd, k)
            job_name = "eforge_profile_850k_probe_tf_map_ids_%s_%d" % (k, p)
            cluster_script = os.path.join(cwd, "map_ids_cluster.sh")
            cmd = "sbatch --parsable --mem-per-cpu=%d --partition=\"%s\" --workdir=\"%s\" --job-name=\"%s\" --wrap=\"%s %s %s %s %s\"" % (mem_per_cpu, partition, work_dir, job_name, cluster_script, fq_probe_fn, fimo_fn, dest_starch_fn, dest_tabix_fn)
            try:
                result = subprocess.check_output(cmd, shell=True)
            except subprocess.CalledProcessError as cpe:
                sys.stderr.write("Something went wrong [%s]\n" % (cpe))
                raise SystemError(cpe)
            job_ids.append(result.rstrip())
    return job_ids

def main():
    job_ids = fimo(dbs)

if __name__ == "__main__":
    main()
