# -*- coding: utf-8 -*-

'''
@author: Faizan-TU Munich

Jan 01, 2025

5:45:17 PM

Instructions:
The code here is needed by other scripts. Do no do anything to this file.
It should next to all the other scripts.
'''

import numpy as np
from scipy.stats import rankdata, linregress


class HMG3DModelEffsNaNs:

    _cmpt_effs_flag = False

    def __init__(
        self,
        ref,
        ns_flag,
        lns_flag,
        kg_flag,
        pc_flag,
        sc_flag,
        sp_flag,
        ns_dc_flag):

        assert isinstance(ref, np.ndarray)
        assert ref.ndim == 2
        assert ref.size

        nnan_idxs = ~np.isnan(ref)

        if self._cmpt_effs_flag:
            assert (nnan_idxs.sum(axis=0) > 0).all()
            assert np.all(np.isfinite(ref[nnan_idxs]))

        assert isinstance(ns_flag, bool)
        assert isinstance(lns_flag, bool)
        assert isinstance(kg_flag, bool)
        assert isinstance(pc_flag, bool)
        assert isinstance(sc_flag, bool)
        assert isinstance(sp_flag, bool)
        assert isinstance(ns_dc_flag, bool)

        assert any([
            ns_flag,
            lns_flag,
            kg_flag,
            pc_flag,
            sc_flag,
            sp_flag,
            ns_dc_flag])

        self.ref = ref
        self.nnan_idxs = nnan_idxs

        self.ns_flag = ns_flag
        self.lns_flag = lns_flag
        self.kg_flag = kg_flag
        self.pc_flag = pc_flag
        self.sc_flag = sc_flag
        self.sp_flag = sp_flag
        self.ns_dc_flag = ns_dc_flag

        self.ref_shape = ref.shape

        self.ref_mean = None
        self.ns_demr = None
        self.ref_ln = None
        self.lns_demr = None
        self.ref_std = None
        self.ref_ranks = None

        self.ref_cum = None
        self.ref_cum_mean = None
        self.ns_dc_demr = None

        self.sim = None
        self.sim_cum = None

        if self._cmpt_effs_flag:
            self._prep_constants()
        return

    def _prep_constants(self):

        self.ref_mean = np.nanmean(self.ref, axis=0)

        if self.ns_flag:
            self.ns_demr = np.nansum((self.ref - self.ref_mean) ** 2, axis=0)

            assert (self.ns_demr > 0).all()

        if self.lns_flag:
            with np.errstate(divide='ignore'):
                self.ref_ln = np.log(self.ref)

            ref_mean_ln = np.nanmean(self.ref_ln, axis=0)

            self.lns_demr = np.nansum((self.ref_ln - ref_mean_ln) ** 2, axis=0)

            assert (self.lns_demr > 0).all()

        if self.kg_flag:
            self.ref_std = np.nanstd(self.ref, axis=0)

            assert (self.ref_std > 0).all()

        if self.sc_flag:
            self.ref_ranks = rankdata(self.ref, axis=0, nan_policy='omit')

        if self.ns_dc_flag:
            with np.errstate(divide='ignore'):
                self.ref_cum = self.ref.copy()

            self.ref_cum[~self.nnan_idxs] = 0
            self.ref_cum = self.ref_cum.cumsum(axis=0)

            self.ref_cum_mean = (
                self.ref_cum.sum(axis=0) / self.nnan_idxs.sum(axis=0))

            self.ref_cum[~self.nnan_idxs] = np.nan

            self.ns_dc_demr = np.nansum(
                (self.ref_cum - self.ref_cum_mean) ** 2, axis=0)

            assert (self.ns_dc_demr > 0).all()

        return

    def set_sim(self, sim_orig, sim_tol):

        assert sim_orig.shape == self.ref_shape, (
            sim_orig.shape, self.ref_shape)

        assert np.all(np.isfinite(sim_orig))

        if sim_tol is not None:

            assert sim_tol.shape == self.ref_shape, (
                sim_tol.shape, self.ref_shape)

            assert np.all(np.isfinite(sim_tol))

            self.sim = sim_tol

        else:
            self.sim = sim_orig

        if self.ns_dc_flag:
            self.sim_cum = sim_orig.copy()
            self.sim_cum[~self.nnan_idxs] = 0
            self.sim_cum = self.sim_cum.cumsum(axis=0)
            self.sim_cum[~self.nnan_idxs] = np.nan

        return

    def get_ns(self):

        assert self.ns_flag

        ns_numr = np.nansum((self.ref - self.sim) ** 2, axis=0)

        ns = 1.0 - (ns_numr / self.ns_demr)

        return ns

    def get_lns(self):

        assert self.lns_flag

        with np.errstate(divide='ignore'):

            lns_numr = np.nansum(
                np.square(self.ref_ln - np.log(self.sim)), axis=0)

        lns = 1.0 - (lns_numr / self.lns_demr)

        return lns

    def get_kg(self):

        assert self.kg_flag

        r = np.empty(self.ref_shape[1])
        b = np.empty(self.ref_shape[1])
        g = np.empty(self.ref_shape[1])

        for i in range(r.shape[0]):

            ref = self.ref[self.nnan_idxs[:, i], i]
            sim = self.sim[self.nnan_idxs[:, i], i]

            try:
                r[i] = np.corrcoef(ref, sim)[0, 1]

            except:
                r[i] = -1.0

            b[i] = np.mean(sim) / self.ref_mean[i]
            g[i] = np.std(sim) / self.ref_std[i]

        kg = 1 - ((r - 1) ** 2 + (b - 1) ** 2 + (g - 1) ** 2) ** 0.5

        return kg

    def get_pc(self):

        assert self.pc_flag

        pc = np.empty(self.ref_shape[1])

        for i in range(pc.shape[0]):
            ref = self.ref[self.nnan_idxs[:, i], i]
            sim = self.sim[self.nnan_idxs[:, i], i]

            try:
                pc[i] = np.corrcoef(ref, sim)[0, 1]

            except:
                pc[i] = -1.0

        return pc

    def get_sc(self):

        assert self.sc_flag

        ref_ranks = self.ref_ranks
        sim_ranks = rankdata(self.sim, axis=0, nan_policy='omit')

        sc = np.empty(self.ref_shape[1])

        for i in range(sc.shape[0]):
            ref = ref_ranks[self.nnan_idxs[:, i], i]
            sim = sim_ranks[self.nnan_idxs[:, i], i]

            try:
                sc[i] = np.corrcoef(ref, sim)[0, 1]

            except:
                sc[i] = -1.0

        return sc

    def get_sp(self):

        assert self.sp_flag

        sp = np.empty(self.ref_shape[1])

        for i in range(sp.shape[0]):
            ref = self.ref[self.nnan_idxs[:, i], i]
            sim = self.sim[self.nnan_idxs[:, i], i]

            sp[i] = linregress(ref, sim).slope

        return sp

    def get_ns_dc(self):

        assert self.ns_dc_flag

        ns_dc_numr = np.nansum((self.ref_cum - self.sim_cum) ** 2, axis=0)

        ns_dc = 1.0 - (ns_dc_numr / self.ns_dc_demr)

        return ns_dc

    def get_all_dict(self):

        effs_dict = {}

        if self._cmpt_effs_flag:

            if self.ns_flag:
                effs_dict['ns'] = self.get_ns()

            if self.lns_flag:
                effs_dict['lns'] = self.get_lns()

            if self.kg_flag:
                effs_dict['kg'] = self.get_kg()

            if self.pc_flag:
                effs_dict['pc'] = self.get_pc()

            if self.sc_flag:
                effs_dict['sc'] = self.get_sc()

            if self.sp_flag:
                effs_dict['sp'] = self.get_sp()

            if self.ns_dc_flag:
                effs_dict['ns_dc'] = self.get_ns_dc()

        else:
            objs = np.ones(self.ref_shape[1])

            if self.ns_flag:
                effs_dict['ns'] = objs

            if self.lns_flag:
                effs_dict['lns'] = objs

            if self.kg_flag:
                effs_dict['kg'] = objs

            if self.pc_flag:
                effs_dict['pc'] = objs

            if self.sc_flag:
                effs_dict['sc'] = objs

            if self.sp_flag:
                effs_dict['sp'] = objs

            if self.ns_dc_flag:
                effs_dict['ns_dc'] = objs

        return effs_dict
