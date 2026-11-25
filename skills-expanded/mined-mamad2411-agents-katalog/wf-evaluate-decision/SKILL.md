---
name: wf-evaluate-decision
description: Structured evaluation of an ADR-shaped decision between two named options, running a red-team pass, council review, and operator interview, ending in an Architecture Decision Record. Not for ordinary in-flight decisions. The Evaluate decision workflow.
---

# Evaluate a decision (Wavefoundry skill)

This skill is a thin pointer: the workflow lives in `docs/prompts/evaluate-decision.prompt.md`. Read that document and follow it; do not improvise the steps from this summary.

- The workflow is prompt-driven (no dedicated MCP tool) and ends in an Architecture Decision Record.
- Frame two specific options before running; a poorly framed question produces a confident but useless evaluation.
