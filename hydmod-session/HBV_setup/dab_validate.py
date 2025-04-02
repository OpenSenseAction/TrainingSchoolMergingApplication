# -*- coding: utf-8 -*-

'''
@author: Faizan-TU Munich

Jan 01, 2024

06:03:54 PM

Instructions:
This scripts uses the results of daa_optimize.py and simulates another time
series with it.
'''

import os
import sys
import time
import timeit
import traceback as tb
from pathlib import Path

import numpy as np
import pandas as pd

#from HBV.daily.HBV_setup.hmg import HBV1D012A
from HBV_setup.hmg import HBV1D012A

from HBV_setup.ba_effs_nans import HMG3DModelEffsNaNs as HMG3DModelEffs
#from HBV.daily.HBV_setup.ba_effs_nans import HMG3DModelEffsNaNs as HMG3DModelEffs

DEBUG_FLAG = False

def main(prms_sr, inp_dfe, cat_area, secs_per_step = 86400, output_dir=r'HBV/daily/validation_hbv_daily', cat_label = '10420'):
#def main():

    # The location where all the inputs lie and where all outputs will be
    # saved.
    #main_dir = Path(
    #    r'/home/seidel/Nextcloud/OPENSENSE/2025_Training_School/HydMod')

    # Label of the catchment for which to run the simulation.
    # cat_label = '10420'

    # Path to the input data time series, relative to main_dir.
    # hbv_inps_ts_path = Path(
    #     rf'HBV/daily/inputs/altenahr/daily_2011_2025/daily_input_data_{cat_label}.csv')

    # Path to the file that holds the surface area of catchments.
    # cats_areas_path = Path(
    #     r'HBV/daily/inputs/altenahr/daily_2011_2025/cat_areas.csv')

    

    # Number of seconds per time step.
    # secs_per_step = 86400  # Daily time step.

    # Initial conditions in the validation period are unknown and hence,
    # a period needs to be specified.
    warmup_steps = 365

    # The directory where all the outputs will be saved.
    ot_dir = Path(output_dir)
    #==========================================================================

    ot_dir.mkdir(exist_ok=True)

    cat_label = str(cat_label)

    # cat_area_sr = pd.read_csv(cats_areas_path, sep=';', index_col=0).iloc[:, 0]
    # cat_area_sr.index = [str(cat_label) for cat_label in cat_area_sr.index]

    # ccaa = cat_area_sr.loc[cat_label]

    # dslr = ccaa / (1000 * secs_per_step)
    dslr = cat_area / (1000 * secs_per_step)

    # inp_dfe = pd.read_csv(hbv_inps_ts_path, sep=';', index_col=0)

    # inp_dfe = inp_dfe.astype(dtype=np.float32)

    # Discharge is allowed to have missing values.
    assert np.all(
        np.isfinite(inp_dfe.loc[:, ['ppt', 'tem', 'pet']].values))

    assert np.all(inp_dfe.loc[:, 'dis_ref'].values >= 0)

    tems = inp_dfe.loc[:, 'tem'].values
    ppts = inp_dfe.loc[:, 'ppt'].values
    pets = inp_dfe.loc[:, 'pet'].values
    diso = inp_dfe.loc[:, 'dis_ref'].values

    modl_objt = HBV1D012A()

    modl_objt.set_inputs(tems, ppts, pets)
    modl_objt.set_outputs(tems.size)

    modl_objt.set_discharge_scaler(dslr)
    #======================================================================

    optn_args = OPTNARGS()

    optn_args.cntr = 0
    optn_args.oflg = 0
    optn_args.vbse = False
    optn_args.modl_objt = modl_objt
    optn_args.take_idxs = np.isfinite(diso)

    otps_lbls = modl_objt.get_output_labels()

    modl_objt.set_optimization_flag(0)

    modl_objt.set_parameters(prms_sr.values)

    _tbeg = timeit.default_timer()

    # Model run with optimized parameters.
    modl_objt.run_model()

    _tend = timeit.default_timer()

    sim_time = (_tend - _tbeg)

    print(f'\tFinal call to model time: {sim_time:0.3E} secs')
    print('')
    #======================================================================

    otps = modl_objt.get_outputs()
    diss = modl_objt.get_discharge()

    # Save data and model parameters.
    sim_otps_df = pd.DataFrame(
        columns=otps_lbls,
        data=otps,
        index=inp_dfe.index,
        dtype=np.float32)

    # Reference and simulated discharge.
    sim_dis_df = pd.DataFrame(
        index=inp_dfe.index,
        data={'ref':diso, 'sim':diss},
        dtype=np.float32)

    HMG3DModelEffs._cmpt_effs_flag = True

    # Do all efficiency measures one time.
    effs_cls = HMG3DModelEffs(
        diso[warmup_steps:, None],
        True,
        True,
        True,
        True,
        True,
        False,
        False)

    effs_cls.set_sim(diss[warmup_steps:, None], None)

    obj_val, effs_dict = get_obj_val_effs2(
        diss[warmup_steps:, None], effs_cls)

    # Model performance metrics.
    prf_sr = pd.Series(
        index=['OBJ'], data=[obj_val], dtype=np.float64)

    for eff_lab in effs_dict:
        prf_sr[eff_lab.upper()] = effs_dict[eff_lab][0]
    #==========================================================================

    # Save all as text. These can be viewed in MS Excel.
    sim_otps_df.to_csv(
        ot_dir / f'sim_{cat_label}_otps_df.csv',
        sep=';',
        float_format='%0.6f')

    sim_dis_df.to_csv(
        ot_dir / f'dis_sim_{cat_label}_df.csv',
        sep=';',
        float_format='%0.1f')

    prms_sr.to_csv(
        ot_dir / f'prms_{cat_label}_sr.csv',
        sep=';',
        float_format='%0.6f')

    prf_sr.to_csv(
        ot_dir / f'prf_{cat_label}_sr.csv',
        sep=';',
        float_format='%0.6f')
    return


def get_obj_val_effs2(dis_sims, effs_cls):

    effs_cls.set_sim(dis_sims, None)

    effs_dict = effs_cls.get_all_dict()

    obj_val = 0.0
    for i in range(1):

        if effs_cls.ns_flag:

            nse = effs_dict['ns'][i]

            obj_val += (1 - nse)
        #======================================================================

        if effs_cls.lns_flag:
            lnse = effs_dict['lns'][i]

            # if args.oflg and (not np.isfinite(lnse)):
            if not np.isfinite(lnse):
                lnse = -(2 + np.random.random()) * 10

            obj_val += (1 - lnse)
        #======================================================================

        if effs_cls.kg_flag:

            kge = effs_dict['kg'][i]

            obj_val += (1 - kge)
        #======================================================================

        if effs_cls.pc_flag:

            pce = effs_dict['pc'][i]

            obj_val += (1 - pce)
        #======================================================================

        if effs_cls.sc_flag:

            sce = effs_dict['sc'][i]

            obj_val += (1 - sce)
        #======================================================================

    assert np.isfinite(obj_val), obj_val

    return obj_val, effs_dict


class OPTNARGS: pass


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
