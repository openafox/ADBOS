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


import gtk
import pygtk
import sys
import numpy as np
from PyQt4 import QtCore, QtGui
import csv
import gwy
import matplotlib.pyplot as plt


def get_ids(container):
    idss = gwy.gwy_app_data_browser_get_data_ids(container)
    # print(idss)
    for i in idss:
       print(gwy.gwy_app_get_data_field_title(container, idss[i]))


def importfile(datafile, savefile):
    """doc string
    """
    container = gwy.gwy_file_load(datafile, gwy.RUN_NONINTERACTIVE)
    gwy.gwy_app_data_browser_add(container)
    # Find 'Height'channele.
    ids = gwy.gwy_app_data_browser_find_data_by_title(container, 'Height*')
    #print("IDS: ", ids)
    if len(ids) == 1:  # if we found "Height"
        i = ids[0]
        # Select the channel and run some functions.
        gwy.gwy_app_data_browser_select_data_field(container, i)
        #gwy.gwy_process_func_run('align_rows', container, gwy.RUN_IMMEDIATE)
        #gwy.gwy_process_func_run('flatten_base', container, gwy.RUN_IMMEDIATE)
        key = gwy.gwy_app_get_data_key_for_id(i)
        field = container[gwy.gwy_name_from_key(key)]  # key works 2

        ## fix Zero
        field.add(-field.get_min())

        ## Set color range
        container.set_string_by_name("/%s/base/palette" % i, "Halcyon")

        #container.set_int32_by_name("/%s/base/range-type" % i,
        #        int(gwy.LAYER_BASIC_RANGE_AUTO))
        Min, Max = field.get_autorange()
        # print('min,max', Min, '  ', Max)
        maxi = round(Max  * 1e9- Min * 1e9) * 1e-9
        # print(maxi)
        container.set_int32_by_name("/%s/base/range-type" % i,
                int(gwy.LAYER_BASIC_RANGE_FIXED))
        container.set_double_by_name("/%s/base/min" % i, 0)
        container.set_double_by_name("/%s/base/max" % i, maxi)

        ## Save the file as a .png
        # get units
        size = str(round(field.get_xreal() * 10**6))
        name = savefile[:-4] + "_" + size + "um"
        pngname = name + ".png"
        #gwy.gwy_app_data_browser_select_data_field(container, 0)
        gwy.gwy_file_save(container, pngname, gwy.RUN_NONINTERACTIVE)

        ## Extract rms and rms of 3sigma masked
        avg, ra, rms, skew, kurtosis = field.get_stats()
        print('pure %s\t%g' % (name, rms))
        # Set Mask
        mask = field.new_alike(False)
        field.mask_outliers(mask, 3)
        container.set_object_by_name("/%d/mask" % i, mask)
        yres = int(field.get_yres())
        xres = int(field.get_xres())
        avg2, ra2, rms2, skew2, kurtosis2 = (
                        field.area_get_stats_mask(mask,
                            gwy.MASK_EXCLUDE, 0, 0, xres, yres)
                        )
        print('mask %s\t%g' % (name, rms2))
        # Save RMS data to csv
        txtname = savefile[:-6] + "rms.csv"
        with open(txtname, "ab") as f:
            writer = csv.writer(f)
            writer.writerow([name[-11:], rms, rms2])



    ## Create a distribution of heights (y)
    line = gwy.DataLine(1, 1, False)
    field.dh(line, 128)
    # storage line, number of samples to take on the distribution function
    valuesY = np.asarray(line.get_data())

    ## Calcule X data
    xMin = line.get_offset()
    xStep = line.get_real()/128 # len of line / number of points
    valuesX = np.asarray([(xMin+i*xStep)*1e9 for i in range(len(valuesY))])

    # Save to csv
    csvname = name + ".csv"
    with open(csvname, "wb") as f:
        writer = csv.writer(f)
        writer.writerow(["Height [nm]", "Density [nm-1]"])
        writer.writerows(zip(valuesX, valuesY/1e9))

    ## Save distribution of heights as .txt
    #file = open ( os.path.splitext(filename)[0] +"_dh_c"+ str(polynom) + "_" + str(colorRangeMin*1000000000) + "_" + str(colorRangeMax*1000000000) + ".txt", "w")
    #file.write(dh)
    #file.close()

    """
    ## Plot
    ax = plt.subplot2grid((1,1),(0,0))
    ax.plot(valuesX, valuesY)
    ax.set_xlabel('counts')
    ax.set_ylabel('density')
    plt.show()
    """

    return ([pngname, txtname, csvname])

if __name__ == '__main__':
    # test(sys.argv[1:])
    importfile("/Users/towel/Desktop/Test/AFM_BBT_c015_230002.ibw", "/Users/towel/Desktop/Test/AFM_BBT_c015_230003")
    pass
