'''
Created on Oct 21, 2024

@author: Faizan
'''

from math import pow as powf

import numpy as np

PINF = +np.float32(np.inf)
NINF = -np.float32(np.inf)

#==============================================================================
# Variables for the model below.
#
# Variable symbols and their meaning.
# PPT = Precipitation (any form).
# TEM = Temperature.
# PWP = Permanent wilting point.
# DIS = Discharge or runoff.
# RNF = Runoff or discharge.
# URR = Upper reservoir.
# LRR = Lower reservoir.
#
# Dimension symbols and their meanings.
# L = Length.
# T = Time.
# K = Temperature.
# - = No dimension, or a ratio only.
#==============================================================================

#==============================================================================
# Parameter indices.
#==============================================================================

# Snow.
prm_snw_dth_i = 0  # Initial depth [L].
prm_snw_ast_i = prm_snw_dth_i + 1  # Air snow TEM [K].
prm_snw_amt_i = prm_snw_ast_i + 1  # Air melt TEM [K].
prm_snw_amf_i = prm_snw_amt_i + 1  # Air melt factor [L/TK].
prm_snw_pmf_i = prm_snw_amf_i + 1  # PPT melt factor [L/LTK].

# Soils.
prm_sl0_mse_i = prm_snw_pmf_i + 1  # Soil 0 initial depth [L].
prm_sl1_mse_i = prm_sl0_mse_i + 1  # Soil 1 initial depth [L].

# Soil 0.
prm_sl0_fcy_i = prm_sl1_mse_i + 1  # Field capacity [L].
prm_sl0_bt0_i = prm_sl0_fcy_i + 1  # Beta [-].

# Soil 1.
prm_sl1_pwp_i = prm_sl0_bt0_i + 1  # PWP [L].
prm_sl1_fcy_i = prm_sl1_pwp_i + 1  # Field capacity [L].
prm_sl1_bt0_i = prm_sl1_fcy_i + 1  # Beta [-].

# Routing reservoirs.
prm_urr_dth_i = prm_sl1_bt0_i + 1  # URR initial depth [L].
prm_lrr_dth_i = prm_urr_dth_i + 1  # LRR initial depth [L].

# Upper reservoir.
prm_urr_rsr_i = prm_lrr_dth_i + 1  # Runoff split ratio [-].
prm_urr_tdh_i = prm_urr_rsr_i + 1  # Threshold depth [L].
prm_urr_tdr_i = prm_urr_tdh_i + 1  # Threshold DIS const. [1/T].
prm_urr_cst_i = prm_urr_tdr_i + 1  # RNF const. [1/T].
prm_urr_dro_i = prm_urr_cst_i + 1  # DIS ratio [-].
prm_urr_ulc_i = prm_urr_dro_i + 1  # URR-to-LRR const. [1/T].

# Lower reservoir.
prm_lrr_tdh_i = prm_urr_ulc_i + 1  # Threshold depth [L].
prm_lrr_cst_i = prm_lrr_tdh_i + 1  # Runoff const. [1/T].
prm_lrr_dro_i = prm_lrr_cst_i + 1  # Discharge ratio [-].

#==========================================================================
# Output indices.
#==========================================================================

# Snow.
out_snw_dth_i = 0  # Depth [L].
out_snw_lpt_i = out_snw_dth_i + 1  # Liquid PPT [L/T].
out_snw_aim_i = out_snw_lpt_i + 1  # Air induced melt [L/T].
out_snw_pim_i = out_snw_aim_i + 1  # PPT induced melt [L/T].
out_snw_mlt_i = out_snw_pim_i + 1  # Total melt [L/T].

# Soils.
out_sl0_mse_i = out_snw_mlt_i + 1  # Soil 0 depth [L].
out_sl1_mse_i = out_sl0_mse_i + 1  # Soil 1 depth [L].

# Soil 0.
out_sl0_prf_i = out_sl1_mse_i + 1  # Potential runoff [L/T].
out_sl0_arf_i = out_sl0_prf_i + 1  # Actual runoff [L/T].

# Soil 1.
out_sl1_etn_i = out_sl0_arf_i + 1  # Evapotranspiration [L/T].

# Routing reservoirs.
out_urr_dth_i = out_sl1_etn_i + 1  # URR depth [L].
out_lrr_dth_i = out_urr_dth_i + 1  # LRR depth [L].

# Upper reservoir.
out_urr_rnf_i = out_lrr_dth_i + 1  # Runoff [L/T].
out_urr_pln_i = out_urr_rnf_i + 1  # Percolation to lower [L/T].

