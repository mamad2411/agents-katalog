---
name: "Category Taxonomy Builder"
author: "taxoai"
version: "1.0.0"
type: "tool"
category: "E-commerce"
license: "MIT"
description: "Builds product category taxonomies with attribute mapping, filter configurations, and breadcrumb structures"
tags:
  - tool
  - e-commerce
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

# Category Taxonomy Builder

Builds product category taxonomies with attribute mapping, filter configurations, and breadcrumb structures

## Usage

This skill can be used standalone or as part of an Agent workflow on SkillsHub.

### Standalone

```
skillshub run taxoai/Category-Taxonomy-Builder --input "Your query here"
```

### In Agent

Add this skill to your Agent configuration to enable its capabilities.
