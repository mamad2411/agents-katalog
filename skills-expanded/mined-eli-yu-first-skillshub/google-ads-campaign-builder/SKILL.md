---
name: "Google Ads Campaign Builder"
author: "adsai"
version: "1.0.0"
type: "workflow"
category: "Marketing & SEO"
license: "MIT"
description: "Creates Google Ads campaigns with keyword groups, ad copy variations, and bidding strategy recommendations"
tags:
  - workflow
  - marketing-&-seo
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

# Google Ads Campaign Builder

Creates Google Ads campaigns with keyword groups, ad copy variations, and bidding strategy recommendations

## Usage

This skill can be used standalone or as part of an Agent workflow on SkillsHub.

### Standalone

```
skillshub run adsai/Google-Ads-Campaign-Builder --input "Your query here"
```

### In Agent

Add this skill to your Agent configuration to enable its capabilities.
