# Exercise 4: Nowcasting methods - Part 1 deterministic nowcasting

The purpose of this exercise is to illustrate how to construct, visualize and apply verification metrics to a deterministic nowcast using pysteps.
In this exercise you will construct your first nowcast using the data of the OpenSense training school, including radar and opportunistic datasets.

## Import data and perform the pre-processing steps

The starting point of this exercise are the processing steps you have taken in the previous exercises. Hence, make sure to load the training school data and do the pre-processing steps (transformations, derivation of advection fields, etc.). After these pre-processing steps, we are ready to construct our first nowcast.

## Deterministic nowcasts
In the deterministic nowcasting part, we will use the loaded data to create a precipitation nowcast and calculate different verification metrics to assess the skill of the nowcast compared to observations.

The first step is to make a nowcast using the **extrapolation** nowcasting method that simply extrapolates the last observed precipitation field along the motion field. You can follow the example in the [PySTEPS example gallery](https://pysteps.readthedocs.io/en/stable/auto_examples/plot_extrapolation_nowcast.html#sphx-glr-auto-examples-plot-extrapolation-nowcast-py). Calculate the nowcasts for 12 leadtimes, i.e. for 1 hour, and visualize some nowcasts with the observations. This approach is similar to what you already have done in [exercise_03](./exercise_03_optical_flow_and_extrapolation.md).

The semi-Lagrangian extrapolation method has some keyword arguments that can improve the quality of the nowcast depending on the data. For a full list of the arguments, see the [pySTEPS documentation](https://pysteps.readthedocs.io/en/latest/generated/pysteps.extrapolation.semilagrangian.extrapolate.html). Feel free to play with it!

If time allows, you can make nowcasts using other methods, for example S-PROG or LINDA (the deterministic version), which are more advanced nowcasting methods than just simple extrapolation. You can compare the nowcasts visually by plotting them and statistically by calculating the verification metrics for all the nowcasting methods and plotting them in the same figure (see below).

### Visualize the results
Visualize the observations and the nowcasts for a few lead times. An example on how to do this is provided in [the STEPS nowcast gallery example](https://pysteps.readthedocs.io/en/latest/auto_examples/plot_steps_nowcast.html#stochastic-nowcast-with-steps). You can plot the observations on one row and the corresponding nowcasts below them.

### Deterministic nowcast verification
Besides a visual inspection of your results, computing verification metrics will statistically show you the quality of the forecast(s) compared to the observations. Deterministic nowcasts can be verified with pySTEPS using different kind of metrics: continuous, categorical, spatial and SAL scores.

- `pysteps.verification.detcatscores` contains methods to calculate categorical metrics, i.e. metrics calculated for some rain rate thresholds, for example probability of detection (POD) and false alarm ratio (FAR).
- `pysteps.verification.detcontscores` contains methods to calculate continuous verification metrics, for example mean absolute error (MAE).
- `pysteps.verification.spatialscores` contains methods for calculating the Fractions Skill Score (FSS) and the Binary mean squared error (BMSE).
- `pysteps.verification.salscores` contains methods for calculating the Spatial-Amplitude-Location (SAL) score defined by Wernli et al. (2008)

Calculate the probability of detection (POD), false alarm ratio (FAR), equitable threat score (ETS), and the mean error (ME) for the nowcast as a function of leadtime, and visualize them.

## Create nowcasts and compare nowcasts with all training school datasets

Repeat the steps above to create nowcasts for all training school datasets (radar, PWS and CMLs) and visualize them all together. What can you say about the quality of the nowcasts with the different products?