# Lower reservoir.
out_lrr_rnf_i = out_urr_pln_i + 1  # RNF [L/T].

# Surface and underground Runoff.
out_rnf_sfc_i = out_lrr_rnf_i + 1  # Surface RNF [L/T].
out_rnf_gnd_i = out_rnf_sfc_i + 1  # Underground RNF [L/T].

# Mass balance.
out_mod_bal_i = out_rnf_gnd_i + 1  # Water balance [L/T].
#==============================================================================

#==============================================================================
# Functions for indices outside cython.
#==============================================================================


def get_idxs_prms_py():

    cmbs = {
        'snw_dth': prm_snw_dth_i,
        'snw_ast': prm_snw_ast_i,
        'snw_amt': prm_snw_amt_i,
        'snw_amf': prm_snw_amf_i,
        'snw_pmf': prm_snw_pmf_i,

        'sl0_mse': prm_sl0_mse_i,
        'sl1_mse': prm_sl1_mse_i,

        'sl0_fcy': prm_sl0_fcy_i,
        'sl0_bt0': prm_sl0_bt0_i,

        'sl1_pwp': prm_sl1_pwp_i,
        'sl1_fcy': prm_sl1_fcy_i,
        'sl1_bt0': prm_sl1_bt0_i,

        'urr_dth': prm_urr_dth_i,
        'lrr_dth': prm_lrr_dth_i,

        'urr_rsr': prm_urr_rsr_i,
        'urr_tdh': prm_urr_tdh_i,
        'urr_tdr': prm_urr_tdr_i,
        'urr_cst': prm_urr_cst_i,
        'urr_dro': prm_urr_dro_i,
        'urr_ulc': prm_urr_ulc_i,

        'lrr_tdh': prm_lrr_tdh_i,
        'lrr_cst': prm_lrr_cst_i,
        'lrr_dro': prm_lrr_dro_i,
    }

    return cmbs


def get_idxs_otps_py():

    cmbs = {
        'snw_dth': out_snw_dth_i,
        'snw_lpt': out_snw_lpt_i,
        'snw_aim': out_snw_aim_i,
        'snw_pim': out_snw_pim_i,
        'snw_mlt': out_snw_mlt_i,

        'sl0_mse': out_sl0_mse_i,
        'sl1_mse': out_sl1_mse_i,

        'sl0_prf': out_sl0_prf_i,
        'sl0_arf': out_sl0_arf_i,

        'sl1_etn': out_sl1_etn_i,

        'urr_dth': out_urr_dth_i,
        'lrr_dth': out_lrr_dth_i,

        'urr_rnf': out_urr_rnf_i,
        'urr_pln': out_urr_pln_i,

        'lrr_rnf': out_lrr_rnf_i,

        'rnf_sfc': out_rnf_sfc_i,
        'rnf_gnd': out_rnf_gnd_i,

        'mod_bal': out_mod_bal_i,

    }

    return cmbs


def get_abds_prms_py():

    '''
    Absolute bounds on each parameter.
    '''

    buds = {
        'snw_dth': (0.00, PINF),
        'snw_ast': (NINF, PINF),
        'snw_amt': (NINF, PINF),
        'snw_amf': (0.00, PINF),
        'snw_pmf': (0.00, PINF),

        'sl0_mse': (0.00, PINF),
        'sl1_mse': (0.00, PINF),

        'sl0_fcy': (0.00, PINF),
        'sl0_bt0': (0.00, PINF),

        'sl1_pwp': (0.00, PINF),
        'sl1_fcy': (0.00, PINF),
        'sl1_bt0': (0.00, PINF),

        'urr_dth': (0.00, PINF),
        'lrr_dth': (0.00, PINF),

        'urr_rsr': (0.00, 1.00),
        'urr_tdh': (0.00, PINF),
        'urr_tdr': (0.00, 1.00),
        'urr_cst': (0.00, 1.00),
        'urr_dro': (0.00, 1.00),
        'urr_ulc': (0.00, 1.00),

        'lrr_tdh': (0.00, PINF),
        'lrr_cst': (0.00, 1.00),
        'lrr_dro': (0.00, 1.00),
    }

    return buds
#==============================================================================

#==============================================================================
# The model.
#==============================================================================


def hbv1d012a_py(
        tems,
        ppts,
        pets,
        otps,
        diss,
        prms,
        oflg,
        dslr):

    _hbv1d012a(
        tems,
        ppts,
        pets,
        otps,
        diss,
        prms,
        oflg,
        dslr)
    return


