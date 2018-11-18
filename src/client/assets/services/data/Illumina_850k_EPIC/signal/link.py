#!/usr/bin/env python

import sys
import os
import glob
import re
import json

root_perbase_dir = '/net/seq/data/projects/ENCODE3_publications/human_hg19/perBase/results'
perbase_prefix = 'base-count'
perbase_suffix = 'perBase.36.hg19.bed.starch'

samples = []
for fn in glob.glob(os.path.join(root_perbase_dir, "%s.*.%s" % (perbase_prefix, perbase_suffix))):
    sample_pattern = re.compile('%s/%s.(.*).%s' % (root_perbase_dir, perbase_prefix, perbase_suffix))
    sample = sample_pattern.findall(fn)
    try:
        samples.append(sample[0])
    except IndexError as ie:
        pass

cwd = os.getcwd()
for sample in samples:
    fn = os.path.join(root_perbase_dir, "%s.%s.%s" % (perbase_prefix, sample, perbase_suffix))
    src_fn = fn
    dst_dir = os.path.join(cwd, sample)
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    dst_fn = os.path.join(dst_dir, "perBase.starch")
    try:
        os.symlink(src_fn, dst_fn)
    except OSError as ose:
        pass

samples_obj = {'samples' : {}}
for sample in samples:
    (tissue, ds) = sample.split('-')
    label = "%s (%s)" % (tissue, ds)
    samples_obj['samples'][sample] = label

sys.stdout.write('%s\n' % json.dumps(samples_obj, indent=2, sort_keys=True))
