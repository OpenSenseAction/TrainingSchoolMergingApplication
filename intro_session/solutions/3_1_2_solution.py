fig,ax=plt.subplots(figsize=(12,5))
# Define the colors for each filter
colors = ['red', 'blue', 'green']

for idx, filter_name in enumerate(["fz_flag", "hi_flag", "so_flag"]):
    filter_data = ds_pws[filter_name]
    idx_id, idx_time  = np.where(filter_data == 1)
    time_values = ds_pws.coords['time'].values[idx_time]
    ax.scatter(time_values, idx_id, s=3, color=colors[idx], label=filter_name, alpha=0.6)

# Set labels
ax.set_xlabel('Time')
ax.set_ylabel('ID')
ax.set_title('Occurance of individual flags')

# Add a legend
ax.legend(loc='lower left')

plt.tight_layout();