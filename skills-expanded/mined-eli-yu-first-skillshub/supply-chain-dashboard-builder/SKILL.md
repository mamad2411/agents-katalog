---
name: "Supply Chain Dashboard Builder"
author: "scm-visual"
version: "1.0.0"
type: "template"
category: "Supply Chain & Logistics"
license: "MIT"
description: "Build real-time supply chain dashboards with KPIs, alerts, and trend visualization"
tags:
  - template
  - supply-chain-&-logistics
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

# Supply Chain Dashboard Builder

Build real-time supply chain dashboards with KPIs, alerts, and trend visualization

## Usage

This skill can be used standalone or as part of an Agent workflow on SkillsHub.

### Standalone

```
skillshub run scm-visual/Supply-Chain-Dashboard-Builder --input "Your query here"
```

### In Agent

Add this skill to your Agent configuration to enable its capabilities.
