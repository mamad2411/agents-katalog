---
name: grill
version: "1.0.0"
description: "Grill a fuzzy idea or a plan, one round of decisions at a time, until the Goal could lock. Writes nothing. Use for grill/interview/stress-test requests and before locking an unclear Goal."
license: MIT
argument-hint: "[raw] [idea, @file refs, or plan path]"
compatibility: Designed for Claude Code
---

Lead with the next round of questions, not a summary.

Resolve the mode, then follow [references/grill.md](references/grill.md).

Resolve cross-stage transitions through the host's skill metadata; do not assume a shared installation parent. Resolve data paths from the consumer repository root. If a required skill or reference is unavailable, report the missing dependency and stop.

Defer to: `brainstorm` to lock or refine the result; `wayfinder` when the decisions span sessions.
