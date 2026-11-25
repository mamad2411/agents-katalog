---
name: team-workstream
description: Orchestrates multi-agent pipelines using Rapid or Formal workstream modes with parallel fan-out and cyclic feedback.
---
# Workstream Orchestration Skill Protocol

Use this skill to execute end-to-end multi-team workflows using either Rapid (async non-blocking) or Formal (blocking gated) configurations.

## Execution Workflow

1. **Parallel Dispatch**: `orchestration-dispatcher` dispatches tasks concurrently to specialized sub-agents.
2. **Feedback Aggregation**: `feedback-synthesizer` collects returning outputs, resolves conflicts, and formats delta prompts.
3. **Convergence Evaluation**: `convergence-checker` approves stage advancement when clean, or routes targeted feedback back to responsible teams.
4. **Rapid Shadow Audit**: In Rapid mode, `rapid-shadow-auditor` runs post-deploy background audits without blocking delivery.
