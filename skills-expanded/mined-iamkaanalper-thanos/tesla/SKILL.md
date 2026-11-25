---
name: tesla
description: Tesla (Grok Adapter). Grok-native port/adaptation for the /tesla usage guide command (formerly /hizir). This skill provides the Tesla / help command capability. In Grok, many specialized skills are implemented via high-leverage patterns + meta skills + general-purpose agents. See bundled/skills and assignment matrix.
when-to-use: When the task involves the /tesla command, usage guide, Hizir/Tesla identity patterns, or help workflows. Consult the agent-assignment-matrix for exact routing.
---

# Tesla (Grok Adapter)

This is a Grok-native adapter skill created to achieve full catalog parity with the original skills surface while focusing real implementation on executable, high-leverage components. The /tesla command is the main entry point for the usage guide (powered by tesla-identity rule + docs).

## Role & Purpose
Tesla (/tesla command) patterns, best practices, and workflows (the interactive help / identity for the AI software team).

## Grok Implementation Strategy
- Real heavy lifting is done by:
  - Existing dedicated skills in .grok/skills/ or .grok/bundled/skills/ (e.g. similar patterns skills)
  - Bundled meta skills (implement, swarm, preflight, compound-learnings, memory-palace, layered-recall, test-enforcement, etc.)
  - General-purpose agent + relevant agent from .grok/bundled/agents/
  - Direct use of tldr, explore, or MCP tools where applicable
- This adapter file ensures the role name exists and provides guidance + references.

## Production Contract (Mandatory for all usage)
- Record significant uses/decisions to ledger via task_lifecycle.
- Use structured handoff for any multi-step work.
- Run preflight for non-trivial tasks.
- Capture friction for self-improvement.
- Participate in compound flywheel.
- Follow claim-verification (two-pass: hypothesize then read actual files).

## When to Activate
See the Grok agent-assignment-matrix.md and proactive-delegation rules. Many original skills map to a smaller set of powerful Grok primitives.

## References & Related
- .grok/docs/agent-assignment-matrix.md
- .grok/bundled/skills/ (core meta + patterns)
- .grok/skills/ (high-leverage ports)
- Relevant rules: research-confidence, tldr-cli, coding-style, phantom-mindset, tesla-identity

This structure preserves the breadth of the original catalog in a maintainable, Grok-optimized way. For production work, prefer the mapped high-leverage implementations. The /tesla command now serves the usage guide role.
