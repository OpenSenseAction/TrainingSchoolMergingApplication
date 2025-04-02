c_area = 749.1 * 1e6
HBVd_valid.main(
    hourly_prms_10420, 
    inp_dfe = hourly_data_valid_10420, 
    cat_area = c_area,
    secs_per_step = 3600, 
    output_dir=r'hourly/validation_Intermet', 
    cat_label = '10420')