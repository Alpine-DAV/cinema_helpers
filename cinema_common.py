# Copyright (c) Lawrence Livermore National Security, LLC and other Ascent
# Project developers. See top-level LICENSE AND COPYRIGHT files for dates and
# other details. No copyright assignment is required to contribute to Ascent.

import glob
import os
import shutil
from os.path import join as pjoin


# given a database path, detect the type of db
def cinema_db_name(path):
    # given cdb dir get name
    return os.path.split(path)[1]

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
# example: cinema_db_copy("my_stuff.cdb","my_copy.cdb")
def cinema_db_copy(src_db,dest_db):
    if cinema_db_type(src_db) == "unknown":
        print("ERROR: can't copy db with unknown spec")
        sys.exit(-1)
    print("[copying {0} to {1}]".format(os.path.abspath(src_db),
                                        os.path.abspath(dest_db)))
    shutil.copytree(src_db,dest_db)
