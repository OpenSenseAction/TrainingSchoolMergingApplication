# Exercise 4: Nowcasting methods - Part 2 probabilistic nowcasting

The purpose of this exercise is to illustrate how to construct, visualize and apply verification metrics to a probablistic (ensemble) nowcast using pysteps. The setup of this exercise is fairly similar to [exercise_04](./exercise_04_deterministic_nowcasting.md), but instead of a deterministic nowcast, we will construct an ensemble nowcast with 10 ensemble members using the STEPS model.

## Import data and perform the pre-processing steps
The starting point of this exercise are the processing steps you have taken in the previous exercices. Hence, make sure to load the training school data and do the pre-processing steps (transformations, derivation of advection fields, etc.). After these pre-processing steps, we are ready to construct our first nowcast.

## Construct the probabilistic nowcasts
In this probabilistic nowcasting part, we will repeat the same basic steps of a deterministic nowcast, but, instead of a deterministic forecast, we will construct and verify a probabilistic STEPS nowcast with 10 ensemble members. We can get an estimate of the uncertainty in our forecast with a probabilistic forecast. It can, for instance, tell us what the (forecast) probability is that rainfall above a certain threshold will take place at location *x*.

The first step is to make a probablistic nowcast using the STEPS approach that is explained in [the STEPS nowcast gallery example](https://pysteps.readthedocs.io/en/latest/auto_examples/plot_steps_nowcast.html#stochastic-nowcast-with-steps). You can follow this example and adjust the code where necessary to make it work for our test case.

Make an ensemble nowcast with 10 ensemble members and 4 lead times of 15 min (one hour in total). You can follow the aforementioned gallery example. For a list of all options when configuring the STEPS nowcast, see the [pysteps documentation](https://pysteps.readthedocs.io/en/latest/pysteps_reference/nowcasts.html#pysteps-nowcasts-steps).

### Visualize the result
Visualize the observations, ensemble mean of the probabilistic nowcast and some individual ensemble members of the nowcast for a few lead times. As a second step, also visualize the probability of exceeding a threshold of 1 mm/h (try some others, too!) for the same lead times.

An example on how to do this is provided in [the STEPS nowcast gallery example](https://pysteps.readthedocs.io/en/latest/auto_examples/plot_steps_nowcast.html#stochastic-nowcast-with-steps). Start with plotting the observations and continue from there with the other plots below it.

What can you say about the quality of the forecast and how do the individual ensemble members compare to the ensemble mean?

### Ensemble forecast verification
You have probably seen that the individual ensemble members from the stochastic forecast maintain the same variance as the observed rainfall field. Hence, it gives a less smoothed outcome than the ensemble mean (which looks more like S-PROG in the deterministic nowcast section of this exercise) and also preserves high-intensity rainfall cells. Rainfall forecasts are uncertain on the high spatial and temporal resolution that we want to reach with nowcasting. Therefore, it is highly valuable to take into account an ensemble forecast that provides an estimate of this uncertainty. To verify such an ensemble forecast, it is only fair to use a verification strategy that takes into account the entire ensemble and that threats all members individually. Hence, this verification section will be different from the deterministic nowcast verification.

Pysteps includes a number of verification metrics to help users to analyze the general characteristics of the nowcasts in terms of consistency and quality (or goodness). In contrast to the verification of the deterministic nowcast, we have a 10-member ensemble that we want to verify. As every member contains valuable information, it is better not to use the deterministic verification metrics on the ensemble mean, but to use a metric that can take the entire ensemble into account.

Therefore, we will focus on the CRPS (continuous ranked probability score) and we will verify our probabilistic forecasts using the ROC curve, reliability diagrams, and rank histograms, as implemented in the [verification module](https://pysteps.readthedocs.io/en/latest/pysteps_reference/verification.html) of pysteps.

- You can see the [CRPS](https://pysteps.readthedocs.io/en/latest/generated/pysteps.verification.probscores.CRPS.html#pysteps.verification.probscores.CRPS) as the mean absolute error of the ensemble. It compares the cdf of the ensemble with the observed rainfall. Calculate and plot the CRPS for the lead times of your forecast. What do you see?
- Plot the ROC curve, reliability diagram and rank histogram following the [gallery example](https://pysteps.readthedocs.io/en/latest/auto_examples/plot_ensemble_verification.html#sphx-glr-auto-examples-plot-ensemble-verification-py). What can you say about the quality of your ensemble forecast?
