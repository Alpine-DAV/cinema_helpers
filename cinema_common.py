# Copyright (c) Lawrence Livermore National Security, LLC and other Ascent
# Project developers. See top-level LICENSE AND COPYRIGHT files for dates and
# other details. No copyright assignment is required to contribute to Ascent.

import glob
import os
import sys
import shutil
from os.path import join as pjoin


# given a database path, return the db name
def cinema_db_name(path):
    # given cdb dir get name
    if path.endswith(os.sep):
        path = path[:path.rfind(os.sep)]
    res = os.path.split(path)[1]
    if res == "":
        print("")
        print("ERROR: database name is empty for db {0}".format(path))
        print("")
        sys.exit(-1)
    return  res

# given a database path, detect the type of db
def cinema_db_type(path):
    res = "unknown"
    # spec d
    if os.path.isfile(pjoin(path,'data.csv')):
        res = "d"
    # spec a
    elif os.path.isfile(pjoin(path,'image','info.json')):
        res = "a"
    return res

# helper to make a copy of a cinema db
# example: cinema_db_copy("my_stuff.cdb","my_stuff_copy.cdb")
def cinema_db_copy(src_db,dest_db):
    db_type = cinema_db_type(src_db)
    if cinema_db_type(src_db) == "unknown":
        print("")
        print("ERROR: {0} database type: {1}".format(src_db,db_type))
        print("ERROR: we won't copy db with unknown spec")
        print("")
        sys.exit(-1)
    print("[copying {0} to {1}]".format(os.path.abspath(src_db),
                                        os.path.abspath(dest_db)))
    shutil.copytree(src_db,dest_db)
