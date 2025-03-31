ds_cmls['tl'] = ds_cmls.tsl-ds_cmls.rsl
for cmlid in [40, 42, 120]:
    ds_cml = ds_cmls.isel(cml_id=cmlid) 

    fig, axs = plt.subplots(3, 1, figsize=(10, 5))
    ds_cml.tsl.plot.line(x='time', ax=axs[0])
    ds_cml.rsl.plot.line(x='time', ax=axs[1])
    ds_cml.tl.plot.line(x='time', ax=axs[2])
    axs[1].set_title('')
    axs[2].set_title('')
    axs[0].set_ylabel('TSL')
    axs[1].set_ylabel('RSL')
    axs[2].set_ylabel('TL');
