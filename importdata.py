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
import os
import numpy as np
from PyQt4 import QtGui
import csv
from importFromUri import importFromURI



def run(files):
    """step through files and do anlysis
    """
    with open('supported_datafiles.txt','r') as dest_f:
        # add to db in future??
        data_iter = csv.reader(dest_f, delimiter = b'\t')
        supported_datafiles = [data for data in data_iter]

    if files is None or files == []:
        files = get_datafiles(supported_datafiles)

    for datafile in files:
        datafile = str(datafile)
        script = get_analysis_script(datafile, supported_datafiles)


        do_analysis(datafile, script)

def get_datafiles(supported_datafiles):
    """Qt file dialogue widget
    """
    types = ' '.join([row[0] for row in supported_datafiles])
    filetypes = 'Supported (' + types + ')'
    app = QtGui.QApplication(sys.argv)
    widget = QtGui.QWidget()
    files = QtGui.QFileDialog.getOpenFileNames(widget,
                                               'Program to run', '',
                                               filetypes +
                                               ';;All files (*.*)',
                                               None,
                                               QtGui.QFileDialog.DontUseNativeDialog)
    return files

def get_analysis_script(datafile, supported_datafiles):
    name, extension = os.path.splitext(datafile)
    for row in supported_datafiles:
        if extension in row[0]:
            if 'None' in row[1] or row[1] is None or row[1] == '':
                script = row[2]
                break
            else:
                with open(datafile,'r') as check_f:
                    if row[1] in check_f.readline():
                        script = row[2]
                        break
    else:
        script = None
        print('no such file supported')
        # Add functionality to add new scripts
    return script


def do_analysis(datafile, script, savefile=None):
    """holding space for future"""
    if savefile is None:
        savefile = datafile[:-4]
    if script is not None:
        print('Running:', script)
        mod = importFromURI(os.path.join('scripts', script))
        savefiles = mod.importfile(datafile, savefile)
        # use savefiles to add to db


if __name__ == '__main__':
    run(sys.argv[1:])

