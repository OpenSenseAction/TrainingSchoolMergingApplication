<img width="259" alt="image" src="https://github.com/user-attachments/assets/89f5527f-7373-4209-9bd8-f9570f1bd4e9" />


# Training School on Merging and Application of Opportunistic Rainfall Sensor Data

This repository contains all code, data and material for following sissions of the training school. 

## Introduction to OS datasets, processing tools and the working environment of the training school
We will present open datasets derived from CML, PWS, and SML data, and introduce the working environment of this training school. Processing methods will be briefly introduced to illustrate the challenges associated with data quality, uncertainties, and other complexities inherent to using opportunistic rainfall datasets. The main goal of this session is to explore and prepare the opportunistic and reference datasets, laying the foundation for the subsequent sessions.

## Merging of OS to rainfall products  
To leverage all available sensors, merging weather radar, rain gauge and OS data will be the main focus of this session. We will use the package mergeplg, which is developed within OpenSense. It consists of several methods to merge radar data with point (rain gauges, PWS) and line-based (CML, SML) rainfall data. Participants will learn techniques for handling line-based sensor information, such as applying a block kriging approach. Additionally, we will interpolate OS data using traditional methods like IDW (Inverse Distance Weighting) and ordinary kriging, enabling comparisons between these rainfall fields and those derived from radar merging. To visualize and validate the resulting rainfall maps and reference datasets we will use poligrain, a package designed to compare gridded, point and line-based rainfall data. 

## OS-based nowcasting with pysteps 
Nowcasting is a powerful tool for short-term forecasting of rainfall up to a few hours in the future. In this session, you will learn the basic principles of rainfall nowcasting and you will get hands-on experience in applying this yourself using the open-source Python nowcasting library pysteps. You will learn how to construct deterministic and ensemble nowcasts with gridded rainfall data from both radar and the OS datasets that were derived in the previous sessions. In addition, you will get experience with using pysteps for data preparation, visualization and verification of forecasts. 

## Hydrological modelling with OS data
Due to the high spatio-temporal variability of rainfall, correct precipitation estimates are still one of the major challenges in Hydrology. If correctly treated, OS data can complement standard precipitation observations and provide better rainfall estimates for hydrological models. In this session you will get hands-on experience with applying OS data to set-up and calibrated a simple hydrological model and learn how uncertainties in OS observations propagate into runoff simulations. You will learn how to reduce OS rainfall uncertainties when a calibrated hydrological model is available and how to use OS data in a data-driven manner.


## Mini project work
The final session will have minimal input from trainer side. You will have plenty of time to test the learned methods and tool on a research question defined by yourself. Either you use the datasets provided within the previous sessions or your own data. We will help you on the way to develop and implement your own project using OS.


