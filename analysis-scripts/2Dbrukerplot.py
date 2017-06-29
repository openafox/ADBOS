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

import sys, os
import numpy as np
import struct
import Tkinter, Tkconstants, tkFileDialog
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.figure import Figure
from matplotlib.colors import LogNorm
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
import matplotlib.patheffects as path_effects

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import sys
if sys.version_info[0] < 3:
    import Tkinter as Tk
else:
    import tkinter as Tk

# https://docs.python.org/2/library/struct.html
# https://github.com/wojdyr/xylib/blob/master/xylib/bruker_raw.cpp

head = {
            'version':       [None, 'Version',                     4,   0],
            'head_1':        [None, 'head 1',                      4,   4],
            'file_status':   [None, 'File Status',              '<I',   8],
            'range_cnt':     [None, 'Range Count',              '<I',  12],
            'm_date':        [None, 'Measure Date',               10,  16],
            'm_time':        [None, 'Measure Time',               10,  26],
            'user':          [None, 'User',                       72,  36],
            'site':          [None, 'Site',                      218, 108],
            'sample_id':     [None, 'Sample ID',                  60, 326],
            'comment':       [None, 'Comment',                   160, 386],
            'head_2':        [None, 'head 2',                      2, 546],
            'c_goni':        [None, 'Goniometer Model',         '<I', 548],
            'c_goni_s':      [None, 'Goniometer Stage',         '<I', 552],
            'c_samp_l':      [None, 'Sample Changer',           '<I', 556],
            'c_goni_c':      [None, 'Goniometer Controler',     '<I', 560],
            'c_goni_r':      [None, '(R4) goniometer radius',   '<f', 564],
            'fix_divr':      [None, '(R4) fixed divergence',    '<f', 568],
            'fix_samp':      [None, '(R4) fixed sample slit',   '<f', 572],
            'prim_ss':       [None, 'primary Soller slit',      '<I', 576],
            'prim_mon':      [None, 'primary monochromator',    '<I', 580],
            'fix_anti':      [None, '(R4) fixed antiscatter',   '<f', 584],
            'fix_detc':      [None, '(R4) fixed detector slit', '<f', 588],
            'sec_ss':        [None, 'secondary Soller slit',    '<f', 592],
            'fix_tf':        [None, 'fixed thin film attach',   '<I', 596],
            'beta_f':        [None, 'beta filter',                 4, 600],
            'sec_mon':       [None, 'secondary monochromator',  '<f', 604],
            'anode':         [None, 'Anode Material',              4, 608],
            'head_3':        [None, 'head 3',                      4, 612],
            'alpha_ave':     [None, 'Alpha Average',            '<d', 616],
            'alpha_1':       [None, 'Alpha 1',                  '<d', 624],
            'alpha_2':       [None, 'Alpha 2',                  '<d', 632],
            'beta':          [None, 'Beta',                     '<d', 640],
            'alpha_ratio':   [None, 'Alpha_ratio',              '<d', 648],
            'unit_nm':       [None, '(C4) Unit Name',              4, 656],
            'int_beta_a1':   [None, 'Intensity Beta:a1',           4, 660],
            'mea_time':      [None, 'Measurement Time',         '<f', 664],
            'head_4':        [None, 'head 4',                     43, 668],
            'hard_dep':      [None, 'hard_dep',                    1, 711],
        }

