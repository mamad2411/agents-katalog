---
name: "ML Experiment Tracker"
author: "exptrackr"
version: "1.0.0"
type: "tool"
category: "Machine Learning"
license: "MIT"
description: "Tracks ML experiments with metrics logging, model versioning, and comparison dashboards using MLflow/W&B"
tags:
  - tool
  - machine-learning
  - ai
  - automation
models:
  - gpt-4o
  - claude-3.5-sonnet
  - gemini-1.5-pro
parameters:
  temperature:
    type: number
    default: 0.7
    min: 0
    max: 2
    description: "Controls randomness in output generation"
  max_tokens:
    type: integer
    default: 4096
    min: 256
    max: 16384
    description: "Maximum number of tokens to generate"
  streaming:
    type: boolean
    default: false
    description: "Enable streaming output"
inputs:
  query:
    type: string
    required: true
    description: "Primary input for the skill"
  context:
    type: object
    required: false
    description: "Additional context for processing"
outputs:
  result:
    type: string
    description: "Primary output from the skill"
  metadata:
    type: object
    description: "Execution metadata including tokens used and latency"
---

# ML Experiment Tracker

Tracks ML experiments with metrics logging, model versioning, and comparison dashboards using MLflow/W&B

## Usage

This skill can be used standalone or as part of an Agent workflow on SkillsHub.

### Standalone

```
skillshub run exptrackr/ML-Experiment-Tracker --input "Your query here"
```

### In Agent

Add this skill to your Agent configuration to enable its capabilities.
