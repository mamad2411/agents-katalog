---
name: learn
description: Project-learning management for Codex. Use when the user wants to capture, review, prune, or export recurring patterns, preferences, and pitfalls across sessions.
---

# Learn

Use this skill when the repo should retain what it has learned instead of rediscovering the same patterns every time.

This port is adapted from `garrytan/gstack` at commit `4d2c8d94d00cc4f4f3d4c26316a4f939ceedc045`.

## Important Adaptation

Upstream gstack keeps a dedicated learnings layer. In this repo, the closest durable equivalents are:

- `brain-ops`
- `query`
- `signal-detector`
- `reports`

## Workflow

1. Find the existing learning or related context first.
2. Add or update only durable patterns:
   - preferences that repeat
   - pitfalls that recur
   - repo-specific decisions worth remembering
3. Prune stale or contradicted learnings when the user asks.
4. Export or summarize the current learnings cleanly when needed.

## Guardrails

- Do not promote one-off observations into durable learnings too quickly.
- Keep the learning tied to evidence or repeated behavior.
- Prefer updating an existing learning over duplicating the same point.