block = {
            'header_len':    [None, 'Header Len',               '<I',   0],
            'steps':         [None, 'Steps',                    '<I',   4],
            'start_theta':   [None, 'Start Theta',              '<d',   8],
            'start_2th':     [0,    'Start 2Theta',             '<d',  16],
            'drive_chi':     [0,    'Chi Start',                '<d',  24],
            'drive_phi':     [None, 'Phi Start',                '<d',  32],
            'drive_x':       [None, 'X Start',                  '<d',  40],
            'drive_y':       [None, 'Y Start',                  '<d',  48],
            'drive_z':       [None, 'Z Start',                  '<d',  56],
            'ig_1':          [None, 'ig 1',                     '<Q',  64],
            'ig_2':          [None, 'ig 2',                        6,  72],
            'ig_2_1':        [None, 'ig 2_1',                   '<h',  78],
            'R8':            [None, '(R8) variable anitscat',   '<d',  80],
            'ig_3':          [None, 'ig 3',                        6,  88],
            'ig_3_1':        [None, 'ig 3_1',                   '<h',  94],
            'dec_code':      [None, 'Detector',                 '<I',  96],
            'hv':            [None, 'High Voltage',             '<f', 100],
            'amp_gain':      [None, 'Ampliphier Gain',          '<f', 104],
            'dis1_LL':       [None, 'Discriminator1 Lower Lev', '<f', 112],
            'ig_4':          [None, 'ig 4',                     '<I', 116],
            'ig_5':          [None, 'ig 5',                     '<d', 120],
            'ig_6':          [None, 'ig 6',                     '<f', 128],
            'ig_a':          [None, 'ig a',                     '<f', 132],
            'ig_b':          [None, 'ig b',                        5, 136],
            'ig_b_1':        [None, 'ig b_1',                      3, 141],
            'ig_c':          [None, 'Aux Axis 1 start',         '<d', 144],
            'ig_d':          [None, 'Aux Axis 2 start',         '<d', 152],
            'ig_e':          [None, 'Aux Axis 3 start',         '<d', 160],
            'ig_f':          [None, 'Scan Mode',                   4, 168],
            'ig_g':          [None, 'ig g',                     '<I', 172],
            'ig_h':          [None, 'ig h',                     '<I', 172],
            'step_size':     [None, 'Step Size',                '<d', 176],
            'ig_i':          [None, 'ig i',                     '<d', 184],
            'step_time':     [None, 'Time Per Step',            '<f', 192],
            'ig_j':          [None, 'Scan Type',                '<I', 196],
            'ig_k':          [None, 'Delay Time',               '<f', 200],
            'ig_l':          [None, 'ig l',                     '<I', 204],
            'rot_speed':     [None, 'Rotation Speed',           '<f', 208],
            'ig_m':          [None, 'ig m',                     '<f', 212],
            'ig_n':          [None, 'ig n',                     '<I', 216],
            'ig_o':          [None, 'ig o',                     '<I', 220],
            'gen_v':         [None, 'Generator Voltage',        '<I', 224],
            'gen_a':         [None, 'Generator Current',        '<I', 228],
            'ig_p':          [None, 'ig p',                     '<I', 232],
            'ig_q':          [None, 'ig q',                     '<I', 236],
            'lambda':        [None, 'Lambda',                   '<d', 240],
            'ig_r':          [None, 'ig r',                     '<I', 248],
            'ig_s':          [None, 'Len of each data in bits', '<I', 252],
            'sup_len':       [None, 'supplementary header len', '<I', 256],
            'ig_t':          [None, 'ig t',                     '<I', 260],
            'ig_u':          [None, 'ig u',                     '<I', 264],
            'ig_v':          [None, 'ig v',                     '<I', 268],
            'ig_w':          [None, 'ig w',                     '<I', 272],
            'ig_x':          [None, 'Reserved for expansion',   '<I', 280],
        }




supp = {
            's_1':          [None, 'Record type',               '<I',   0],
            's_2':          [None, 'record length',             '<I',   4],
            's_3':          [None, 'reserved',                  '<I',   8],
            's_5':          [None, 'integration range start',   '<f',  16],
            's_6':          [None, 'integration range end',     '<f',  20],
            'chi_start':    [None, 'int range chi start',       '<f',  24],
            'chi_end':      [None, 'int range chi end',         '<f',  28],
            's_9':          [None, 'norm method',               '<I',  32],
            's_10':         [None, 'prog name',                   20,  36],
            'act_2th':      [None, 'act 2th',                   '<f',  56],
            'act_omega':    [None, 'act omega',                 '<f',  60],
            'act_phi':      [None, 'act phi',                   '<f',  64],
            'act_psi':      [None, 'act psi',                   '<f',  68],
        }

def get_datafiles(supported_datafiles, location):
    root = Tkinter.Tk()
    types = ' '.join([row[0] for row in supported_datafiles])
    filetypes = ('Supported', types )
    root.update()
    files = tkFileDialog.askopenfilenames(initialdir = location,
            title = "Select file",
            filetypes = (filetypes, ("all files","*.*")))

    root.destroy()
    return files

