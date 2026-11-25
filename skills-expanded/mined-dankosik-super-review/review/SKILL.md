---
name: review
description: Review readability and maintainability of Go, TypeScript, Rust, or Java PRs or local source with Super Review.
argument-hint: "<PR URL or local scope> [review aspects]"
disable-model-invocation: true
context: fork
agent: super-review:orchestrator
background: false
---

Use Super Review for this request: $ARGUMENTS

Read `${CLAUDE_PLUGIN_ROOT}/resources/super-review/SKILL.md`.
Follow its Claude adapter and return the report in this conversation. Accept a
PR, local changes, or explicitly requested whole-project source. For help, explain
usage without starting a review. For an actual review with no identifiable source,
ask only for the missing target; do not reacquire a target already given.
