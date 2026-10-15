---
name: Inference
skill_id: inference
description: Guides model-serving and runtime-inference decisions across local, remote, and packaged deployment paths.
version: 1.0.0
source_kind: elephant-builtin
aliases: ["model inference", "serve a model", "run inference"]
trigger_phrases: ["help me serve this model", "set up inference for this model", "run local inference"]
keywords: ["inference", "serving", "latency", "throughput", "deployment", "runtime"]
category: mlops
---

# Inference

Use this built-in skill when the user needs to run, serve, benchmark, or operationalize model inference.

## Core rules

- Separate model choice, hardware fit, serving stack, and request pattern.
- Make latency, throughput, memory, and quality tradeoffs explicit.
- Inspect the real deployment target before recommending a stack.
- Prefer reproducible launch and benchmark steps over hand-wavy performance advice.

## Default workflow

1. Identify the model, hardware, traffic pattern, and latency target.
2. Choose the serving path that fits the deployment constraints.
3. Validate startup, request shape, batching, and resource usage.
4. Benchmark and tune only after the baseline path is stable.

## Guardrails

- Do not imply a model will fit on hardware you have not checked.
- Do not conflate prototype notebook inference with production serving.
- Do not quote performance numbers without workload context.
