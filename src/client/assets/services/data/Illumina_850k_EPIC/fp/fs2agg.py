#!/usr/bin/env python

import sys
import json

try:
    samples_filtered_fn = sys.argv[1]
except IndexError as ie:
    raise SystemError("specify arguments")

filtered_samples = []
with open(samples_filtered_fn, "r") as ifh:
    filtered_samples = [l.rstrip() for l in ifh]

ps_obj = {}
sorted_fss = sorted(filtered_samples, key=lambda s: s.lower())
for fs in sorted_fss:
    fsvs = fs.split("-")
    ct = fsvs[0]
    ds = fsvs[1]
    if ct not in ps_obj:
        ps_obj[ct] = []
    ps_obj[ct].append(fs)

samples_obj = { 'samples' : ps_obj }

print(json.dumps(samples_obj))
