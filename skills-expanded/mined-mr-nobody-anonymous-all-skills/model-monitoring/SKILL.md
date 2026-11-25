---
name: model-monitoring
description: "Monitor production model latency, throughput, error rates, and track ground-truth delayed accuracy metrics."
category: mlops
author: AAS Platform
version: 1.0.0
disable-model-invocation: false
risk: low
source: authoring
tags:
  - mlops
  - monitoring
  - telemetry
  - prometheus
  - grafana
---

# Production ML Model Performance & Accuracy Telemetry

## Overview & Core Principles
Monitor production model latency, throughput, error rates, and track ground-truth delayed accuracy metrics.

Instrument OpenTelemetry spans to capture inference latency percentiles (P95, P99) and payload shapes.