def _hbv1d012a(tems, ppts, pets, otps, diss, prms, oflg, dslr):

    '''
    A lumped conceptual HBV.

    Variant: 012a (child of 012).
             18 model parameters. 5 initial values. 23 parameters in total.

    Features:
        - Snow fall and melt temperature are different.
        - Precipitation can induce melt as well.
        - Two soil layers. One that limits infiltration and the other
          controls evapotranspiration.
        - Non-linear routing for the upper reservoir.
        - Some flow may exit catchment without appearing as runoff.
        - Limit on the depth of lower reservoir. Smooth transition.
          e.g., more flow downstream when the cell downstream has less depth.

    Parameters:
        tems: Temperature [time]
        ppts: Precipitation [time]
        pets: Potential evapotranspiration [time]
        otps: Outputs [time, variable]
        diss: Discharge that flows out on surface [time]
        prms: Model parameters [parameter]
        oflg: Optimization flag. When True, the otps is only a single step.
              Which is overwritten at each iteration. This spares memory.
    '''

    nt = otps.shape[0]
    #==========================================================================

    prm_snw_ast = prms[prm_snw_ast_i]
    prm_snw_amt = prms[prm_snw_amt_i]
    prm_snw_amf = prms[prm_snw_amf_i]
    prm_snw_pmf = prms[prm_snw_pmf_i]

    prm_sl0_fcy = prms[prm_sl0_fcy_i]
    prm_sl0_bt0 = prms[prm_sl0_bt0_i]

    prm_sl1_pwp = prms[prm_sl1_pwp_i]
    prm_sl1_fcy = prms[prm_sl1_fcy_i]
    prm_sl1_bt0 = prms[prm_sl1_bt0_i]

    prm_urr_rsr = prms[prm_urr_rsr_i]
    prm_urr_tdh = prms[prm_urr_tdh_i]
    prm_urr_tdr = prms[prm_urr_tdr_i]
    prm_urr_cst = prms[prm_urr_cst_i]
    prm_urr_dro = prms[prm_urr_dro_i]
    prm_urr_ulc = prms[prm_urr_ulc_i]

    prm_lrr_tdh = prms[prm_lrr_tdh_i]
    prm_lrr_cst = prms[prm_lrr_cst_i]
    prm_lrr_dro = prms[prm_lrr_dro_i]

    for t in range(nt):

        if oflg:
            tt = 0

        else:
            tt = t
        #======================================================================

        # Inputs.
        tem = tems[t]
        ppt = ppts[t]
        pet = pets[t]
        #======================================================================

        #======================================================================
        # Snowpack formation and melt parameters.
        #======================================================================

        if t == 0:
            lpv_snw_dth = prms[prm_snw_dth_i]

        elif oflg:
            lpv_snw_dth = otps[tt, out_snw_dth_i]

        else:
            lpv_snw_dth = otps[t - 1, out_snw_dth_i]
        #======================================================================

        # Snowpack formation and melt.
        lpv_snw_aim = 0
        lpv_snw_pim = 0
        lpv_snw_mlt = 0
        lpv_snw_lpt = 0

        if (lpv_snw_dth > 0) and (tem > prm_snw_amt):

            # Air induced snow melt.
            lpv_snw_aim = tem - prm_snw_amt
            lpv_snw_aim *= prm_snw_amf
            lpv_snw_aim = min(lpv_snw_dth, lpv_snw_aim)

            if lpv_snw_aim > 0:

                lpv_snw_dth -= lpv_snw_aim
                lpv_snw_mlt += lpv_snw_aim

            if ppt > 0:

                lpv_snw_lpt = ppt

                if (prm_snw_pmf > 0) and (lpv_snw_dth > 0):

                    # Precipitation induced snow melt.
                    # TODO: ppt can also freeze when little!
                    lpv_snw_pim = tem - prm_snw_amt
                    lpv_snw_pim *= prm_snw_pmf * ppt
                    lpv_snw_pim = min(lpv_snw_dth, lpv_snw_pim)

                    if lpv_snw_pim > 0:

                        lpv_snw_dth -= lpv_snw_pim
                        lpv_snw_mlt += lpv_snw_pim

        elif (tem <= prm_snw_ast) and (ppt > 0):

            lpv_snw_dth += ppt

        elif (tem > prm_snw_ast) and (ppt > 0):

            # Liquid precipitation.
            lpv_snw_lpt = ppt
        #======================================================================

        otps[tt, out_snw_dth_i] = lpv_snw_dth
        otps[tt, out_snw_lpt_i] = lpv_snw_lpt
        otps[tt, out_snw_aim_i] = lpv_snw_aim
        otps[tt, out_snw_pim_i] = lpv_snw_pim
        otps[tt, out_snw_mlt_i] = lpv_snw_mlt
        #======================================================================

        #======================================================================
        # Evapotranspiration, infiltration, soil moisture and runoff.
        # Soil layer 0 is for runoff only.
        # Soil layer 1 is for evapotranspiration only.
        #======================================================================

        # Previous soil moistures.
        if t == 0:
            lpv_sl0_mse = prms[prm_sl0_mse_i]
            lpv_sl1_mse = prms[prm_sl1_mse_i]

        elif oflg:
            lpv_sl0_mse = otps[tt, out_sl0_mse_i]
            lpv_sl1_mse = otps[tt, out_sl1_mse_i]

        else:
            lpv_sl0_mse = otps[t - 1, out_sl0_mse_i]
            lpv_sl1_mse = otps[t - 1, out_sl1_mse_i]
        #======================================================================

        # Potential runoff from snow melt and liquid water.
        lpv_sl0_prf = lpv_snw_lpt + lpv_snw_mlt

        # Actual runoff.
        lpv_sl0_arf = 0

        # Remaining runoff.
        lpv_sl0_rrm = lpv_sl0_prf
        #======================================================================

        if lpv_sl0_rrm:

            # Relative amount that becomes runoff.
            lpv_sl0_ror = powf(lpv_sl0_mse / prm_sl0_fcy, prm_sl0_bt0)

            if lpv_sl0_ror > 1: lpv_sl0_ror = 1

            # Infiltration.
            lpv_sl0_iln = min(
                lpv_sl0_rrm * (1 - lpv_sl0_ror), prm_sl0_fcy - lpv_sl0_mse)

            if lpv_sl0_iln < 0: lpv_sl0_iln = 0

            lpv_sl0_mse += lpv_sl0_iln
            lpv_sl0_rrm -= lpv_sl0_iln

            lpv_sl0_arf += lpv_sl0_rrm
            lpv_sl0_rrm = 0
        #======================================================================

        # Evapotranspiration.
        lpv_sl1_epr = lpv_sl1_mse / prm_sl1_pwp

        if lpv_sl1_epr > 1: lpv_sl1_epr = 1

        lpv_sl1_etn = lpv_sl1_epr * pet
        lpv_sl1_etn = min(lpv_sl1_mse, lpv_sl1_etn)

        lpv_sl1_mse -= lpv_sl1_etn
        #======================================================================

        # Transfer of moisture from layer 0 to 1.
        if (lpv_sl0_mse > 0) and (lpv_sl1_mse < prm_sl1_fcy):

            lpv_sl0_sl1 = lpv_sl0_mse * powf(
                1 - (lpv_sl1_mse / prm_sl1_fcy), prm_sl1_bt0)

            lpv_sl0_sl1 = min(lpv_sl0_sl1, prm_sl1_fcy - lpv_sl1_mse)

            lpv_sl0_mse -= lpv_sl0_sl1
            lpv_sl1_mse += lpv_sl0_sl1

            # This lead to numerical errors, somehow.
            # Possibly due to negative inputs of powf?
            # if lpv_sl1_mse > prm_sl1_fcy:
            #     lpv_sl0_mse += lpv_sl1_mse - prm_sl1_fcy
            #     lpv_sl1_mse = prm_sl1_fcy
            #
            #     acts[t, prm_sl1_fcy_i] += 1
            #
            #     # Just in case.
            #     if lpv_sl0_mse > prm_sl0_fcy:
            #         lpv_sl0_arf += lpv_sl0_mse - prm_sl0_fcy
            #         lpv_sl0_mse = prm_sl0_fcy
            #
            #         acts[t, prm_sl0_fcy_i] += 1
        #======================================================================

        otps[tt, out_sl0_mse_i] = lpv_sl0_mse
        otps[tt, out_sl1_mse_i] = lpv_sl1_mse
        otps[tt, out_sl0_prf_i] = lpv_sl0_prf
        otps[tt, out_sl0_arf_i] = lpv_sl0_arf
        otps[tt, out_sl1_etn_i] = lpv_sl1_etn
        #======================================================================

        #======================================================================
        # Runoff routing within cell/catchment (non-channel).
        #======================================================================

        # Previous upper and lower reservoir states.
        if t == 0:
            lpv_urr_dth = prms[prm_urr_dth_i]
            lpv_lrr_dth = prms[prm_lrr_dth_i]

        elif oflg:
            lpv_urr_dth = otps[tt, out_urr_dth_i]
            lpv_lrr_dth = otps[tt, out_lrr_dth_i]

        else:
            lpv_urr_dth = otps[t - 1, out_urr_dth_i]
            lpv_lrr_dth = otps[t - 1, out_lrr_dth_i]

        lpv_rnf_sfc = 0
        lpv_rnf_gnd = 0
        #======================================================================

        # Upper reservoir.
        lpv_urr_dth += lpv_sl0_arf * (1 - prm_urr_rsr)
        #======================================================================

        # Runoff from upper and lower outlets of the upper reservoir.
        if lpv_urr_dth > prm_urr_tdh:

            lpv_rnf_sfc += (lpv_urr_dth - prm_urr_tdh) * prm_urr_tdr
            lpv_urr_dth -= (lpv_urr_dth - prm_urr_tdh) * prm_urr_tdr

        lpv_urr_rnf = lpv_urr_dth * prm_urr_cst

        lpv_urr_dth -= lpv_urr_rnf

        lpv_rnf_sfc += lpv_urr_rnf * prm_urr_dro
        lpv_rnf_gnd += lpv_urr_rnf * (1 - prm_urr_dro)
        #======================================================================

        # Percolation from upper to lower reservoir.
        if lpv_lrr_dth < prm_lrr_tdh:
            lpv_urr_pln = lpv_urr_dth * prm_urr_ulc
            lpv_urr_pln *= 1 - (lpv_lrr_dth / prm_lrr_tdh)

        else:
            lpv_urr_pln = 0

        lpv_urr_dth -= lpv_urr_pln
        #======================================================================

        otps[tt, out_urr_rnf_i] = lpv_urr_rnf
        otps[tt, out_urr_pln_i] = lpv_urr_pln
        #======================================================================

        # Lower reservoir.
        lpv_lrr_rnf = lpv_lrr_dth * prm_lrr_cst

        lpv_lrr_dth -= lpv_lrr_rnf
        lpv_lrr_dth += lpv_urr_pln

        lpv_rnf_sfc += lpv_lrr_rnf * prm_lrr_dro
        lpv_rnf_gnd += lpv_lrr_rnf * (1 - prm_lrr_dro)
        #======================================================================

        otps[tt, out_lrr_dth_i] = lpv_lrr_dth
        otps[tt, out_lrr_rnf_i] = lpv_lrr_rnf
        #======================================================================

        # Upper reservoir update.
        lpv_urr_dth += lpv_sl0_arf * prm_urr_rsr

        otps[tt, out_urr_dth_i] = lpv_urr_dth
        #======================================================================

        # Surface and Groundwater runoff update.
        otps[tt, out_rnf_sfc_i] = lpv_rnf_sfc
        otps[tt, out_rnf_gnd_i] = lpv_rnf_gnd
        #======================================================================

        # River discharge.
        diss[t] = lpv_rnf_sfc * dslr
        #======================================================================

        #======================================================================
        # Mass Balance
        #======================================================================

        # A full length otps array is required, so this only takes place
        # when oflag is False. Values in this column should all be zeros.
        if oflg == 0:
            otps[t, out_mod_bal_i] = (
                ppt - (lpv_sl1_etn + lpv_rnf_sfc + lpv_rnf_gnd))

            if t == 0:
                otps[t, out_mod_bal_i] += (
                    prms[prm_snw_dth_i] +
                    prms[prm_sl0_mse_i] +
                    prms[prm_sl1_mse_i] +
                    prms[prm_urr_dth_i] +
                    prms[prm_lrr_dth_i])

                otps[t, out_mod_bal_i] -= (
                    lpv_snw_dth +
                    lpv_sl0_mse +
                    lpv_sl1_mse +
                    lpv_urr_dth +
                    lpv_lrr_dth)

            else:
                otps[t, out_mod_bal_i] -= (
                    (lpv_snw_dth - otps[t - 1, out_snw_dth_i]) +
                    (lpv_sl0_mse - otps[t - 1, out_sl0_mse_i]) +
                    (lpv_sl1_mse - otps[t - 1, out_sl1_mse_i]) +
                    (lpv_urr_dth - otps[t - 1, out_urr_dth_i]) +
                    (lpv_lrr_dth - otps[t - 1, out_lrr_dth_i]))
        #======================================================================
    return
