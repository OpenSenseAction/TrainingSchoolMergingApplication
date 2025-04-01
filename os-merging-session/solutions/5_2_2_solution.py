ok_interpolator = mrg.interpolate.InterpolateOrdinaryKriging(min_observations=2, discretization=8)

R_grid_idw = idw_interpolator.interpolate(
            da_grid=ds_radar,
            da_cml=ds_cmls.R_diff,
            p=3,
            idw_method='standard',
        )

R_grid_ok = ok_interpolator.interpolate(
            da_grid=ds_radar,
            da_cml=ds_cmls.R_diff,
            variogram_parameters = {"sill": 1, "range": 20, "nugget": 0.01},
            full_line=False,
        )

R_grid_ok_block = ok_interpolator.interpolate(
            da_grid=ds_radar,
            da_cml=ds_cmls.R_diff,
            variogram_parameters = {"sill": 1, "range": 20, "nugget": 0.01},
            full_line=True,
        )

vmin, vmax = -3, 3
fig, axs = plt.subplots(1, 3, figsize=(14, 3))
R_grid_idw.plot(ax=axs[0], vmin=vmin, vmax=vmax, cmap='RdBu')
R_grid_ok.plot(ax=axs[1], vmin=vmin, vmax=vmax, cmap='RdBu')
R_grid_ok_block.plot(ax=axs[2], vmin=vmin, vmax=vmax, cmap='RdBu')
for i in [0, 1, 2]:
    plg.plot_map.plot_plg(da_cmls=ds_cmls.R_diff, ax=axs[i], vmin=vmin, vmax=vmax, cmap='RdBu', add_colorbar=False)
