# Copyright (c) Lawrence Livermore National Security, LLC and other Ascent
# Project developers. See top-level LICENSE AND COPYRIGHT files for dates and
# other details. No copyright assignment is required to contribute to Ascent.

import sys
import json
import glob
import os

from os.path import join as pjoin

from cinema_common import *

# Given a cdb (directory) finds Spec A info.json
# Copies Cinema DB files into `_output/database.cdb`
# Copies spec a viewer html and js to `_output/cinema_spec_a_viewer/`
# Creates custom `_output/cinema_spec_a_viewer/index.html`

def cinema_db_create_spec_a_viewer(db_path,dest_root):
    db_name =  cinema_db_name(db_path)
    dest_dir =  pjoin(dest_root,"cinema_spec_a_viewer")
    print("[{0}: {1}]").format(db_name,os.path.abspath(db_path))
    print("[copying {0} to {1}]".format(db_path, dest_dir))
    # copy cinema resources to output
    shutil.copytree(pjoin("viewers","cinema_spec_a"),dest_dir)
    # copy cdb to output
    dest_db  =pjoin(dest_dir, db_name)
    cinema_db_copy(db_path,dest_db)
    # parse info.json and create info.js js that connects the
    # db to the viewer
    db_info = json.load(open(pjoin(dest_db,"image","info.json")))
    db_info["name_pattern"] = pjoin(db_name,"image",db_info["name_pattern"])
    js_src = "var info = " + json.dumps(db_info,indent=2) + ";"
    # write final js file
    ofname = pjoin(dest_dir,"info.js")
    open(ofname,"w").write(js_src)
    print("[created: {0}]".format(ofname))
    print("[open {0}/index.html to view]".format(dest_dir))
    return dest_dir


def main():
    if len(sys.argv) < 1:
        print("usage: python cinema_cdb_generate_spec_a_viewer.py input.cdb <output_dir>")
        print("       (default output_dir = _output)")
        sys.exit(-1)
    db_path = sys.argv[1]
    dest_dir = "_output"
    if(len(sys.argv) > 2):
        dest_dir = sys.argv[2]
    dest_dir = os.path.abspath(dest_dir)
    if os.path.exists(pjoin(dest_dir,"cinema_spec_a_viewer")):
        print("")
        print("ERROR: Output dir {0} already exists".format(pjoin(dest_dir,"cinema_spec_a_viewer")))
        print("       This script won't overwrite, please remove or provide new output dir.")
        print("")
        sys.exit(-1)
    if not os.path.isdir(db_path):
        print("")
        print("ERROR: {0} is not a directory".format(db_path))
        print("")
        sys.exit(-1)
    db_type = cinema_db_type(db_path)
    if not db_type == "a":
        print("")
        print("ERROR: {0} database type: {1}".format(db_path,db_type))
        print("       Expected cinema spec a (legacy image) database.")
        print("")
        sys.exit(-1)

    cinema_db_create_spec_a_viewer(db_path,dest_dir);


if __name__ == "__main__":
    main()
