#!/usr/bin/env python
"""Converts Diffrac V4 debug format text files (converted from raw files with
RawFileConverter) to single CSV files with one 2theta column and a series of
counts columns. Assumes all scans in file have same 2theta range and increment.

To DO:
    - Create file checker to prevent errors if wrong file is selected
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
import numpy as np
import csv


def importfile(datafile, savefile):
    """doc string
    """
    with open(datafile, 'r') as f:
        table = []
        start = 0
        online = -1
        for line in f:
            line = str(line)
            # print('line: ', line)

            if '[RangeHeader]' in line:
                # end data collection
                if online > 0:
                    start = 1
                    online = -1

            if online > -1:
                data = line.split(",")
                # print('data: ', data)
                if start == 0:
                    table.append([float(data[0]), float(data[1])])
                else:
                    # print('on line: ', online)
                    table[online].append(float(data[1]))
                online += 1
            if 'Angle' in line:
                # start data collection
                online = 0

        # print('table: ', table)

    savefile = savefile + ".csv"
    with open(savefile, 'wb') as f:
        writer = csv.writer(f)
        writer.writerows(table)

    return [savefile]

if __name__ == '__main__':
    pass
