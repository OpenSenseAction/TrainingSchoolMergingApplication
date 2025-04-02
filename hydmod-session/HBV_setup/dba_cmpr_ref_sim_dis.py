# -*- coding: utf-8 -*-

'''
@author: Faizan-TU Munich

Jan 01, 2024

06:04:35 PM

Instructions:
This script compares the observed and simulated discharge values for a given
case.
'''

import os
import sys
import time
import timeit
import traceback as tb
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt

DEBUG_FLAG = False

path='/home/seidel/Nextcloud/OPENSENSE/2025_Training_School/HydMod'
def main(main_dir=path, beg_time='2015-01-01', end_time='2022-01-01'):

    # The location where all the inputs lie. These could be the outputs of the
    # scripts daa_optimize.py, and dab_validate.
    #main_dir = Path(
   #     r'/home/seidel/Nextcloud/OPENSENSE/2025_Training_School/HydMod/HBV/daily/optimization_results_validation_2011_2025')

    #os.chdir(main_dir)

    # Path to the file that holds the observed and simulated discharges.
    # You need to change the label in the name e.g., 3465, 3470 etc.
    path_to_ref_sim_dis = Path(r'HBV/daily/validation_hbv_daily/dis_sim_10420_df.csv')

    # The time period for which to plot the time series. The format is:
    # Year-Month-Day.
    #beg_time = '2015-01-01'
    #end_time = '2020-01-01' 
    #==========================================================================

    dis_df = pd.read_csv(path_to_ref_sim_dis, sep=';', index_col=0)
    dis_df.index = pd.to_datetime(dis_df.index, format='%Y-%m-%d')

    dis_df = dis_df.loc[beg_time:end_time,:]

    plt.plot(dis_df.index, dis_df['ref'].values, label='REF', alpha=0.8)
    plt.plot(dis_df.index, dis_df['sim'].values, label='SIM', alpha=0.8)

    plt.xlabel('Time [day]')
    plt.ylabel('Discharge [m$^3$.s$^{-1}$]')

    plt.grid()
    plt.gca().set_axisbelow(True)

    plt.legend()

    plt.show()

    plt.close()
    return


if __name__ == '__main__':
    print('#### Started on %s ####\n' % time.asctime())
    START = timeit.default_timer()

    #==========================================================================
    # When in post_mortem:
    # 1. "where" to show the stack,
    # 2. "up" move the stack up to an older frame,
    # 3. "down" move the stack down to a newer frame, and
    # 4. "interact" start an interactive interpreter.
    #==========================================================================

    if DEBUG_FLAG:
        try:
            main()

        except:
            pre_stack = tb.format_stack()[:-1]

            err_tb = list(tb.TracebackException(*sys.exc_info()).format())

            lines = [err_tb[0]] + pre_stack + err_tb[2:]

            for line in lines:
                print(line, file=sys.stderr, end='')

            import pdb
            pdb.post_mortem()
    else:
        main()

    STOP = timeit.default_timer()
    print(('\n#### Done with everything on %s.\nTotal run time was'
           ' about %0.4f seconds ####' % (time.asctime(), STOP - START)))
