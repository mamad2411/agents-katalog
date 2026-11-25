---
name: broken-skill
description: "Use when testing corrupted YAML
triggers: "unterminated string
---

# Broken

This file has a corrupted YAML frontmatter (unterminated quote, missing close). The miner should degrade gracefully — either treat as anomaly or skip entirely, but MUST NOT crash.
