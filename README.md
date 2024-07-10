# Landslide-Guardian

Landslide Prediction and SOS Alert System

This repository contains the code for a Landslide Prediction and SOS Alert System. The system leverages a trained machine learning model to predict landslide risks based on environmental parameters. It also includes functionality to fetch and analyze real-time data and trigger SOS alerts in case of emergency situations.
Landslide-Guardian, aims to provide a solution for dealing with landslide crises by developing a platform which triggers SOS in the form of sms and emails in case of landslide emergency on the basis of a machine learning model predicting landslides.

The repository includes the following files:

Landslide_prediction.py: This file contains the trained machine learning model for landslide prediction. It uses the LGBM(Light Gradient Boosting Machine) model to analyze input data and generate predictions regarding landslide risks. The model has been trained on historical landslide data and relevant environmental parameters.

fetch_data.py: This file is responsible for fetching and analyzing real-time data. It connects to various data sources, such as weather stations and rainfall sensors, to collect up-to-date information. The fetched data is then processed and fed into the trained model for landslide risk analysis.

app.py: This file implements the SOS alert system. It monitors the output of the landslide prediction model and triggers SOS alerts when high-risk areas or emergency situations are detected. The SOS alerts are sent through various communication channels, such as SMS or email, to relevant stakeholders and emergency response teams.
