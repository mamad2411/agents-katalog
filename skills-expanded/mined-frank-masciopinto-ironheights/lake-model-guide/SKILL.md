---
name: lake-model-guide
description: Run a 1D lake temperature model, understand its input files and change configuration parameters.
---

# Lake Model Guide

## Optional: station temperature offset

Some users correct station air temperature for the difference between the station and the air over the lake. This guide does not ship an offset value.

If the user gives you an offset and the source for it, write a corrected copy to `inputs/weather_corrected.csv`, keep the original file unchanged, point the configuration at the copy, and tell the user the value, its source and which file the run used. Without a user-supplied value, use the original file as is.

## Running the model

Run the model from the folder that holds the configuration file. Results are written to `output/`.

## Tips

- Back up the configuration file before changing parameters.
- Compare simulated surface temperature with observations to judge fit.
