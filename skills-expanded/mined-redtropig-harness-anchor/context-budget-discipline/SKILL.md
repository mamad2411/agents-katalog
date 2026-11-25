---
name: context-budget-discipline
description: Use when sessions run long, adding subagents, fetching large files, or planning context-heavy work. SELECT/WRITE/COMPRESS/ISOLATE discipline.
---

# Context Budget Discipline

Context is a finite resource. Every token competes for the model's attention. The "lost-in-the-middle" phenomenon is real — content buried in 50% of the window position is least attended.

This skill applies four operations to keep the budget sane.

## The Four Operations

```
SELECT     load context just-in-time, not all-at-once
WRITE      persist to disk; let the filesystem remember, not chat
COMPRESS   summarize older turns when window fills
ISOLATE    delegate so child work doesn't pollute parent context
```

### SELECT — pull, don't push

Default behaviour: don't preemptively load files. Wait until they're needed.

- ❌ "Let me read all 30 .cpp files to understand the project."
- ✅ "I'll consult PROJECT-TOC.md first, then read only the 2 files the task touches."

### WRITE — disk is cheap, context is expensive

Anything reusable across turns should live on disk:

- Active feature → `feature_list.json`
- Decisions / rationale → `progress.md` or `docs/decisions/`
- "What I just did" → `session-handoff.md`

Anti-pattern: re-explaining the same plan/decision in every reply.

### COMPRESS — summarize old turns when window pressure rises

When context usage > 70% of model window, mid-session compaction can help. But per [Anthropic Nov 2025](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents):

> "Compaction preserves continuity, but doesn't give the agent a clean slate. Context anxiety can still persist."

**Flush before you compress.** Before compaction/reset — or when the PostToolUse watermark fires (T1 "Context is filling" = flush now; T2 "Context is heavily filled" = wrap up via /session-end + fresh session) — write chat-only durable memory to disk first: golden-rule stubs
(`capturing-golden-rules`), feature status, a milestone `progress.md` entry. After a compaction,
do NOT backfill memory from the summary: reconstruct from on-disk evidence (git diff, test
output, progress.md) and state uncertainty where evidence is missing.

If compaction isn't enough → use `/session-end` to write a rich handoff, then suggest the user start a **fresh context** (context reset > compaction for long runs).

### ISOLATE — child work doesn't bleed up

Subagents (`/verify`, `cpp-build-doctor`, etc.) run in **fresh context**. They:
- Don't inherit conversational baggage
- Return a fixed-structure result (diagnosis / evidence / recommendation)
- Don't dump their working notes into your context

If you delegate a noisy task, ask for a SUMMARY back, not a transcript.

## Token Budget Reference

| Tier | Budget | Source |
|---|---|---|
| Tier 1 (always loaded) | ~3000 tokens cap; measured at v0.10.0: generic ≈1160 t, C/C++ ≈1580 t | SessionStart hook injection (hard-capped 12000 chars, meta-skill injected slimmed; `${CLAUDE_PLUGIN_ROOT}/scripts/measure-context.sh` re-measures both baselines) |
| System prompt + tools | Model-defined | Outside your control |
| Working context | Most of remaining window | Your edits + reads accumulate here |

## State-file budgets

Hot state files carry fixed budgets. The SessionStart banner warns (warn-only) when one is
exceeded; `/session-end` offers deterministic archival via `state-archive.mjs`.

| File | Hot window | Sentinel |
|---|---|---|
| `progress.md` | newest 20 sections | 64KB |
| `feature_list.json` | live features + 10 newest `pass` | 32KB |
| `golden-rules.md` | prune — never archived | 8KB |
| `AGENTS.md` | keep it a map (~80 lines) | 8KB |
| `session-handoff.md` | overwritten each session | 4KB |

Archives (`progress-archive.md`, `feature_archive.json`) are grep-only — never load whole.

## When to invoke this skill

- A session has been going for >2 hours
- You notice your replies summarizing already-discussed content (you're losing focus)
- About to read a large file (>500 lines) — ask: do I need ALL of it?
- About to dispatch a subagent — confirm it returns summary, not log
- Context monitor / Claude Code warns about token usage

## Practical moves

When budget pressure rises:

1. **Stop and write handoff.** Run `/session-end` if features are in flight.
2. **Hard-truncate reads.** Prefer `head -50`, `grep -A 5`, line range in Read tool — over reading whole files.
3. **Drop tool definitions.** If you have many MCP tools loaded and none are relevant to current work, that's overhead — but you can't control this from inside the session.
4. **Consider context reset.** A fresh session with rich handoff often outperforms continuing a stale one.

## Calibrated estimates

You can roughly estimate context use by:

- 1 token ≈ 4 chars (English) or 1-2 chars (Chinese)
- A 200-line code file ≈ 1500-2500 tokens
- A medium SKILL.md ≈ 1000-2000 tokens
- Your own multi-paragraph replies ≈ 200-500 tokens each

When the user asks "how much room do we have?", be honest about the estimate.

## Looking up context engineering research

For specific patterns (e.g., compaction algorithms, attention windowing, RAG indexing strategies) — invoke the `docs-lookup` skill. Pattern names evolve fast in this area; don't rely on memory.

Typical entry query: `context engineering 2026` or `<specific technique> llm`.

## Related

- `using-harness-anchor` — Tier 1 injection budget reference
- `feature-state-keeper` — what to write to disk
- `project-indexing` — TOC as compressed file index
