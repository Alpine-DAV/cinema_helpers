# Copyright (c) Lawrence Livermore National Security, LLC and other Ascent
# Project developers. See top-level LICENSE AND COPYRIGHT files for dates and
# other details. No copyright assignment is required to contribute to Ascent.

import sys
import json
import glob
import os

from os.path import join as pjoin

from cinema_common import *

# helper to created proper embedded js
# for static site
def cinema_db_gen_meta_js(db_name, db_path):
    res = {"directory": os.path.basename(db_path),
           "name" : db_name }
    res["csvs"] = {}
    csvs = glob.glob(pjoin(db_path,"*.csv"))
    # we pull in csv data for js to parse
    for csv in csvs:
        csv_base = os.path.split(csv)[1]
        csv_base = os.path.splitext(csv_base)[0]
        print("[reading {0}]".format(csv))
        res["csvs"][csv_base] = open(csv).read()
    return res

# Given a cdb (directory), locate the data.csv file
# Copy Cinema DB files into `_output/cinema_explorer/database.cdb`
# Copy cinema explorer html and js to `_output/cinema_explorer`
# Create custom `_output/cinema_explorer/index.html`
def cinema_db_create_explorer(db_path,dest_root):
    db_name =  cinema_db_name(db_path)
    dest_dir =  pjoin(dest_root,"cinema_explorer")
    print("[{0}: {1}]".format(db_name,os.path.abspath(db_path)))
    print("[copying {0} to {1}]".format(db_path, dest_dir))
    # copy cinema resources to output
    shutil.copytree(pjoin("viewers","cinema_explorer"),dest_dir)
    # copy cdb to output
    dest_db  =pjoin(dest_dir, db_name)
    cinema_db_copy(db_path,dest_db)
    # gen static js that connects the db to the viewer
    db_info = []
    db_info.append(cinema_db_gen_meta_js(db_name, dest_db))
    js_src = "var databases = " + json.dumps(db_info,indent=2) + ";"
    # write final js file
    ofname = pjoin(dest_dir,"_gen_database.js")
    open(ofname,"w").write(js_src)
    print("[created: {0}]".format(ofname))
    print("[open {0}/index.html to view]".format(dest_dir))
    return dest_dir


def main():
    if len(sys.argv) < 1:
        print("usage: python cinema_cdb_generate_explorer.py input.cdb <output_dir>")
        print("       (default output_dir = _output)")
        sys.exit(-1)
    db_path = sys.argv[1]
    dest_dir = "_output"
    if(len(sys.argv) > 2):
        dest_dir = sys.argv[2]
    dest_dir = os.path.abspath(dest_dir)
    if os.path.exists(pjoin(dest_dir,"cinema_explorer")):
        print("")
        print("ERROR: Output dir {0} already exists".format(pjoin(dest_dir,"cinema_explorer")))
        print("       This script won't overwrite, please remove or provide new output dir.")
        print("")
        sys.exit(-1)
    if not os.path.isdir(db_path):
        print("")
        print("ERROR: {0} is not a directory".format(db_path))
        print("")
        sys.exit(-1)
    db_type = cinema_db_type(db_path)
    if not db_type == "d":
        print("")
        print("ERROR: {0} database type: {1}".format(db_path,db_type))
        print("       Expected cinema spec d (csv-style) database.")
        print("")
        sys.exit(-1)

    cinema_db_create_explorer(db_path,dest_dir);


if __name__ == "__main__":
    main()


