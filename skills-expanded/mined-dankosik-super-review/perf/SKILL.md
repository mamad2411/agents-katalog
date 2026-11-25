---
name: perf
description: Find work that Go, TypeScript, Rust or Java source of a PR or local tree does not need on its hot paths, by reading it, with Performance Review.
argument-hint: "<PR URL or local scope> [files, lenses, hot paths, profile]"
disable-model-invocation: true
context: fork
agent: super-review:perf-orchestrator
background: false
---

Use Performance Review for this request: $ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/resources/perf-review/SKILL.md`.
Follow its Claude adapter and return the report in this conversation. Accept a
PR, local changes, or explicitly requested whole-project source. For help, explain
usage without starting a review. For an actual review with no identifiable source,
ask only for the missing target; do not reacquire a target already given.
