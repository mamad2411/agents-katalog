---
name: leeway-predict-observe-delta
description: Closes the simulation-to-reality loop by comparing predicted state with actual post-execution observations and routing model error into repair and learning.
license: MIT
---
# LeeWay Predict Observe Delta

Before execution preserve predicted observables and tolerances. After execution measure the same observables. Compute/describe delta by dimension, classify MODEL_ERROR, EXECUTION_ERROR, ENVIRONMENT_CHANGE, MEASUREMENT_ERROR or UNKNOWN, then repair/retest.

A correct-looking final output does not validate a bad model if prediction failed for hidden reasons. Learning requires preserving both prediction and observation.
