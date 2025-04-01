R_product_dict = {
    'uncorrected radar': ds_radar.R_observed,
    'IDW (gauge and CML)': R_grid_idw_high_level,
    'OK (gauge and CML)': R_grid_ok_high_level,
    'KED (gauge and CML)': R_grid_ked_high_level,
}

fig, axs = plt.subplots(1, 4, figsize=(12, 3))
for i, (product_name, R_product) in enumerate(R_product_dict.items()):
    axs[i].scatter(
        ds_radar.R_true.data.flatten(), 
        R_product.data.flatten(),
        c='k',
        alpha=0.5,
        s=10,
    )
    axs[i].plot([0, 20], [0, 20])
    axs[i].set_title(product_name)