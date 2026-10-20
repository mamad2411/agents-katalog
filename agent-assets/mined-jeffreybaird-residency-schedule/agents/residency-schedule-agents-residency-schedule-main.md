# Repository instructions

Before working in this repository, read and follow
[.docs/project-guidance.md](.docs/project-guidance.md), the shared project rules
for both Codex and Claude, and its relevant supporting documents. Keep project
guidance there; keep this entry point equivalent to the other platform's file.

<!-- BEGIN MANAGED AGENT WORKFLOW -->
Shared native agent workflow version 2.0.0 applies to every behavior
change. This section supersedes legacy workflow, role-assignment, and blanket
test-edit approval instructions only. Preserve domain, privacy, coverage,
static-analysis, deployment, and project constraints. Follow [.docs/agent-workflow.md](.docs/agent-workflow.md) for role ownership,
red → accepted tests → implementation → green → independent review.
Accepted tests are a contract: only the test writer changes them when the
expected behavior changes, with renewed review. Never weaken tests to pass.
The orchestrator coordinates the pipeline. This hook restricts only direct source
and test edits; other files, tools and commands retain ordinary native permissions.
Do not use alternate editing routes to evade the source/test ownership workflow.
<!-- END MANAGED AGENT WORKFLOW -->
