---
name: docs-ship
description: "[OMCP] Run repository docs checks and emit explicit evidence before completion."
orchestrates-agents: "document-specialist, reviewer, verifier"
---

# [OMCP] Docs Ship

Use this skill when a task modifies docs, prompts, instructions, agents, or
example layouts.

## Agent orchestration

This skill coordinates `document-specialist` for docs surface quality,
`reviewer` for scope and parity drift, and `verifier` for concrete validation
evidence.

## Run

```bash
./skills/docs-ship/run-docs-checks.sh
```

## Goal

- prefer concrete validation output over “looks good”
- run local repo validation if present
- otherwise run parity-guard and basic file checks
