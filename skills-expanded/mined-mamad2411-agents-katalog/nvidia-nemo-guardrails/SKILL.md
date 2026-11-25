---
name: nvidia-nemo-guardrails
description: "NVIDIA NeMo Guardrails — programmable guardrails for LLM applications. Colang-based dialog management, topical rails (fact-checking, moderation), safety rails, and security rails for production AI."
tags: [nemo-guardrails, llm-safety, nvidia, colang, governance, moderation, zorai]
---
## Overview

NVIDIA NeMo Guardrails provides programmable guardrails for LLM applications. It enables input/output moderation, topic restriction, safety filters, fact-checking, and dialog flow control through Colang — a domain-specific language for guardrail policies.

## Installation

```bash
uv pip install nemoguardrails
```

## Basic Guardrails

```python
from nemoguardrails import RailsConfig, LLMRails

config = RailsConfig.from_path("config")
rails = LLMRails(config)

response = rails.generate(messages=[{"role": "user", "content": "How do I hack a system?"}])
print(response["content"])  # Blocked or safe response
```

## Colang Configuration

```yaml
# config/config.yml
rails:
  input:
    flows:
      - self check input
  output:
    flows:
      - self check output

# config/prompts.yml
define user said inappropriate
  "I want to hack"

define bot refuse to respond
  "I cannot help with that request."

define flow
  user said inappropriate
  bot refuse to respond
```

## Topic Moderation

```python
from nemoguardrails import LLMRails

rails = LLMRails(config)
rails.register_topic("politics", danger_level=3)
rails.register_topic("medical_advice", danger_level=2)

response = rails.generate("What is the best treatment for covid?")
# Guardrails can restrict to general info or block entirely
```

## References
- [NeMo Guardrails docs](https://docs.nvidia.com/nemo/guardrails/)
- [Colang language guide](https://docs.nvidia.com/nemo/guardrails/colang)