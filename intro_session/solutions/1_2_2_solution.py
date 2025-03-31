i = 27
cml_id = gauge_id_closest.isel(cml_id=i).cml_id
gauge_id = gauge_id_closest.isel(cml_id=i)

plt.scatter(
    ds_gauges_municp.sel(id=gauge_id).rainfall_amount.resample(time='1h').sum(),
    ds_cmls.isel(sublink_id=0).sel(cml_id=cml_id).R.resample(time='1h').mean(),
    alpha=0.5,
    label='CML',
)
plt.scatter(
    ds_gauges_municp.sel(id=gauge_id).rainfall_amount.resample(time='1h').sum(),
    radar_along_cml.sel(cml_id=cml_id).resample(time='1h').mean(),
    alpha=0.5,
    label='radar',
)
plt.xlim(0, 15)
plt.ylim(0, 15)
plt.title(f'CML: {cml_id.data}     Gauge: {gauge_id.data}')
plt.xlabel('Gauge rainfall sum (mm)')
plt.ylabel('CML or radar rainfall sum  (mm)')
plt.legend();