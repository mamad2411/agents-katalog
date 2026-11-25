---
name: distributed-inference-orchestrator
description: Manage AI processing across multiple global GPU providers.
---

# Distributed Inference Orchestrator

This skill manages the 'Brain Latency' of the system by routing AI queries to the closest or cheapest GPU provider (RunPod, Lambda, AWS) in real-time.

## Instructions
1. Monitor live prices and queue times for 5+ GPU cloud providers.
2. Implement 'Failover' logic: if Provider A is slow, route to Provider B.
3. Use 'Load Balancing' to handle bursts of 10,000+ simultaneous AI requests.
4. Optimize cold-start times for custom model weights.

## Examples
- "Route all non-urgent 8K video renders to the cheapest available GPU node globally."