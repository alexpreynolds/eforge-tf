#!/usr/bin/env python

import sys
import os
import json
import subprocess

try:
    samples_fn = sys.argv[1]
    samples_filtered_fn = sys.argv[2]
    padding = int(sys.argv[3])
    probes_fn = sys.argv[4]
    chopped_probes_fn = sys.argv[5]
    chopped_probes_archive_fn = sys.argv[6]
except IndexError as ie:
    raise SystemError("specify arguments")

samples_obj = json.load(open(samples_fn))
perBase_fn = 'perBase.starch'
perBase_probe_fn = 'perBase.probe.starch'
reduced_probe_starch_fn = 'reduced.probe.starch'
reduced_probe_tabix_fn = 'reduced.probe.gz'
cwd = os.getcwd()
partition = "queue0"
mem_per_cpu = 12000

filtered_samples = {}
with open(samples_filtered_fn, "r") as ifh:
    filtered_samples = {l.rstrip():True for l in ifh}

def main():
    #chop_probes(probes_fn, chopped_probes_fn, chopped_probes_archive_fn)
    map_job_ids = []
    for sample in samples_obj['samples']:
        #if sample == 'GM12878-DS10671' or sample == 'GM12878-DS49684B':
        if sample in filtered_samples:
            map_job_id = signal_map(sample)
            map_job_ids.append(map_job_id)

    reduce_job_ids = []
    idx = 0
    for sample in samples_obj['samples']:
        #if sample == 'GM12878-DS10671' or sample == 'GM12878-DS49684B':
        if sample in filtered_samples:
            reduce_job_id = signal_reduce(sample, map_job_ids[idx])
            reduce_job_ids.append(reduce_job_id)
            idx += 1

def chop_probes(probes, chopped_probes, chopped_probes_archive):
    if not os.path.exists(chopped_probes_archive):
        sys.stderr.write("chopping and compressing probes into Starch...\n")
        try:
            cmd = "./chop.sh %d %s %s" % (padding, probes, chopped_probes_archive)
            print(cmd)
            sys.exit(1)
            result = subprocess.check_call(cmd, shell=True)
        except subprocess.CalledProcessError as cpe:
            sys.stderr.write("Something went wrong [%s]\n" % (cpe))

def signal_map(sample):
    fq_chopped_probes_archive_fn = os.path.join(cwd, chopped_probes_archive_fn)
    sample_fn = os.path.join(cwd, sample, perBase_fn)
    probe_mapped_sample_fn = os.path.join(cwd, sample, perBase_probe_fn)
    work_dir = os.path.join(cwd, sample)
    error_fn = os.path.join(cwd, "error_log.txt")
    job_name = "eforge_profile_850k_probe_vs_%s" % (sample)
    cluster_script = os.path.join(cwd, "map_cluster.sh")
    cmd = "sbatch --parsable --partition=\"%s\" --workdir=\"%s\" --error=\"%s\" --job-name=\"%s\" --wrap=\"%s %s %s %s\"" % (partition, work_dir, error_fn, job_name, cluster_script, fq_chopped_probes_archive_fn, sample_fn, probe_mapped_sample_fn)
    print(cmd)
    try:
        result = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as cpe:
        sys.stderr.write("Something went wrong [%s]\n" % (cpe))
        raise SystemError(cpe)
    job_id = int(result.rstrip())
    return job_id

def signal_reduce(sample, map_job_id):
    probe_mapped_sample_fn = os.path.join(cwd, sample, perBase_probe_fn)
    probe_reduced_sample_starch_fn = os.path.join(cwd, sample, reduced_probe_starch_fn)
    probe_reduced_sample_tabix_fn = os.path.join(cwd, sample, reduced_probe_tabix_fn)
    work_dir = os.path.join(cwd, sample)
    job_name = "eforge_profile_850k_probe_reduce_%s" % (sample)
    cluster_script = os.path.join(cwd, "reduce_cluster.sh")
    pernode_script = os.path.join(cwd, "reduce.py")
    cmd = "sbatch --dependency=\"afterok:%d\" --parsable --mem-per-cpu=%d --partition=\"%s\" --workdir=\"%s\" --job-name=\"%s\" --wrap=\"%s %s %s %d %s %s\"" % (map_job_id, mem_per_cpu, partition, work_dir, job_name, cluster_script, pernode_script, probe_mapped_sample_fn, padding, probe_reduced_sample_starch_fn, probe_reduced_sample_tabix_fn)
    print(cmd)
    try:
        result = subprocess.check_output(cmd, shell=True)
    except subprocess.CalledProcessError as cpe:
        sys.stderr.write("Something went wrong [%s]\n" % (cpe))
        raise SystemError(cpe)
    job_id = int(result.rstrip())
    return job_id

if __name__ == "__main__":
    main()
