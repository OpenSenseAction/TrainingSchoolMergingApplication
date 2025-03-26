# OpenSense 2025 Training School Nowcasting Session

Training instructors: Jenna Ritvanen (Finnish Meteorological Institute) and Ruben Imhoff (Deltares)

This folder contains the material prepared for the hands-on session on using pysteps with opportunistic sensing data.
The exercises are split into a folder [exercises](./exercises), containing the description and steps to be taken per exercise, and a folder [notebooks](./notebooks), which contain the notebooks that can be used for each exercise and that should be filled out further by you. In addition, this folder also contains the sub folder [solutions](./notebooks/solutions), which provides the solution to the exercices. The attendees are encouraged to try the exercises first before looking at the solutions.

## General information
  * Information about the training school can be found [here](https://indico.scc.kit.edu/event/4626/overview).
  * The session has some PPT slides that we use for the introduction and wrap up of the different exercises. You can find these PPT slides in the folder [presentations](./presentations).

## About the exercices
The exercises are divided into 4 blocks:

1. Install pysteps and its dependecies (you have probably already done so when setting up the environment for the training school), see [exercise_01](./excercises/exercise_01_local_conda_setup.md).
2. Read, visualize and process input data, see [exercise_02](./excercises/exercise_02_input_data.md).
3. Optical flow and extrapolation, see [exercise_03](./excercises/exercise_03_optical_flow_and_extrapolation.md).
    * [Optional] Advection correction of the gridded rainfall fields for accumulation, see [exercise_03a](./excercises/exercise_03a_advection_interpolation.md). If time allows, you can try out this exercise.
4. Creating your first nowcasts with the (opportunistic) dataset, see [exercise_04](./excercises/exercise_04_deterministic_nowcasting.md).
    * [Optional] Creating a probabilistic (ensemble) nowcast with the same datasets, see [exercise_04a](./excercises/exercise_04a_probabilistic_nowcasting.md). If time allows, you can try out this exercise.
