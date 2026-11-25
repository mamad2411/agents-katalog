---
name: rendering
description: "Implement the rendering equation, Cook-Torrance microfacet specular reflectance, and GGX normal distribution."
category: graphics
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - graphics
  - rendering
  - pbr
  - brdf
  - ggx
---

# Physically Based Rendering (PBR) and Radiometry

## Overview & Core Principles
Implement the rendering equation, Cook-Torrance microfacet specular reflectance, and GGX normal distribution.

Evaluate rendering equation: $L_o = L_e + \int_{\Omega} f_r \cdot L_i \cdot (\omega_i \cdot n) d\omega_i$.
