---
name: image-processing
description: "Implement separable Gaussian blurs, Sobel edge detectors, tone mapping (ACES), and color grading LUTs."
category: graphics
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - graphics
  - image-processing
  - filters
  - lut
  - aces
---

# GPU-Accelerated Image Processing & Filtering

## Overview & Core Principles
Implement separable Gaussian blurs, Sobel edge detectors, tone mapping (ACES), and color grading LUTs.

Utilize 2-pass 1D convolution kernels to reduce complexity from $O(K^2)$ to $O(2K)$.
