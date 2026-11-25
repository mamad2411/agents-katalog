---
name: openclawforge-ai-model-assigner
description: >
  Use when assigning or optimizing AI models for OpenClaw agents, configuring model parameters
  (temperature, max_tokens), or adjusting model assignments based on task requirements.
---

# OpenClaw Model Assigner - OpenClaw AI Model Assignment & Optimization

## Overview
Assigns optimal AI models to OpenClaw agents based on task complexity, performance requirements, and cost considerations. Works alongside the Agent Creator and SQLite Manager to ensure every agent has an appropriate model assigned for their specific role. Model configuration data is stored in the SQLite database on `srv1628373.hstgr.cloud`.

## Capabilities
- **Model Selection**: Choose optimal AI models (e.g., GLM-5.1, Claude, GPT-4) based on agent task requirements
- **Parameter Configuration**: Set temperature, max_tokens, and other model parameters per agent
- **Assignment Prioritization**: Configure primary vs. fallback model assignments
- **Cost Optimization**: Balance model capability against monthly budget constraints

## When to Use
- When assigning a model to a newly created agent
- When optimizing model performance or cost for existing agents
- When updating agent model parameters (temperature, max_tokens)
- When configuring primary and fallback model assignments

## Platform Context
- **VPS Hostname**: `srv1628373.hstgr.cloud`
- **Database**: SQLite on the VPS (model assignments persisted there)
- See `infrastructure/vps-infrastructure.md` for detailed knowledge