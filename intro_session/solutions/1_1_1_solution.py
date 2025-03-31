radar_along_cml_R_sum = radar_along_cml_R_1h.sum(dim='time')
cmls_R_sum = cmls_R_1h.sum(dim='time')

da_diff = radar_along_cml_R_sum - cmls_R_sum

fig, axs = plt.subplots(1, 3, figsize=(12, 5))
plg.plot_map.plot_plg(da_cmls=radar_along_cml_R_sum, ax=axs[0], vmin=0, vmax=100)
plg.plot_map.plot_plg(da_cmls=cmls_R_sum, ax=axs[1], vmin=0, vmax=100)
plg.plot_map.plot_plg(da_cmls=da_diff, ax=axs[2], vmin=-20, vmax=20, cmap='RdBu')