def get_smap_table(filename):
    with open(filename, mode='rb') as f: # b is important -> binary
        fileContent = f.read()
    header = get_metta(fileContent, head, 0)
    data = []
    y_pos = 712
    y = []
    while True:
        metta = get_metta(fileContent, block, y_pos)
        h_len = metta['header_len'][0]
        #print(metta['header_len'][1], hl)
        supmetta = get_metta(fileContent, supp, y_pos + h_len)
        s_len = metta['sup_len'][0]
        #print(metta['sup_len'][1], sl)
        y_start = y_pos+h_len+s_len
        data_len = metta['steps'][0]
        y_pos = y_start + data_len * 4
        y_data = []
        for i in range(data_len):
            (ret,) = struct.unpack('<f', fileContent[y_start+i*4: y_start+i*4+4])
            y_data.append(ret)
        #print(y_data)
        data.append(y_data)
        """
        print(supmetta['chi_start'][1] + ':', supmetta['chi_start'][0])
        print(supmetta['chi_end'][1] + ':', supmetta['chi_end'][0])
        print(supmetta['act_chi'][1] + ':', supmetta['act_chi'][0])
        print(supmetta['act_omega'][1] + ':', supmetta['act_omega'][0])
        print(supmetta['act_phi'][1] + ':', supmetta['act_phi'][0])
        print(supmetta['act_2th'][1] + ':', supmetta['act_2th'][0])
        print('data len', len(data))
        print('range_cnt', head['range_cnt'][0])
        """
        y.append(90 - int(supmetta['act_psi'][0]))
        if len(data) >= int(head['range_cnt'][0]):
            break

    twoth_0 = metta['start_2th'][0]
    twoth_s = metta['step_size'][0]
    twoth_e = twoth_0 + twoth_s*metta['steps'][0]

    x = np.arange(twoth_0,twoth_e, twoth_s)
    y = np.arange(min(y), max(y)+1, 1)
    data = np.asarray(data)
    return x, y, data


def plot_heatmap(x, y, data, name):
    # colors
    # https://matplotlib.org/users/colormaps.html
    # https://matplotlib.org/api/_as_gen/matplotlib.axes.Axes.pcolor.html
    axlables = {'family': 'serif',
            'color':  'black',
            'weight': 'normal',
            'size': 14,
            }
    titles = {'family': 'serif',
            'color':  'black',
            'weight': 'normal',
            'size': 16,
            }
    lables = {'family': 'serif',
            'fontname':'DejaVu Serif',
            'color':  '#66ff33',
            'weight': 'normal',
            'size': 12,
            'verticalalignment': 'center',
            'horizontalalignment': 'right',
            }

    fig = Figure(figsize=(12,6), dpi=100)
    ax = fig.add_subplot(111)
    plt = ax.pcolormesh(x, y, data, vmin=data.min()+5, vmax=1e3, #data.max(),
               cmap='viridis') #alpha=0.8)
    #plt.pcolor(x, y, data, norm=LogNorm(vmin=data.min()+5, vmax= 1e3),# data.max()),
    #           cmap='viridis') #alpha=0.8)
    ax.set_xlabel('2\u03b8[\u00b0]', fontdict=titles)
    ax.set_ylabel(u'\u03A8[\u00b0]', fontdict=titles)
    fig.colorbar(plt)
    # figure out later
    #plt.tick_params(fontdict=axlables)
    peaks = [[22.842, 0, '100'],
             [32.525, 0, '110'],
             [32.525, 45, '110\u2081\u2080\u2080'],
             #[40.117, 0, '111'],
             [40.117, 54.74, '111\u2081\u2080\u2080'],
             [46.662, 0, '200'],
             #[52.564, 0, '210'],
             #[58.031, 0, '211'],
             [58.031, 35.26, '211\u2081\u2080\u2080'],
             [58.031, 65.91, '121\u2081\u2080\u2080'],
             #[68.124, 0, '220'],
             [68.124, 45, '220\u2081\u2080\u2080'],
             #[72.891, 0, '221'],
             #[77.540, 0, '310'],
             [77.540, 18.43, '310\u2081\u2080\u2080'],
             #[82.106, 0, '311'],
             #[86.622, 0, '222'],
             #[39.764, 0, 'Pt111'],
             #[39.764, 70.53, u'Pt111\u2081\u2081\u2081'],
             #[46.244, 54.74, u'Pt200\u2081\u2081\u2081'],
             #[67.456, 35.26, u'Pt220\u2081\u2081\u2081'],
             #[81.289, 29.50, u'Pt311\u2081\u2081\u2081'],
             #[81.289, 58.52, u'Pt311\u0304\u2081\u2081\u2081'],
             #[81.289, 79.98, u'Pt31\u03041\u0304\u2081\u2081\u2081'],
             #[85.715, 0, 'Pt222'],
             #[85.715, 70.53, u'Pt222\u2081\u2081\u2081'],
             #[69.132, 00.00, u'Si400'],
             #[28.443, 54.74, u'Si111\u2084\u2080\u2080'],
             #[47.303, 45.00, u'Si220\u2084\u2080\u2080'],
             #[56.122, 25.24, u'Si311\u2084\u2080\u2080'],
             #[56.122, 72.45, u'Si131\u2084\u2080\u2080'],
             #[76.379, 46.51, u'Si331\u2084\u2080\u2080'],
             #[76.379, 76.74, u'Si133\u2084\u2080\u2080'],
             #[88.029, 35.26, u'Si422\u2084\u2080\u2080'],
             #[88.029, 65.91, u'Si242\u2084\u2080\u2080'],
             #[94.951, 15.79, u'Si511\u2084\u2080\u2080'],
             #[94.951, 78.90, u'Si151\u2084\u2080\u2080'],
             [39.764, 0, 'Pt'],
             [39.764, 70.53, u'Pt'],
             [46.244, 54.74, u'Pt'],
             [67.456, 35.26, u'Pt'],
             [81.289, 29.50, u'Pt'],
             [81.289, 58.52, u'Pt'],
             [81.289, 79.98, u'Pt'],
             [85.715, 0, 'Pt'],
             [85.715, 70.53, u'Pt'],
             [69.132, 00.00, u'Si'],
             [28.443, 54.74, u'Si'],
             [47.303, 45.00, u'Si'],
             [56.122, 25.24, u'Si'],
             [56.122, 72.45, u'Si'],
             [76.379, 46.51, u'Si'],
             [76.379, 76.74, u'Si'],
             [88.029, 35.26, u'Si'],
             [88.029, 65.91, u'Si'],
             [94.951, 15.79, u'Si'],
             [94.951, 78.90, u'Si'],
             ]
    for peak in peaks:
        txt = ax.text(peak[0], peak[1], peak[2], fontdict=lables)
        txt.set_path_effects([path_effects.Stroke(linewidth=1,
            foreground='black'), path_effects.Normal()])


    root = Tk.Tk()
    root.wm_title(name)
    # a tk.DrawingArea
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.show()
    canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

    button = Tk.Button(master=root, text='Cancel', command=sys.exit)
    button.pack(side=Tk.BOTTOM)

    button2 = Tk.Button(master=root, text='Save', command=lambda: write_png(fig))
    button2.pack(side=Tk.BOTTOM)

    Tk.mainloop()

    #result = tkMessageBox.askquestion("Delete", "Are You Sure?", icon='warning')
    #if result == 'yes':
    #    print "Deleted"
    #else:
    #    print "I'm Not Deleted Yet"

