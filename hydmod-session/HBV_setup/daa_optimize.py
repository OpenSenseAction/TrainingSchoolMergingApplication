# -*- coding: utf-8 -*-

'''
@author: Faizan-TU Munich

Jan 01, 2024

5:46:29 PM

Instructions:
This code find the optimium model parameters for given data and objective
functions.
'''

import os
import sys
import time
import timeit
import traceback as tb
from pathlib import Path
from timeit import default_timer

import numpy as np
import pandas as pd
from scipy.optimize import differential_evolution

#from daily.HBV_setup.hmg import HBV1D012A
from HBV_setup.hmg import HBV1D012A

from HBV_setup.ba_effs_nans import HMG3DModelEffsNaNs as HMG3DModelEffs
#from HBV.daily.HBV_setup.ba_effs_nans import HMG3DModelEffsNaNs as HMG3DModelEffs

DEBUG_FLAG = False


def main(prms_buds_dict, inp_dfe, cat_area, secs_per_step = 86400, output_dir=r'HBV/daily/calib_results_hbv_daily', cat_label = '10420'):

#def main():


    # The location where all the inputs lie and where all outputs will be
    # saved.
    #main_dir = Path(
    #    r'/home/seidel/Nextcloud/OPENSENSE/2025_Training_School/HydMod/HBV/daily/inputs')

    #os.chdir(main_dir)

    # Directory where the input time series lie.
    # hbv_inps_ts_dir = Path(
    #     r'HBV/daily/inputs/altenahr/daily_2001_2011')

    # Path to the file that holds the surface area of catchments.
    # cats_areas_path = Path(
    #     r'HBV/daily/inputs/altenahr/daily_2001_2011/cat_areas.csv')

    # Labels of catchments.

    # Number of seconds per time step.
    # secs_per_step = 86400  # Daily time step.

    # An optimization parameter. Leave it like this.
    pop_size = 3

    # Bounds for all parameters.
    # First one is lower, last is upper.
    # Initial values of the model are also calibrated. Hence, no warmup period.

    # Type of objective functions used to get model parameters.
    eff_ns_flag = True  # NSE.
    eff_lns_flag = False  # Ln. NSE.
    eff_kg_flag = False  # KGE.
    eff_pc_flag = False  # Pearson Corr.
    eff_sc_flag = False  # Spearman Corr.

    # The directory where all the outputs will be saved.
    ot_dir = Path(output_dir)
    #==========================================================================

    ot_dir.mkdir(exist_ok=True)

    # cat_area_sr = pd.read_csv(cats_areas_path, sep=';', index_col=0).iloc[:, 0]
    # cat_area_sr.index = [str(cat_label) for cat_label in cat_area_sr.index]
    

    # cat_labels = [str(cat_label) for cat_label in cat_labels]

    HMG3DModelEffs._cmpt_effs_flag = True

    # for cat_label in cat_labels:
        #ccaa = cat_area_sr.loc[cat_label]

        #dslr = ccaa / (1000 * secs_per_step)
    dslr = cat_area / (1000 * secs_per_step)
    
    # inp_dfe = pd.read_csv(
    #     hbv_inps_ts_dir / f'daily_input_data_{cat_label}.csv',
    #     sep=';',
    #     index_col=0)

    inp_dfe = inp_dfe.astype(dtype=np.float32)

    # Discharge is allowed to have missing values.
    assert np.all(
        np.isfinite(inp_dfe.loc[:, ['ppt', 'tem', 'pet']].values))

    assert np.all(inp_dfe.loc[:, 'dis_ref'].values >= 0)

    tems = inp_dfe.loc[:, 'tem'].values
    ppts = inp_dfe.loc[:, 'ppt'].values
    pets = inp_dfe.loc[:, 'pet'].values
    diso = inp_dfe.loc[:, 'dis_ref'].values
    #======================================================================

    modl_objt = HBV1D012A()

    prms_buds = modl_objt.get_parameter_bounds_in_correct_order(
        prms_buds_dict)

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

    optn_args.effs_cls = HMG3DModelEffs(
        diso[:, None],
        eff_ns_flag,
        eff_lns_flag,
        eff_kg_flag,
        eff_pc_flag,
        eff_sc_flag,
        False,
        False)

    modl_objt.set_optimization_flag(1)

    print('Optimizing...')

    _tbeg = default_timer()

    optn_ress = differential_evolution(
        get_objv_fntn_vlue,
        bounds=prms_buds,
        args=(optn_args,),
        popsize=pop_size,
        polish=False)

    _tend = default_timer()

    prms = optn_ress.x

    optn_args.vbse = True

    get_objv_fntn_vlue(prms, optn_args)
    #==========================================================================

    print('\tBest model parameters:')

    for prm_lbl, i in modl_objt.get_parameter_labels().items():
        print(
            f'{prm_lbl}:',
            prms_buds[i, 0],
            round(prms[i], 6),
            prms_buds[i, 1])

    print('')

    print('\tBest objective function value:', round(optn_ress.fun, 3))
    print('')

    print('\tTotal number of iterations:', optn_ress.nit)
    print('')

    print('\tTime to optimize:', f'{_tend - _tbeg:0.2f} secs')
    print('')
    #======================================================================

    modl_objt.set_optimization_flag(0)

    otps_lbls = modl_objt.get_output_labels()

    modl_objt.set_parameters(prms)

    _tbeg = default_timer()

    # Model run with optimized parameters.
    modl_objt.run_model()

    _tend = default_timer()

    sim_time = (_tend - _tbeg)

    print(f'\tFinal call to model time: {sim_time:0.3E} secs')
    print('')
    #======================================================================

    otps = modl_objt.get_outputs()
    diss = modl_objt.get_discharge()

    obj_val = get_obj_val_effs(diss[:, None], optn_args)

    # Save data and model parameters.
    sim_otps_df = pd.DataFrame(
        data=otps,
        columns=otps_lbls,
        index=inp_dfe.index,
        dtype=np.float32)

    # Reference and simulated discharge.
    sim_dis_df = pd.DataFrame(
        index=inp_dfe.index,
        data={'ref':diso, 'sim':diss},
        dtype=np.float32)

    # Model parameters.
    prms_sr = pd.Series(
        index=list(modl_objt.get_parameter_labels().keys()),
        data=prms,
        dtype=np.float32)

    # Model performance metrics.
    prf_sr = pd.Series(
        index=['OBJ'], data=[obj_val], dtype=np.float64)

    # Do all efficiency measures one time.
    effs_cls = HMG3DModelEffs(
        diso[:, None],
        True,
        True,
        True,
        True,
        True,
        False,
        False)

    effs_cls.set_sim(diss[:, None], None)

    effs_dict = effs_cls.get_all_dict()

    for eff_lab in effs_dict:
        prf_sr[eff_lab.upper()] = effs_dict[eff_lab][0]
    #======================================================================

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
    #======================================================================

    return


