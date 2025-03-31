distance_matrix_pws_ref = plg.spatial.calc_point_to_point_distances(ds_pws, ds_gauges)

for pws_id in  ['ams74', 'ams134', 'ams113', 'ams36', str(ds_pws.isel(id=(ds_pws.hi_flag>0).sum(dim='time').argmax()).id.values)]:

    fig,ax=plt.subplots(1,2,figsize=(14,4))
    
    ds_pws_hourly.sel(id=pws_id).rainfall.plot(ax=ax[0],label=pws_id)
    (ds_gauges.sel(id=distance_matrix_pws_ref.idxmin(dim='id_neighbor').sel(id=pws_id)).rainfall*-1).plot(ax=ax[0],label='-ref')
    ds_pws.fz_flag.where(ds_pws.fz_flag>0).sel(id=pws_id).plot.line(x='time',lw=2,color='pink',label='FZ',ax=ax[0])
    ds_pws.hi_flag.where(ds_pws.hi_flag>0).sel(id=pws_id).plot.line(x='time',lw=2,color='cyan',label='HI',ax=ax[0])
    ds_pws.so_flag.where(ds_pws.so_flag>0).sel(id=pws_id).plot.line(x='time',lw=2,color='red',label='SO',ax=ax[0])
    ax[0].legend()

    indcorr_results.plot.scatter(x="dist", y="indcorr", color="grey", alpha=0.5, s=10, ax=ax[1])
    ax[1].scatter(dist_mtx_ref, indcorr_mtx_ref, color="r", alpha=0.5, s=10, label="Ref")
    indcorr_results.sel(id_neighbor=pws_id).plot.scatter(
        x="dist", y="indcorr", color="lime", s=15, label=pws_id, ax=ax[1]
    )
    IndCorr_Score = str(
        "{:.2f}".format(indcorr_results.sel(id_neighbor=pws_id).indcorr_score.values)
    )
    ax[1].text(0.8,0.8,IndCorr_Score, transform=ax[1].transAxes)
    plt.legend(loc='lower left')
    plt.show();