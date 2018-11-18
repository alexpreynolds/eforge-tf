#!/usr/bin/env python

import sys
import os
import json
import subprocess
import shutil

try:
    probe_fn = sys.argv[1]
    summary_fn = sys.argv[2]
    filtered_json_fn = sys.argv[3]
except IndexError as ie:
    raise SystemError("specify arguments")

fp_dir = "/home/sjn/proj/encode3/breeze/fp.calls.hg19/results"

paddings = [20, 50, 100, 200, 500]

cwd = os.getcwd()
map_prefix = "probe.fp"
map_starch_suffix = "starch"
map_tabix_suffix = "gz"
partition = "queue0"
mem_per_cpu = 12000
fq_probe_fn = os.path.join(cwd, probe_fn)

def map():
    with open(filtered_json_fn, "r") as fjh:
        filtered_samples_obj = json.load(fjh)
    filtered_samples_arr = filtered_samples_obj['samples']
    filtered_samples_table = {}
    for filtered_sample_obj in filtered_samples_arr:
        v = filtered_sample_obj.keys()[0]
        k = v.split('-')[1] 
        filtered_samples_table[k] = v

    job_ids = []
    with open(summary_fn, "r") as sfh:
        line = sfh.readline()
        for line in sfh:
            (sample, fdr, elements, bases, unique_bases) = line.rstrip().split()
            fp_fn = os.path.join(fp_dir, sample, "%s.ratesJVJS.footprints_FDR5pct.final.starch" % (sample))
            if not os.path.exists(fp_fn):
                raise SystemError("Cannot find fp [%s]\n" % (fp_fn))
            dest_dir = os.path.join(cwd, filtered_samples_table[sample])
            if os.path.exists(dest_dir):
                shutil.rmtree(dest_dir)
            os.makedirs(dest_dir)
            work_dir = dest_dir
            for p in paddings:
                dest_starch_fn = os.path.join(dest_dir, "%s.%d.%s" % (map_prefix, p, map_starch_suffix))
                dest_tabix_fn = os.path.join(dest_dir, "%s.%d.%s" % (map_prefix, p, map_tabix_suffix))
                job_name = "eforge_profile_850k_probe_fp_map_%s_%d" % (sample, p)
                cluster_script = os.path.join(cwd, "map_cluster.sh")
                cmd = "sbatch --parsable --mem-per-cpu=%d --partition=\"%s\" --workdir=\"%s\" --job-name=\"%s\" --wrap=\"%s %s %s %s %s %d\"" % (mem_per_cpu, partition, work_dir, job_name, cluster_script, fq_probe_fn, fp_fn, dest_starch_fn, dest_tabix_fn, p)
                print(cmd)
                try:
                    result = subprocess.check_output(cmd, shell=True)
                except subprocess.CalledProcessError as cpe:
                    sys.stderr.write("Something went wrong [%s]\n" % (cpe))
                    raise SystemError(cpe)
                job_ids.append(result.rstrip())

    return job_ids

def main():
    job_ids = map()

if __name__ == "__main__":
    main()
