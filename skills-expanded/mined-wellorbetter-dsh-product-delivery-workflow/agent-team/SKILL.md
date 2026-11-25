---
name: agent-team
description: Multi-agent team and swarm workflow for DeepSeek Harness using bounded subagents, parallel workflows, disjoint ownership, and independent review.
user-invocable: true
---

# Agent Team

Use DSH `subagent`, `subagent_fork`, and `workflow` to coordinate parallel work when delegation is explicitly requested or required by an active workflow.

Define the objective and independent workstreams. Keep the immediate blocking task local. Delegate only concrete, self-contained work with exact file ownership, inputs, outputs, acceptance checks, and prohibited actions. Tell workers they share the workspace and must not revert other edits. Use explorers for read-only investigation, workers for bounded implementation, reviewers for independent verification, and the parent agent as integrator. Do not duplicate work. Prefer fewer strong agents. Integrate results and validate the combined state.
