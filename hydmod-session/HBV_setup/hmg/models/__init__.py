# -*- coding: utf-8 -*-

'''
@author: Faizan-TU Munich

Nov 13, 2023

10:13:39 AM

Keywords:
'''

from timeit import default_timer

import numpy as np


class HBV1D012A:

    '''
    Interface for the 012A (lumped/1D) variant of HBV.
    More about the implementation inside hbv1d012a.pyx.

    This class allows for running the model given valid inputs with setters
    and retrieving outputs with getters.

    For functionality, read the documentation of the individual methods below.
    '''

    def __init__(self):

        '''
        Initiliaze everything correctly.

        For description of variables defined here, either look below or in the
        hbv1d012.pyx file.
        '''

        try:
            raise ImportError  # For now, don't use the cython version.

            # import pyximport
            # pyximport.install(inplace=True)
            #
            # from models.hbv1d012a_cy import (
            #     hbv1d012a_cy,
            #     get_idxs_prms_cy,
            #     get_idxs_otps_cy,
            #     get_abds_prms_cy)
            #
            # # The cy version was 464 times faster than the py version.
            # self._modl = hbv1d012a_cy  # The Model (as a function) in Cython.
            #
            # self._idxs_prms = get_idxs_prms_cy()  # Parameter indices.
            # self._idxs_otps = get_idxs_otps_cy()  # Output variables indices.
            # self._abds_prms = get_abds_prms_cy()  # Absolute parameter bounds.

        except:
            from .hbv1d012a_py import (
                hbv1d012a_py,
                get_idxs_prms_py,
                get_idxs_otps_py,
                get_abds_prms_py)

            self._modl = hbv1d012a_py  # The Model (as a function) in Python.

            self._idxs_prms = get_idxs_prms_py()  # Parameter indices.
            self._idxs_otps = get_idxs_otps_py()  # Output variables indices.
            self._abds_prms = get_abds_prms_py()  # Absolute parameter bounds.

        self._tems = None  # Temperature.
        self._ppts = None  # Precipitation.
        self._pets = None  # Potential evapotranspiration.

        self._tsps = None  # Number of time steps.
        self._otps = None  # Outputs.
        self._diss = None  # Discharge simulated.

        self._prms = None  # Parameters.

        self._oflg = None  # Optimization flag.
        self._dslr = None  # Runoff to river flow conversion constant (scaler).
        return

    def get_parameter_bounds_in_correct_order(self, buds_dict):

        '''
        Given a dictionary of parameter labels (keys), and the lower and
        upper bounds tuple (values) as a dictionary, return them in a 2D
        array with a guaranteed correct order/sequence for the model.
        Read below for the conditions that the items in buds_dict must pass
        before acceptance.

        Parameter labels and their absolute bounds can be had by the
        get_parameter_labels and get_parameter_absolute_bounds getters
        respectively.

        The output of this method is needed to set the parameter bounds
        for global optimizers like this of scipy.
        '''

        assert isinstance(buds_dict, dict), type(buds_dict)

        assert len(buds_dict) == len(self._abds_prms), (
            len(buds_dict), len(self._abds_prms))

        assert all([
            isinstance(lmts, (tuple, list))
            for lmts in buds_dict.values()]), buds_dict

        assert all([len(lmts) == 2 for lmts in buds_dict.values()]), buds_dict

        prms_buds = np.empty((len(self._abds_prms), 2), dtype=np.float32)

        for prm_lbl, (prm_llm_inp, prm_ulm_inp) in buds_dict.items():

            prm_llm_abs, prm_ulm_abs = self._abds_prms[prm_lbl]

            assert prm_llm_inp <= prm_ulm_inp, (
                prm_lbl, prm_llm_inp, prm_ulm_inp)

            assert prm_llm_abs <= prm_llm_inp <= prm_ulm_abs, (
                prm_lbl, prm_llm_abs, prm_llm_inp, prm_ulm_abs)

            assert prm_llm_abs <= prm_ulm_inp <= prm_ulm_abs, (
                prm_lbl, prm_llm_abs, prm_ulm_inp, prm_ulm_abs)

            prms_buds[self._idxs_prms[prm_lbl], 0] = prm_llm_inp
            prms_buds[self._idxs_prms[prm_lbl], 1] = prm_ulm_inp

        return prms_buds

    def get_parameter_labels(self):

        '''
        Get model parameters labels (keys) along with their indices (values)
        as a dictionary. This is needed for passing the parameters in a
        correct sequence to the model from outside. For meaning of each
        parameter, look inside the hbv1d012a.pyx file.
        '''

        return self._idxs_prms

    def get_parameter_absolute_bounds(self):

        '''
        The absolute bounds of each parameter as a dictionary. Parameter labels
        keys with a tuple of two values as the value. First value is the
        lower bound while the second is the upper. This is needed when
        specifying new parameters as a sanity check.
        '''

        return self._abds_prms

    def get_output_labels(self):

        '''
        Get model output labels (keys) along with their indices (values) as a
        dictionary. This is needed after a model run to see what each column
        means. For meaning of each parameter, look inside the hbv1d012a.pyx
        file.
        '''

        return self._idxs_otps

    def set_inputs(self, tems, ppts, pets):

        '''
        Time series of input variables for the model. These are to be in
        a specific form. Look at the tests below to know what is expected.
        Ideally, a 1D array of values for each variable, all of same length,
        of floating values and range checks.
        '''

        # Temperature [°C, °F, K].
        assert isinstance(tems, np.ndarray), type(tems)
        assert tems.ndim == 1, tems.ndim
        assert np.isfinite(tems).all()
        assert np.issubdtype(tems.dtype, np.floating), tems.dtype

        # Precipitation [Depth per unit time].
        assert isinstance(ppts, np.ndarray), type(ppts)
        assert ppts.ndim == 1, ppts.ndim
        assert np.isfinite(ppts).all()
        assert (ppts >= 0).all()
        assert np.issubdtype(ppts.dtype, np.floating), ppts.dtype

        # Potential evapotranspiration [Depth per unit time].
        assert isinstance(pets, np.ndarray), type(pets)
        assert pets.ndim == 1, pets.ndim
        assert np.isfinite(pets).all()
        assert (pets >= 0).all()
        assert np.issubdtype(pets.dtype, np.floating), pets.dtype

        # Shape check.
        assert tems.shape == ppts.shape == pets.shape, (
            tems.shape, ppts.shape, pets.shape)

        # Casting.
        self._tems = tems.astype(np.float32)
        self._ppts = ppts.astype(np.float32)
        self._pets = pets.astype(np.float32)
        return

    def set_outputs(self, tsps):

        '''
        Initialize the array that will hold all model outputs (otps) along
        with a seperate array that will hold the simulated river flow (diss).

        The columns of the otps array are identified by the dictionary
        returned by the get_output_labels.

        The arrays created here can be returned by the methods defined later
        below. This method only initilizes required arrays. The model will
        fill these later.
        '''

        assert isinstance(tsps, int), type(tsps)
        assert tsps > 0, tsps

        otps = np.empty((tsps, len(self._idxs_otps)), dtype=np.float32)
        diss = np.empty((tsps,), dtype=np.float32)

        self._tsps = tsps
        self._otps = otps
        self._diss = diss
        return

    def set_optimization_flag(self, oflg):

        '''
        Whether the model is an optimization run (oflag == 1) or a regular
        model run (oflg == 0). In case of optimization, only the outputs
        of the last time step are needed. Hence, only a single row in the
        outputs array is written to and read from again and again.
        Read below to see what conditions oflg must pass before usage.
        '''

        assert isinstance(oflg, (int, np.int64, np.int32)), type(oflg)
        assert oflg in (0, 1), oflg

        self._oflg = np.int64(oflg)
        return

    def set_discharge_scaler(self, dslr):

        '''
        Convert the model runoff from units those of the preciptiation to
        some other ones. Normally, preciptiation is either in mm/day or
        mm/hr. However, riverflow is measured m3/s. Also, as the model is
        lumped, that needs to be taken into account. dslr is the constant
        to do this. In case, the river flow also has the same units as
        preciptiation then dslr should be 1.

        For example, if dslr is 1 and precipitation has the units of
        mm/day then the resulting river flow (array returned by get_discharge)
        also has the units precipitation (specific discharge). If the
        desired units of discharge are m3/s, with say a catchment area of
        25.5 km2 and precipitation in mm/day, then
        dslr = (25.5 * 1e6) / (3600 * 24 * 1000).
        '''

        assert isinstance(dslr, (float, np.float32, np.float64)), type(dslr)

        assert dslr > 0, dslr

        self._dslr = np.float32(dslr)
        return

    def set_parameters(self, prms):

        '''
        Model parameters as an array of floating values only. The number of
        values should match the length of the parameter labels. All values
        should be within the absolute bounds defined inside hbv1d12a.pyx.
        prms should pass the follwing conditions in order for it to be
        accepted for the model.
        '''

        assert isinstance(prms, np.ndarray), type(prms)
        assert prms.ndim == 1, prms.ndim
        assert np.isfinite(prms).all(), prms

        assert prms.size == len(self._idxs_prms), (
            prms.size, len(self._idxs_prms))

        assert np.issubdtype(prms.dtype, np.floating), prms.dtype

        prms = prms.astype(np.float32)

        for prm_lbl, idx in self._idxs_prms.items():

            prm_llm, prm_ulm = self._abds_prms[prm_lbl]

            assert (prm_llm <= prms[idx] <= prm_ulm), (
                    prm_lbl, prm_llm, prms[idx], prm_ulm)

        self._prms = prms
        return

    def get_model(self):

        '''
        Get the model as a fucntion. Function signature and implemntation
        inside hbv1d12a.pyx.
        '''

        return self._modl

    def run_model(self):

        '''
        Given all the variables set by all the setters before, run the model.

        Nothing is returned here. For various outputs, use the getters
        following this methods.
        '''

        assert self._tems is not None
        assert self._ppts is not None
        assert self._pets is not None

        assert self._tsps is not None
        assert self._otps is not None
        assert self._diss is not None

        assert self._prms is not None

        assert self._oflg is not None
        assert self._dslr is not None

        assert self._tems.shape[0] == self._otps.shape[0], (
            self._tems.shape[0], self._otps.shape[0])

        tme_flg = True

        if tme_flg: beg_tme = default_timer()

        self._modl(
            self._tems,
            self._ppts,
            self._pets,
            self._otps,
            self._diss,
            self._prms,
            self._oflg,
            self._dslr,
            )

        if tme_flg:
            end_tme = default_timer()

            #print(f'Model runtime: {end_tme - beg_tme:0.2E} seconds.')
        return

    def get_outputs(self):

        '''
        Get the outputs array filled by the model after callling run_model.
        Each column in this array has a label that is returned by
        get_output_labels.
        '''

        return self._otps

    def get_discharge(self):

        '''
        Get the simulated river flow with the conversion resulting after
        taking the product of dslr and model runoff. For example, if dslr was
        1 then the units of the returned value are same as those of the
        precipitation (specific discharge). If dslr was to scale model runoff
        to m3/s then the returned values have the units of m3/s.
        '''

        return self._diss

    def reset(self):

        '''
        Reinitiliaze everything correctly.
        '''

        self.__init__()
        return