def get_objv_fntn_vlue(prms, args):

    modl_objt = args.modl_objt

    modl_objt.set_parameters(prms)
    modl_objt.run_model()

    diss = modl_objt.get_discharge()[args.take_idxs]

    obj_val = get_obj_val_effs(diss[:, None], args)

    return obj_val


def get_obj_val_effs(dis_sims, args):

    args.effs_cls.set_sim(dis_sims, None)

    effs_dict = args.effs_cls.get_all_dict()

    obj_val = 0.0
    for i in range(1):

        if args.effs_cls.ns_flag:

            nse = effs_dict['ns'][i]

            obj_val += (1 - nse)
        #======================================================================

        if args.effs_cls.lns_flag:
            lnse = effs_dict['lns'][i]

            # if args.oflg and (not np.isfinite(lnse)):
            if not np.isfinite(lnse):
                lnse = -(2 + np.random.random()) * 10

            obj_val += (1 - lnse)
        #======================================================================

        if args.effs_cls.kg_flag:

            kge = effs_dict['kg'][i]

            obj_val += (1 - kge)
        #======================================================================

        if args.effs_cls.pc_flag:

            pce = effs_dict['pc'][i]

            obj_val += (1 - pce)
        #======================================================================

        if args.effs_cls.sc_flag:

            sce = effs_dict['sc'][i]

            obj_val += (1 - sce)
        #======================================================================

    assert np.isfinite(obj_val), obj_val

    return obj_val


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
