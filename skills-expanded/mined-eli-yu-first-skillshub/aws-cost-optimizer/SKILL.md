---
name: "AWS Cost Optimizer"
author: "costai"
version: "1.0.0"
type: "agent"
category: "DevOps & Cloud"
license: "MIT"
description: "Analyzes AWS billing and suggests cost optimization strategies for EC2, RDS, S3, and Lambda"
tags:
  - agent
  - devops-&-cloud
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

# AWS Cost Optimizer

Analyzes AWS billing and suggests cost optimization strategies for EC2, RDS, S3, and Lambda

## Usage

This skill can be used standalone or as part of an Agent workflow on SkillsHub.

### Standalone

```
skillshub run costai/AWS-Cost-Optimizer --input "Your query here"
```

### In Agent

Add this skill to your Agent configuration to enable its capabilities.
