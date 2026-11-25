---
name: model-validation
description: "Deploy models into shadow (dark) traffic mode and compare outputs against the incumbent champion model."
category: mlops
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - mlops
  - model-validation
  - shadow-deployment
  - champion-challenger
---

# Pre-Deployment Model Validation & Shadow Testing

## Overview & Core Principles
Deploy models into shadow (dark) traffic mode and compare outputs against the incumbent champion model.

Route 100% of live traffic asynchronously to candidate models without impacting end-user SLA latency.
