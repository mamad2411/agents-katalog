---
name: brainstorm
version: "6.0.0"
description: "Explore trade-offs and lock the Goal into `.monows/plans/active/{slug}.md`, including a decided `wayfinder` map. Use for ideation, architecture decisions, and RFC/PRD-to-spec work."
license: MIT
argument-hint: "[explore|lock|refine] [idea, @file refs, plan path, or trade-off question]"
compatibility: Designed for Claude Code
---

Lead with the recommendation, then the key trade-off.

Resolve the mode, then follow [references/brainstorm.md](references/brainstorm.md) (`.monows/WORKFLOW.md` IF routing is unclear).

Resolve cross-stage transitions through the host's skill metadata; do not assume a shared installation parent. Resolve data paths from the consumer repository root. If a required skill or reference is unavailable, report the missing dependency and stop; retained legacy playbooks are not a fallback.

Defer to: `grill` for fuzzy intent, `wayfinder` for decisions that span sessions; `to-plan` after an approved high-risk lock, `work` after a normal one; `check` for quality gates after implementation.
