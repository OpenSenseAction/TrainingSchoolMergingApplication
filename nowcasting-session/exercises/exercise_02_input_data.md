# Exercise 2: Read, visualize and process input data

The purpose of this exercise is to get the users acquainted with the input data of the nowcasting methods, and its visualization and preprocessing.

## Read an example dataset to get to know the pysteps data structure

From the datasets downloaded in the [previous exercise](exercise_01_local_conda_setup.md), pick either the "fmi" or "mch" dataset that have been tested to work with this exercise. You can use [pysteps.datasets.load_dataset](https://pysteps.readthedocs.io/en/stable/generated/pysteps.datasets.load_dataset.html#pysteps.datasets.load_dataset) for this purpose. For the mch data, choose the time period between 2015-05-15 15:50-16:50 UTC. For "fmi", choose 2016-09-28 14:45-15:50 UTC. Use pysteps functions to read the time series into a numpy array and examine the metadata.

Note the structure of the metadata and the data array. The metadata is required and updated by many pysteps functions, and it contains information about the time, geographical extent, and the units of the data. The data array contains the precipitation values in the specified units. The metadata should contain the following information:

- `accutime`: accumulation time (minutes) for computing the quantity contained in the data
- `cartesian_unit`: the distance unit of the geographical coordinates
- `institution`: institution providing the data
- `product`: name of the product
- `projection`: PROJ-compatible projection definition
- `threshold`: the minimum observed value
- `timestamps`: list of timestamps, one for each element in the returned data array
- `transform`: applied transformation to the data values (if any)
- `unit`: the unit of the data
- `x1`: x-coordinate of the lower-left corner of the domain in geographical coordinates
- `x2`: x-coordinate of the upper-right corner of the domain in geographical coordinates
- `xpixelsize`: pixel size in x-direction (meters)
- `y1`: y-coordinate of the lower-left corner of the domain in geographical coordinates
- `y2`: y-coordinate of the upper-right corner of the domain in geographical coordinates
- `yorigin`: 'upper' or 'lower' depending on whether the origin of the coordinate system is in the lower-left or upper-left corner
- `ypixelsize`: pixel size in y-direction (meters)
- `zerovalue`: value corresponding to no precipitation
- `zr_a`: the a-coefficient in the Z(R) relationship Z=a\*R^b applied to the data (if representing rain rate)
- `zr_b`: the b-coefficient in the Z(R) relationship Z=a\*R^b applied to the data (if representing rain rate)

## Read a dataset processed in the previous sessions

We have uploaded an example dataset of radar and CML data processed with the methods introduced in the merging session.
The datasets are located in the `nowcasting-session/data` folder, and the following files are available:

- `OpenRainER_cml.nv`: interpolated CML data in the OpenSense NetCDF format. The file contains several versions of the interpolation in the `rainfall_interpolateIDW_10`, `rainfall_interpolateIDW_20` and `rainfall_interpolateIDW_40` variables.
- `OpenRainER_radar.nc`: radar data in the OpenSense NetCDF format.

For this, we can't use an existing pysteps importer. Instead, read the data with `xarray.load_dataset` and convert it to a numpy array. The data should be in the format of a 3D numpy array with dimensions (time, x, y), where x and y are the spatial dimensions of the data. The metadata should be stored in a dictionary with the keys described previously.

Note that the data is provided in a latitude-longitude coordinate system with a slightly varying grid spacing. Usually pysteps expects data in a metric coordinate system with constant grid spacing. However, in this small domain we can treat the lat-lon grid as metric. Note that this will impact how spatial processing methods, such as upsampling and clipping the domain.

Other option is to reproject the data into a metric coordinate system with constant grid spacing.

## Visualize the data

The data can be plotted by using the methods in the [pysteps.visualization](https://pysteps.readthedocs.io/en/stable/pysteps_reference/visualization.html) module. Try different colorscales. Plot the data on top of a basemap with longitude-latitude lines and tick labels.

## Try different data processing methods

Pysteps implements various methods for preprocessing the input data. The most important of these include:

| **Functionality**                                               | **Purpose**                                                                                           |
| --------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- |
| upsampling (i.e. reducing spatial resolution)                   | needed for reducing computation time                                                                  |
| picking a smaller subrectangle from the input domain (clipping) | focus to the region of interest to reduce computation time                                            |
| conversion between different units                              | needed, for instance, for converting inputs to rain rate (mm/h, if not already in this unit)          |
| logarithmic transformation of rain rates                        | improve the reliability of optical flow and nowcasting methods                                        |
| normal quantile transformation                                  | needed for transforming the data to normal distribution (if the log-transformation is not sufficient) |

Experiment with the above functionality implemented in the [pysteps.utils](https://pysteps.readthedocs.io/en/stable/pysteps_reference/utils.html) module. When transforming the data values, visualize the transformation and/or analyze the impact on the data distribution.

Because the domain of the data is already small and the grid spacing is not constant, these methods may not be as useful as they would be for larger domains with constant grid spacing. Instead, you can test the methods using the "fmi" or "mch" datasets.
