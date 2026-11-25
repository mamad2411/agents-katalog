---
name: edge-computing
description: "Edge computing paradigms: local inference, fog architectures, containerization (Docker, balena), latency optimization, and data preprocessing"
category: iot
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/iot/edge-computing/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Edge Computing Architectures

## Scope
Edge computing processes telemetry data locally at the network perimeter (gateways, edge devices) rather than transmitting raw streams to central cloud data centers.

## Architecture & Edge Deployment
- **Edge-to-Cloud Continuum**: Sensor Node $\to$ Edge Gateway $\to$ Fog Layer $\to$ Cloud Core.
- **Edge Data Preprocessing**: Time-series downsampling, anomaly detection, statistical aggregation, filtering out repetitive nominal data to reduce cellular/satellite bandwidth costs.
- **Containerization at the Edge**: Lightweight container runtimes (Docker, containerd, BalenaOS, K3s) for OTA application deployment and sandboxed modular services.

## Tools & Standards
- **Platforms**: AWS IoT Greengrass, Azure IoT Edge, BalenaCloud, EdgeX Foundry.
