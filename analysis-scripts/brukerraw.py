#!/usr/bin/env python
"""This is my doc string.

Keyword arguments:
A -- apple
"""
# Copyright 2015 Austin Fox
# Program is distributed under the terms of the
# GNU General Public License see ./License for more information.

# Python 3 compatibility
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from builtins import (
         bytes, dict, int, list, object, range, str,
         ascii, chr, hex, input, next, oct, open,
         pow, round, super,
         filter, map, zip)
# #######################
import sys
import xylib
import os
import numpy as np
import re
import csv


def get_samplenames(datafile):
    # need error catcher for wrong format sample names
    sampnames = []
    for m in re.finditer('c\d{3}_\d{2}-\d{2}', datafile):
        start = int(datafile[m.end()-5:m.end()-3])
        end = int(datafile[m.end()-2:m.end()])
        for i in range(start, end+1):
            name = datafile[m.start():m.start()+5] + "%02d" % i
            sampnames.append(name)
    return sampnames


def importfile(datafile, savefile):

    d = xylib.load_file(bytes(datafile, 'utf8'), bytes("bruker_raw", 'utf8'))

    """
    for i in range(0, d.meta.size()):
        key = d.meta.get_key(i)
        value = d.meta.get(key)
        print(key, value)
    """

    # Get MetaData
    meta = []
    keys = [b'ALPHA1', b'MEASURE_DATE']
    for key in keys:
        meta.append(key + ': ' + d.meta.get(key))


    start = 0
    table = []

    ### need to do check vs sample names
    nb = d.get_block_count()
    samplenames = get_samplenames(datafile)

    for i in range(0, nb):
        block = d.get_block(i)
        """
        print("blocknm:", block.get_name())
        print("blockmeta:", block.meta)
        for i in range(0, block.meta.size()):
            key = block.meta.get_key(i)
            value = block.meta.get(key)
            print(key, value)
        """
        # get more meta data from first block
        if start == 0:
            keys = [b'GENERATOR_CURRENT', b'GENERATOR_VOLTAGE', b'STEP_SIZE']
            deg_min = (float(block.meta.get(b'STEP_SIZE'))/
                       float(block.meta.get(b'TIME_PER_STEP'))*60*191)
            # print(deg_min)
            for key in keys:
                meta.append(key + ': ' + block.meta.get(key))

        nrow = block.get_point_count()
        for j in range(nrow):
            if start == 0:
                table.append([float(block.get_column(1).get_value(j)),
                             float(block.get_column(2).get_value(j))])
            else:
                table[j].append(float(block.get_column(2).get_value(j)))
        start = 1


    header = ['Bruker XRD'] + meta + ['DEG_PER_MIN: ' + str(deg_min)]
    header2 = ['angle'] + samplenames
    table.insert(0, header2)
    table.insert(0, header)
    with open(savefile +'.csv', 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(table)
    return [savefile]

if __name__ == '__main__':
    exfiles = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
                                           os.pardir, 'examplefiles'))
    #list_supported_formats()
    #print_filetype_info("bruker_raw")
    datafile = os.path.join(exfiles, "XRD_BBT_c016_13-18.raw")
    savefile = "test"
    table = importfile(datafile, savefile)