def write_png(fig):
    location = '~/_The_Universe/_Materials_Engr/_Mat_Systems/_BNT_BKT/_CSD/'
    filename = tkFileDialog.asksaveasfile(initialdir = location,
            mode='w', defaultextension=".png")
    if f is None: # asksaveasfile return `None` if dialog closed with "cancel".
        print('No File Saved')
        return
    fig.savefig(filename, bbox_inches = 'tight',
            pad_inches = 0, transparent=True)

def get_metta(fileContent, attrs, start_pos):

    keys = sorted(attrs, key=lambda key: attrs[key][3])
    for key in keys:
        #print(key)
        pos = attrs[key][3]+start_pos
        typ = attrs[key][2]
        bits = 0
        if typ == '<h' or typ == '<H':
            bits = 2
        elif typ == '<f' or typ == '<I':
            bits = 4
        elif typ == '<d' or typ == '<Q' or typ == '<q':
            bits = 8
        elif isinstance(typ, int):
            (attrs[key][0],) = struct.unpack('%ds' % typ,
                    fileContent[pos: pos+typ])
            #print(attrs[key][1] + ':', attrs[key][0])
            continue

        (attrs[key][0],) = struct.unpack(typ, fileContent[pos: pos+bits])
        #print(attrs[key][1] + ':', attrs[key][0])

    return attrs


if __name__ == '__main__':
    import script_resources

    exfiles = os.path.abspath(os.path.join(os.path.dirname( __file__ ),
                                           os.pardir, 'examplefiles'))
    datafile = os.path.join(exfiles, "2D_XRD2.raw")
    savefile = os.path.join(exfiles, "test2")
    location = '~/_The_Universe/_Materials_Engr/_Mat_Systems/_BNT_BKT/_CSD/'

    files = get_datafiles(['*.raw'], location)
    ys = None
    for i, f in enumerate(sorted(files)):
        datafile = str(f)
        x, y, data = get_smap_table(datafile)
        if np.array_equal(y, ys):
            datas = np.concatenate((datas, data), axis=1)
            xs = np.concatenate((xs, x), axis=0)
            print('data:', datas.shape)
            print('x', xs.shape)
            continue
        elif ys is not None:
            print('error')
        ys = y
        datas = data
        xs = x
    name = os.path.basename(f)

    plot_heatmap(xs, ys, datas, name)

    #files = get_datafiles(["*.raw"])
    #for datafile in files:
    #    datafile = str(datafile)
    #    table = test(datafile)

