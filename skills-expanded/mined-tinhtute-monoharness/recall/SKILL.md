---
name: recall
version: "5.0.0"
description: "Rebuild working context from Git, the plan, recent transcripts and merged PRs into a cited brief; `state` is Git and plan only, `deep` adds subagents and MCP sources. Use for 'where did I leave off'."
argument-hint: "[state | deep] [<topic>] [window]"
compatibility: Designed for Claude Code
---

Lead with the capsule (`recall state`: branch state and readiness).

Follow [references/recall.md](references/recall.md) (`.monows/WORKFLOW.md` IF routing is unclear). This stage stays read-only.

Resolve cross-stage transitions through the host's skill metadata; do not assume a shared installation parent. Resolve data paths from the consumer repository root. If a required skill or reference is unavailable, report the missing dependency and stop; retained legacy playbooks are not a fallback.

Defer to: `handoff` writes resumable state; `check` runs the actual gate; `git` handles Git operations; `brainstorm` starts new work.
