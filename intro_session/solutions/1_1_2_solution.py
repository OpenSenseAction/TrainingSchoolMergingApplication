cml_ids_with_zero_rainfall = cmls_R_sum.cml_id.where(cmls_R_sum == 0, drop=True).data

i = 0

fig, axs = plt.subplots(2, 1, figsize=(12, 4))
ds_cmls.sel(cml_id=cml_ids_with_zero_rainfall[i]).rsl.plot.line(x='time', ax=axs[0])
ds_cmls.sel(cml_id=cml_ids_with_zero_rainfall[i]).tsl.plot.line(x='time', ax=axs[1])
plt.tight_layout();