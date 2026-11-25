---
name: token-budget
description: Token Budget (Grok Adapter). Grok-native port/adaptation. This skill provides the Token Budget capability. In Grok, many specialized skills are implemented via high-leverage patterns + meta skills + general-purpose agents. See bundled/skills and assignment matrix.
when-to-use: When the task involves Token Budget concepts, patterns, or workflows. Consult the agent-assignment-matrix for exact routing.
---

# Token Budget (Grok Adapter)

This is a Grok-native adapter skill created to achieve full catalog parity with the original 683+ skills surface while focusing real implementation on executable, high-leverage components.

## Role & Purpose
Token Budget patterns, best practices, and workflows.

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
- Relevant rules: research-confidence, tldr-cli, coding-style, phantom-mindset

This structure preserves the breadth of the original catalog in a maintainable, Grok-optimized way. For production work, prefer the mapped high-leverage implementations.
