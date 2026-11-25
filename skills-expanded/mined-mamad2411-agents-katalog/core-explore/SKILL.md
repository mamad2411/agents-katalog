---
name: core-explore
description: Context-safe comprehension of a large/unfamiliar codebase — map first, scope to the task, fan out per-module readers that return compact summaries, so the orchestrator never holds the whole source and never runs out of context.
---

> **[Persona Directive]** Act as a **Staff Engineer onboarding to a large codebase under a deadline**. You answer a specific question (what to change for this task, how it connects, what's risky) — you do NOT read the whole repo.

Explore for: $ARGUMENTS

Use this when you must understand a **large or unfamiliar codebase** to plan or implement something — and reading it all would blow the context window. For explaining a single known file/function, use [core-explain](../core-explain/SKILL.md) instead.

## The core rule
**Never read the whole codebase into one agent's context.** Read a *map* and *summaries*, not raw source, at the orchestrator level. Raw source is read only by short-lived sub-readers that return a compact summary and are then discarded.

## Phase 1 — Map first (cheap, before any source)
1. Read the compressed indexes if they exist: `docs/SYSTEM_MAP.md`, `docs/DOMAIN_GLOSSARY.md`, and the **local `README.md`/`RULES.md`** of the directories in scope (progressive disclosure, per `AGENTS.md`).
2. If no map exists, build a lightweight one **without reading file bodies** — structure only:
   ```bash
   git ls-files | sed 's#/[^/]*$##' | sort -u | head -60      # directory map
   git ls-files | grep -E '\.(ts|js|py|go|rs|java)$' | wc -l  # size sense
   ```
   Use naming conventions (`*.controller.*`, `*.service.*`, `*.repository.*`) to infer responsibility from paths.

## Phase 2 — Scope to the task (don't read what you don't need)
From the map, pick **only the modules/paths relevant to `$ARGUMENTS`**. Locate entry points by symbol, not by reading files:
```bash
grep -rln "<symbol or route or table>" --include='*.{ts,js,py,go,rs}' | head -20
```
Write down the candidate slice (a handful of directories/files). Everything outside it is out of scope for this exploration.

## Phase 3 — Fan-out readers (one slice each → compact summary)
For each module/path in scope, spawn a **reader subagent** (spawn-subagents capability, [agent-tool-mapping](../../resources/agent-tool-mapping.md); tier `strong`). Each reader:
- reads **only its assigned slice** (one module/dir, or one large file),
- returns a **compact summary** — never the raw source — written to `.harness/reports/explore-<slice>.md`:
  - public interface (the few functions/types that matter),
  - inputs/outputs and key data flow,
  - what this slice depends on and what depends on it,
  - the exact files a change to `$ARGUMENTS` would touch, and gotchas.

The orchestrator reads **only the summaries** (pointers, per the file-based communication rule), never the slices' raw source. Run readers in parallel (cap ~8; batch the rest).

## Phase 4 — Recurse when a slice is still too big
If a reader reports its slice is too large to summarize safely, it **splits** the slice (by sub-directory or by symbol) and fans out again — summarize-then-discard at each level. Depth over width: never widen a single agent's reading to "just get it all".

## Output — a focused comprehension brief
Synthesize the summaries into one brief (to `docs/design-docs/<id>/exploration.md` if part of a feature):
1. **Files to change** for this task, and why each.
2. **How they connect** (the relevant slice of the architecture, not the whole map).
3. **Risks / blast radius** — what else depends on these paths.
4. **Open questions** for the user.

This brief — not the raw source — feeds planning. Keep `SYSTEM_MAP.md` updated with anything you learned so the next session pays the cost once.

## Hard rules
- Map and summaries at the top level; raw source only inside short-lived readers.
- Read the **slice the task needs**, not the whole tree.
- Compact summaries to files; pass pointers, not bodies.
- When a slice is too big, **recurse** — never widen.
