---
tags: [backend, k8s, health, via, getnodelist]
name: k8s-health-via-getnodelist
description: Use `listNode()` with readiness check for Kubernetes cluster health — `getVersion()` succeeds on degraded clusters that will fail real work
version: 1.0.0
source_project: cygnus
source_ref: cygnus@cbb96a6dfff
category: backend
triggers:
  - cluster liveness probe before running a collector pass
  - guard against API-server flaps
linked_knowledge:
  - k8s-clusterrole-aggregation-npe
---

# Kubernetes Availability via getNodeList

See `content.md`.
