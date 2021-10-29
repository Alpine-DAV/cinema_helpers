# Copyright (c) Lawrence Livermore National Security, LLC and other Ascent
# Project developers. See top-level LICENSE AND COPYRIGHT files for dates and
# other details. No copyright assignment is required to contribute to Ascent.

import sys
import json
import glob
import os
import itertools
import csv

from os.path import join as pjoin

from cinema_common import *

# Given a spec a cdb (directory), creates a new spec d database

def gen_path(pattern, keys, values):
    # note: fstrings would be nice here.
    res = pattern
    for i,k in enumerate(keys):
        tag = "{" + k + "}"
        res = res.replace(tag,str(values[i]))
    return res

def mkdirp(path):
    os.makedirs(path)

def cinema_db_convert_spec_a_to_spec_d(src_db_path,dest_db_path):
    # get source db info
    src_db_info = json.load(open(pjoin(src_db_path,"image","info.json")))
    # walk the structure and convert into spec d 
    pat = src_db_info["name_pattern"]
    args = src_db_info["arguments"].keys()
    vals = []
    for a in args:
        vals.append(src_db_info["arguments"][a]["values"])
    mkdirp(dest_db_path)
    csv_path = pjoin(dest_db_path,"data.csv")
    csv_out = csv.writer(open(csv_path,"w"), quoting=csv.QUOTE_ALL)
    # spec d header ex:
    # theta,phi,FILE
    # first our params from spec a
    csv_headers = list(args)
    # then add special entry for the image file
    csv_headers.append("FILE")
    csv_out.writerow(csv_headers)
    for entry in itertools.product(*vals):
        rel_image_path  = gen_path(pat,args,entry)
        # copy from source to dest 
        src_image_path  = pjoin(src_db_path,"image",rel_image_path)
        dest_image_path = pjoin(dest_db_path,"image",rel_image_path)
        mkdirp(os.path.split(dest_image_path)[0])
        shutil.copy(src_image_path,dest_image_path)
        # prep csv row for new db
        dest_row = list(entry)
        dest_row.append(pjoin("image",rel_image_path))
        csv_out.writerow(dest_row)
    print("[created spec d database: {0}]".format(dest_db_path))
    return dest_db_path


def main():
    if len(sys.argv) < 3:
        print("usage: python cinema_cdb_convert_spec_a_to_spec_d.py input.cdb output.cdb")
        sys.exit(-1)
    src_db_path   = os.path.abspath(sys.argv[1])
    dest_db_path  = os.path.abspath(sys.argv[2])
    if os.path.exists(dest_db_path):
        print("")
        print("ERROR: Output dir {0} already exists".format(dest_db_path))
        print("       This script won't overwrite, please remove or provide new output dir.")
        print("")
        sys.exit(-1)
    if not os.path.isdir(src_db_path):
        print("")
        print("ERROR: {0} is not a directory".format(src_db_path))
        print("")
        sys.exit(-1)
    db_type = cinema_db_type(src_db_path)
    if not db_type == "a":
        print("")
        print("ERROR: {0} database type: {1}".format(src_db_path,db_type))
        print("       Expected cinema spec a (legacy image) database.")
        print("")
        sys.exit(-1)

    cinema_db_convert_spec_a_to_spec_d(src_db_path,dest_db_path);


if __name__ == "__main__":
    main()
