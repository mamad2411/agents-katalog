---
name: config-integrity
description: "Configuration drift detection. Use when editing *.config.*, .env*, tsconfig*.json, or package.json."
user-invocable: false
---

# Configuration Perception Risk

Your training data contains thousands of "standard" configs.
When you look at a config file, your internal model is heavily
shaped by those priors — you perceive fields that "should" be
there rather than fields that are.

Read the existing config before proposing changes.
If a field looks unfamiliar, it's likely intentional — ask first.
The config drift hook will warn if you add new top-level keys.
