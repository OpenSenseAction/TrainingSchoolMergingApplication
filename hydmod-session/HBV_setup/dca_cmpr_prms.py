# -*- coding: utf-8 -*-

'''
@author: Faizan-TU Munich

Jan 01, 2024

06:04:47 PM

Instructions:
This script compares model parameters of two or more catchments.
'''

import os
import sys
import time
import timeit
import traceback as tb
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from adjustText import adjust_text

DEBUG_FLAG = False


def main():

    # The location where the model parameters are saved. These are ouputs of
    # script: daa_optimize.
    main_dir = Path(
        r'/home/seidel/Uni/HBV_Faizan/optimization_results_validation')

    os.chdir(main_dir)

    # Bounds for all parameters.
    # First one is lower, second is upper.
    # These should be the same as those in daa_optimize.
    # Bounds for each parameter are normed between 0 and 1, so that they are
    # on the same scale.
    prms_buds_dict = {
        'snw_dth': (0.00, 1e+2),
        'snw_ast': (-1.0, +1.0),
        'snw_amt': (-0.0, +2.0),
        'snw_amf': (0.00, 2.00),
        'snw_pmf': (0.00, 2.00),

        'sl0_mse': (0.00, 1e+2),
        'sl1_mse': (0.00, 2e+2),

        'sl0_fcy': (0.00, 2e+2),
        'sl0_bt0': (0.00, 3.00),

        'sl1_pwp': (0.00, 4e+2),
        'sl1_fcy': (0.00, 4e+2),
        'sl1_bt0': (0.00, 4.00),

        'urr_dth': (0.00, 2e+1),
        'lrr_dth': (0.00, 5.00),

        'urr_rsr': (0.00, 1.00),
        'urr_tdh': (0.00, 1e+2),
        'urr_tdr': (0.00, 1.00),
        'urr_cst': (0.00, 1.00),
        'urr_dro': (0.00, 1.00),
        'urr_ulc': (0.00, 1.00),

        'lrr_tdh': (0.00, 1e+4),
        'lrr_cst': (0.00, 1.00),
        'lrr_dro': (0.00, 1.00),
        }

    # Path to the calibrated model parameter files.
    # Change the labels of the catchments only.
    paths_to_prms = (
        Path(r'prms_3470_sr.csv'),
        #Path(r'prms_3465_sr.csv'),
        )

    # Choose names for the respective parameter files to be displayed on the
    # plot.
    prms_labels = ('3470')#, '3465')
    #==========================================================================

    prms_dict = {}

    prms_bounds = np.array(
        [prms_buds_dict[prm] for prm in prms_buds_dict])

    for prm_label, path_to_prms in zip(prms_labels, paths_to_prms):

        prms_df = pd.read_csv(path_to_prms, sep=';', index_col=0)

        prms_df = prms_df.iloc[:, 0]

        prms_sr = prms_df.loc[list(prms_buds_dict.keys())]

        prms_dict[prm_label] = prms_sr.values

    plot_prms_hbv(
        prms_dict, prms_bounds, list(prms_buds_dict.keys()))

    plt.show()

    plt.close()
    return


def plot_prms_hbv(prms_dict, prms_bds, hbv_prms_labs):

    n_splits = len(prms_dict)

    ax_stts = plt.subplot2grid((15, 1), (0, 0), 2, 1)

    ax_prms = plt.subplot2grid((15, 1), (3, 0), 11, 1, sharex=ax_stts)
    #======================================================================

    [ax_stts.text(
        i,
        j,
        f'{prms_bds[i, j]:0.3f}'.rstrip('0').rstrip('.'),
        va='center',
        ha='center',
        rotation=80)
     for j in range(prms_bds.shape[1])
     for i in range(prms_bds.shape[0])]

    ax_stts.set_yticks(np.arange(2))
    ax_stts.set_yticklabels(['Lower', 'Upper'])

    # ax_stts.set_xticklabels([])

    ax_stts.spines['bottom'].set_visible(False)
    ax_stts.spines['top'].set_visible(False)
    ax_stts.spines['right'].set_visible(False)

    ax_stts.tick_params(
        labelleft=True,
        labelbottom=False,
        labeltop=False,
        labelright=False)

    ax_stts.xaxis.set_ticks_position('none')
    #======================================================================

    bds_diffs = prms_bds[:, 1] - prms_bds[:, 0]

    bds_lock_idxs = np.isclose(prms_bds[:, 1], prms_bds[:, 0])

    bds_diffs[bds_lock_idxs] = np.inf

    plt_texts = []
    for ca_lab in prms_dict:

        prms_norm = (prms_dict[ca_lab] - prms_bds[:, 0]) / bds_diffs

        prms_norm[bds_lock_idxs] = 0.5

        ax_prms.plot(
            prms_norm,
            alpha=0.8,
            # lw=self._ga__ps.lws[1],
            label=f'{ca_lab}')

        prms_norm = (prms_dict[ca_lab] - prms_bds[:, 0]) / bds_diffs

        prms_norm[bds_lock_idxs] = 0.5

        continue

        if n_splits > 6:
            continue

        for j in range(prms_bds.shape[0]):

            if bds_lock_idxs[j]:
                continue

            prms_val_str = (
                f'{prms_dict[ca_lab][j]:0.4f}').rstrip('0').rstrip('.')

            text = ax_prms.text(
                j,
                prms_norm[j],
                prms_val_str,
                va='top',
                ha='left')
            plt_texts.append(text)

    if plt_texts:
        adjust_text(plt_texts, only_move={'points': 'y', 'text': 'y'})

    ax_prms.set_xlabel('Parameter [-]')
    ax_prms.set_ylabel('Normalized value [-]')

    ax_prms.set_xticks(np.arange(len(hbv_prms_labs)))
    ax_prms.set_xticklabels(hbv_prms_labs, rotation=90)

    ax_prms.set_ylim(-0.1, +1.1)

    ax_prms.grid()
    ax_prms.set_axisbelow(True)

    ax_prms.legend()
    #======================================================================
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
