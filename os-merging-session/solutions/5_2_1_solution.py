R_grid_ok = ok_interpolator.interpolate(
            da_grid=ds_radar,
            da_cml=ds_cmls.R_diff,
            variogram_parameters = {"sill": 1, "range": 10, "nugget": 0.01},
        )

plot_true_obs_adj_diff(
    da_grid_R_true=ds_radar.R_true,
    da_grid_R_observed=ds_radar.R_observed,
    da_grid_R_adjusted=ds_radar.R_observed + R_grid_ok,
    da_cmls_R=ds_cmls.R,
    da_cmls_R_diff=ds_cmls.R_diff,
)