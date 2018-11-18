#!/usr/bin/env python

import sqlite3
import os
import sys
import shutil

dbs = {
    "xfac" :     "hg19.xfac.1e-4",
    "uniprobe" : "hg19.uniprobe.1e-4",
    "jaspar" :   "hg19.jaspar.1e-4",
    "taipale" :  "hg19.taipale.1e-4"
}

paddings = [0]

cwd = os.getcwd()

def create_tables(dbs):
    for k in dbs.keys():
        for p in paddings:
            sqlite_fn = os.path.join(cwd, "%s_ids" % (k), "probe.db.%d.starch.reduced.mtx.sqlite" % (p))
            if os.path.exists(sqlite_fn):
                os.remove(sqlite_fn)
            table_name = "%s" % (k)
            # connect
            conn = sqlite3.connect(sqlite_fn)
            c = conn.cursor()
            # create
            c.execute('CREATE TABLE IF NOT EXISTS {tn} ({nf1} {ft1} PRIMARY KEY, {nf2} {ft2});'\
                      .format(tn=table_name, nf1='probe', ft1='TEXT', nf2='bitstring', ft2='TEXT'))
            # commit changes and close
            conn.commit()
            conn.close()

def import_reduced_binary_mtx(dbs):
    for k in dbs.keys():
        for p in paddings:
            sys.stderr.write("%s | %d\n" % (k, p))
            sqlite_fn = os.path.join(cwd, "%s_ids" % (k), "probe.db.%d.starch.reduced.mtx.sqlite" % (p))
            if not os.path.exists(sqlite_fn):
                raise SystemError("cannot find db [%s]\n" % (sqlite_fn))
            table_name = "%s" % (k)
            # connect
            conn = sqlite3.connect(sqlite_fn)
            c = conn.cursor()
            # import
            with open(os.path.join(cwd, "%s_ids" % (k), "probe.db.%d.starch.reduced.mtx" % (p)), "r") as pfh:
                for line in pfh:
                    (probe, bitstring) = line.rstrip().split('\t')
                    try:
                        c.execute("INSERT INTO {tn} ({pf}, {bf}) VALUES ('{pv}', '{bv}');".\
                                  format(tn=table_name, pf='probe', bf='bitstring', pv=probe, bv=bitstring))
                    except sqlite3.IntegrityError:
                        sys.stderr.write('ERROR: probe ID already exists in PRIMARY KEY column {}\n'.format('probe'))
            # cleanup
            conn.commit()
            conn.close()

def main():
    create_tables(dbs)
    import_reduced_binary_mtx(dbs)

if __name__ == "__main__":
    main()
