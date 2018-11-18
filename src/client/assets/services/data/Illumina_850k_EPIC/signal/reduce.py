#!/usr/bin/env python

import sys
import os
import json
import subprocess

try:
    probe_sample_fn = sys.argv[1]
    padding = int(sys.argv[2])
except IndexError as ie:
    raise SystemError("specify arguments")

window = padding*2 + 1

def main():
    ids = {}
    extract = subprocess.Popen(['unstarch', probe_sample_fn], stdout=subprocess.PIPE)
    for elem in extract.stdout:

        (chromosome, start, stop, id, score) = elem.rstrip().split('\t')

        if id not in ids:
            ids[id] = {}
            ids[id]['chromosome'] = chromosome
            ids[id]['start'] = int(start)
            ids[id]['stop'] = int(start) + padding*2 + 1
            ids[id]['scores'] = []

        ids[id]['scores'].append(int(score))

        if len(ids[id]['scores']) == window:
            sys.stdout.write("%s\t%d\t%d\t%s\t%d\t%d\t%d\t%s\n" % (ids[id]['chromosome'],
                                                                   ids[id]['start'] + padding,
                                                                   ids[id]['stop'] - padding,
                                                                   id,
                                                                   padding,
                                                                   ids[id]['start'],
                                                                   ids[id]['stop'],
                                                                   ','.join([str(x) for x in ids[id]['scores']])))
            del(ids[id])

if __name__ == "__main__":
    main()
