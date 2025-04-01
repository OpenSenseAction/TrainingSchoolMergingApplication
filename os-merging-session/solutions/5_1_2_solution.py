get_grid_at_points = plg.spatial.GridAtPoints(
    da_gridded_data=ds_radar,
    da_point_data=ds_gauges,
    nnear=1,
    use_lon_lat=False,
)

ds_gauges['R_radar'] = get_grid_at_points(
    da_gridded_data=ds_radar.R_observed,
    da_point_data=ds_gauges.R,
)

ds_gauges['R_fact'] = ds_gauges.R / ds_gauges.R_radar

idw_interpolator = mrg.interpolate.InterpolateIDW(min_observations=2)

R_grid_idw = idw_interpolator.interpolate(
            da_grid=ds_radar,
            da_gauge=ds_gauges.R_fact,
            p=3,
            idw_method='standard',
        )

plot_true_obs_adj_diff(
    da_grid_R_true=ds_radar.R_true,
    da_grid_R_observed=ds_radar.R_observed,
    da_grid_R_adjusted=ds_radar.R_observed * R_grid_idw,
    da_gauges_R=ds_gauges.R,
    da_gauges_R_diff=ds_gauges.R_diff,
)