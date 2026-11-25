---
name: architecture-reviewer
description: Perform focused architecture and modularity reviews. Identify boundary violations, god objects, tangled dependencies, and propose the smallest reversible improvements. Use the repo-graph MCP when available. Trigger with "architecture review", "check the boundaries", "is this modular enough?".
version: 1.0.0
author: Cobus Greyling
---

# Architecture Reviewer

Keeps large codebases from turning into big balls of mud.

## Process

1. Get a structural view (use `repo-graph` MCP or manual exploration + subagents).
2. Map current modules and data flow.
3. Identify:
   - Unclear or violated boundaries
   - High coupling / low cohesion
   - Missing abstractions
   - Opportunities for ports/adapters or domain-driven splits
4. Propose the *smallest* change that meaningfully improves the situation.
5. Always pair recommendations with a plan (hand off to `plan-mode-orchestrator`).

## Output Format

- Current state summary (with diagram if possible)
- Specific problems with file/line evidence
- Recommended improvement + rationale
- Risk of the change
- How to verify the improvement (usually via tests + `repo-graph` diff)

## Ties to Other Skills
- Works extremely well after or with `subagent-arena`.
- Feeds directly into `plan-mode-orchestrator`.
- Use `security-audit` in parallel for security-relevant architecture work.
