---
tags: [backend, service, discovery, replica, leader, tracking]
name: service-discovery-replica-leader-tracking
description: Track Eureka replica UP/DOWN events and emit ServiceLeaderElected / ServiceReplicaAllDown Spring events for cluster-aware init
trigger: Microservice needs to react when the cluster gains its first live peer, loses its last peer, or the leader changes — not just on startup
category: backend
source_project: lucida-report
version: 1.0.0
---

# Discovery-driven replica & leader events

See `content.md`.
