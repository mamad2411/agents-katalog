---
name: dsp-algorithm-design
description: Design and review digital signal processing pipelines including sampling, filtering, transforms, detection, estimation, feature extraction, fixed-point concerns, and implementation tradeoffs. Use when developing or debugging DSP methods for communications, sensing, audio, imaging, robotics, or embedded systems.
---
# DSP Algorithm Design

Use this skill when a signal-processing idea needs to become a testable pipeline.

## Core Workflow

1. Define the signal model, sampling assumptions, and noise sources.
2. Specify inputs, outputs, latency limits, and implementation platform.
3. Break the pipeline into estimation, filtering, transform, and decision stages.
4. Check numerical range, precision, and aliasing before tuning parameters.
5. Validate with synthetic, boundary, and real-world signals.

## Execution Rules

1. Make units explicit.
2. Keep simulation assumptions separate from deployment assumptions.
3. Treat calibration and synchronization as part of the algorithm, not cleanup.
4. When fixed-point or embedded deployment matters, quantify the error budget.

## Output Contract

Return:

1. Signal model.
2. Pipeline stages.
3. Key equations or update rules.
4. Validation plan.
5. Numerical and implementation risks.
