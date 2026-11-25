---
name: wayfinder
version: "1.0.0"
description: "Chart a Goal too fogged for one session as a decision map in the active plan, settle one decision per session, then hand it to brainstorm lock. Use when grilling shows the work spans sessions."
license: MIT
argument-hint: "[destination, @file refs, or nothing to resume the map]"
compatibility: Designed for Claude Code
---

Lead with the destination and the next frontier.

Follow [references/wayfinder.md](references/wayfinder.md).

Resolve cross-stage transitions through the host's skill metadata; do not assume a shared installation parent. Resolve data paths from the consumer repository root. If a required skill or reference is unavailable, report the missing dependency and stop.

Defer to: `grill` for each HITL decision; `brainstorm` to lock the decided map; `work` only after that lock.
