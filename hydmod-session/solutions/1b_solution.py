# Identify dates of yearly flow maxima
peak_flow_dates = daily_sim_valid_10420.resample('YE')['ref'].apply(lambda x: x.idxmax())
daily_sim_valid_10420.loc[peak_flow_dates]