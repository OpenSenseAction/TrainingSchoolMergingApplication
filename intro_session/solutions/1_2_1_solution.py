i = 15

cml_id = gauge_id_closest.isel(cml_id=i).cml_id
gauge_id = gauge_id_closest.isel(cml_id=i)

plt.scatter(
    ds_gauges_municp.sel(id=gauge_id).rainfall_amount.resample(time='1h').sum(),
    ds_cmls.isel(sublink_id=0).sel(cml_id=cml_id).R.resample(time='1h').mean(),
)
plt.xlim(0, 15)
plt.ylim(0, 15)
plt.title(f'CML: {cml_id.data}     Gauge: {gauge_id.data}')
plt.xlabel('Gauge rainfall sum (mm)')
plt.ylabel('CML rainfall sum  (mm)');