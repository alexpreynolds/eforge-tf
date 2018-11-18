#!/usr/bin/env python

import sys
import os
import json
import subprocess

try:
    samples_fn = sys.argv[1]
    samples_filtered_fn = sys.argv[2]
except IndexError as ie:
    raise SystemError("specify arguments")

samples_obj = json.load(open(samples_fn))
reduced_probe_starch_fn = 'reduced.probe.starch'
reduced_probe_tabix_fn = 'reduced.probe.gz'
cwd = os.getcwd()
partition = "queue0"

filtered_samples = {}
with open(samples_filtered_fn, "r") as ifh:
    filtered_samples = {l.rstrip():True for l in ifh}

def main():
    #
    # chop_probes(probes_fn, chopped_probes_fn, chopped_probes_archive_fn)
    #
    job_ids = []
    for sample in samples_obj['samples']:
        #if sample == 'GM12878-DS10671' or sample == 'GM12878-DS49684B':
        if sample in filtered_samples:
            job_id = signal_convert(sample)
            job_ids.append(job_id)

def signal_convert(sample):
    src_fn = os.path.join(cwd, sample, reduced_probe_starch_fn)
    dest_fn = os.path.join(cwd, sample, reduced_probe_tabix_fn)
    work_dir = os.path.join(cwd, sample)
    job_name = "eforge_profile_850k_probe_convert_%s" % (sample)
    cluster_script = os.path.join(cwd, "convert_cluster.sh")
    cmd = "sbatch --parsable --partition=\"%s\" --workdir=\"%s\" --job-name=\"%s\" --wrap=\"%s %s %s\"" % (partition, work_dir, job_name, cluster_script, src_fn, dest_fn)
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
