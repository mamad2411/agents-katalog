---
name: "Model Explainability Tool"
author: "explainai"
version: "1.0.0"
type: "tool"
category: "Machine Learning"
license: "MIT"
description: "Generates model explanations using SHAP, LIME, and feature importance with visual interpretations"
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

# Model Explainability Tool

Generates model explanations using SHAP, LIME, and feature importance with visual interpretations

## Usage

This skill can be used standalone or as part of an Agent workflow on SkillsHub.

### Standalone

```
skillshub run explainai/Model-Explainability-Tool --input "Your query here"
```

### In Agent

Add this skill to your Agent configuration to enable its capabilities.
