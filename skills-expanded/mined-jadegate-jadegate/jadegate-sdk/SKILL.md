---
name: jadegate-sdk
description: Protect AI agent tool calls with 2 lines of Python code. Auto-hooks into OpenAI/Anthropic SDK tool calls with zero configuration.
---

# JadeGate Python SDK

Protect AI agent tool calls with 2 lines of Python code. Auto-hooks into OpenAI/Anthropic SDK tool calls with zero configuration.

## When to Use

- User is building a Python AI agent and wants security
- User asks about protecting tool calls in code
- User wants to add security to their MCP client programmatically

## Usage

```python
import jadegate
session = jadegate.activate()          # All SDK tool calls now protected

# Optional: custom policy
jadegate.activate(policy="my-policy.json")
jadegate.activate(policy={"max_calls_per_minute": 30})

# Deactivate when done
jadegate.deactivate()
```

## Features

- Zero external dependencies
- Auto-hooks into OpenAI and Anthropic SDK tool calls
- Fully offline — no cloud, no telemetry
- Python 3.8+ compatible
