---
name: todo-llm-routing
description: Use when choosing a Claude Code or Codex model for todo-list work, translating Fable, Opus, Sonnet, or Haiku tiers to GPT models, or selecting reasoning effort.
---

# Cross-platform model routing

Route by capability tier first. Provider model names are implementations of the tier,
not part of a skill's behavior.

| Tier | Claude Code | Codex | Use for |
|---|---|---|---|
| `frontier` | `Opus 5.0`, max effort | `gpt-5.6-sol`, max effort | Security, payments, data integrity, concurrency, multi-repo architecture |
| `deep` | `Opus 5.0`, high effort | `gpt-5.6-sol`, high effort | Ambiguous design, unknown-cause debugging, cross-file refactors |
| `balanced` | `Opus 5.0`, medium effort | `gpt-5.6-sol`, medium effort | Well-scoped implementation, verification, visual generation |
| `fast` | `Opus 5.0`, low effort | `gpt-5.6-sol`, low effort | Mechanical edits, formatting, state updates, routine Git operations |

This is a workload mapping, not a claim that the models are identical. On Claude Code all
four tiers resolve to Opus and **reasoning effort is the only lever**; on Codex the tier picks
between two models (`sol` above, `terra` below) and an effort level. Sonnet, Haiku, and Fable
are never defaults — if Claude Code plan quota is tight, drop the tier rather than the model.

## When dispatching

1. Select the tier required by the task.
2. On Codex, use the table's model only when it appears in `codex debug models` or the model
   picker. If it is missing, use the closest model that is listed at the same effort. Do not
   guess availability from API docs.
3. Use the current host's model and effort from the selected table entry.
4. If the host cannot choose a model for a subagent, inherit the session model or run
   inline. Never invent unsupported model or tool parameters.
5. Keep user-selected models. Treat this table as the default only.
6. Review this dated mapping when either provider changes its model lineup, or when
   CursorBench publishes a new revision.

Mapping reviewed: 2026-07-25 against CursorBench 3.2.
