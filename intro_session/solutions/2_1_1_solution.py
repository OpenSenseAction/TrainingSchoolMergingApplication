for cmlid in [40, 42, 120]:
    ds_cml = ds_cmls.isel(cml_id=cmlid) 

    fig, axs = plt.subplots(2, 1, figsize=(10, 3))
    ds_cml.tsl.plot.line(x='time', ax=axs[0])
    ds_cml.rsl.plot.line(x='time', ax=axs[1])
    axs[1].set_title('')
    axs[0].set_ylabel('TSL')
    axs[1].set_ylabel('RSL');
