# FZ flag
most_fz_flags_id = (ds_pws.fz_flag == 1).sum(dim='time').argmax()

fig, ax1 = plt.subplots(figsize=(10, 4))

# Plot the 'pws time series' (rainfall) and 'neighbor time series' (reference)
ds_pws.isel(id=most_fz_flags_id).rainfall.plot(ax=ax1, label='PWS time series')
(ds_pws.isel(id=most_fz_flags_id).reference * -1).plot(ax=ax1, label='Neighbor time series')

# Create a twin y-axis to plot 'fz_flag'
ax2 = ax1.twinx()
ds_pws.isel(id=most_fz_flags_id).fz_flag.plot(ax=ax2, label='FZ-flag',color='red')

ax1.set_xlabel('Time')
ax1.set_ylabel('Rainfall / Neighbor time series (time -1)')
ax2.set_ylabel('FZ-flag')

ax2.set_ylim(-2,20)
ax2.axhline(y = 0, color='black',  lw=0.5)

ax1.set_title('FZ flag')
ax2.set_title('')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right');

# HI flag
max_rainfall_id = ds_pws.rainfall.where(ds_pws.rainfall == ds_pws.rainfall.max(), drop=True).id

fig, ax1 = plt.subplots(figsize=(10, 4))

# Plot the 'pws time series' (rainfall) and 'neighbor time series' (reference)
ds_pws.sel(id=max_rainfall_id).rainfall.plot(ax=ax1, label='PWS time series')
(ds_pws.sel(id=max_rainfall_id).reference * -1).plot(ax=ax1, label='Neighbor time series')

# Create a twin y-axis to plot 'hi_flag'
ax2 = ax1.twinx()
ds_pws.sel(id=max_rainfall_id).hi_flag.plot(ax=ax2, label='HI_flag',color='red')

ax1.set_xlabel('Time')
ax1.set_ylabel('Rainfall / Neighbor time series (time -1)')
ax2.set_ylabel('HI-flag')

ax1.set_ylim(-5,30)
ax2.set_ylim(-2,20)
ax2.axhline(y = 0, color='black',  lw=0.5)

ax1.set_title('HI flag')
ax2.set_title('')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right');

# SO flag
(ds_pws.so_flag == 1).sum(dim='time')

so_flag_id=9

fig, ax1 = plt.subplots(figsize=(10, 4))

# Plot the 'pws time series' (rainfall) and 'neighbor time series' (reference)
ds_pws.sel(time='2018').isel(id=so_flag_id).rainfall.plot(ax=ax1, label='PWS time series')
(ds_pws.sel(time='2018').isel(id=so_flag_id).reference * -1).plot(ax=ax1, label='Neighbor time series')

# Create a twin y-axis to plot 'so_flag'
ax2 = ax1.twinx()
ds_pws.sel(time='2018').isel(id=so_flag_id).so_flag.plot(ax=ax2, label='SO-flag',color='red')

ax1.set_xlabel('Time')
ax1.set_ylabel('Rainfall / Neighbor time series (time -1)')
ax2.set_ylabel('SO-flag')

ax1.set_ylim(-2,4)
ax2.set_ylim(-2,20)
ax2.axhline(y = 0, color='black',  lw=0.5)

ax1.set_title('SO flag')
ax2.set_title('')
ax1.legend(loc='upper left')
ax2.legend(loc='upper right');