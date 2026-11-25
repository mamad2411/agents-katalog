---
name: tests
description: Check whether the tests of Go, TypeScript, Rust or Java source in a PR or local tree would fail if a plausible bug appeared, with Test Review.
argument-hint: "<PR URL or local scope> [files, questions]"
disable-model-invocation: true
context: fork
agent: super-review:test-orchestrator
background: false
---

Use Test Review for this request: $ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/resources/test-review/SKILL.md`.
Follow its Claude adapter and return the report in this conversation. Accept a
PR, local changes, or explicitly requested whole-project source. For help, explain
usage without starting a review. For an actual review with no identifiable source,
ask only for the missing target; do not reacquire a target already given.
