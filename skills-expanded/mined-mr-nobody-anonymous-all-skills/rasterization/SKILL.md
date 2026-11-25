---
name: rasterization
description: "Implement barycentric coordinate triangle interpolation, depth buffer testing, and sub-pixel edge equations."
category: graphics
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - graphics
  - rasterization
  - depth-buffer
  - barycentric
---

# Software Rasterizer Pipeline & Scanline Algorithms

## Overview & Core Principles
Implement barycentric coordinate triangle interpolation, depth buffer testing, and sub-pixel edge equations.

Perform perspective-correct attribute interpolation: $A = \frac{A_0/w_0 \lambda_0 + A_1/w_1 \lambda_1 + A_2/w_2 \lambda_2}{1/w_0 \lambda_0 + 1/w_1 \lambda_1 + 1/w_2 \lambda_2}$.
