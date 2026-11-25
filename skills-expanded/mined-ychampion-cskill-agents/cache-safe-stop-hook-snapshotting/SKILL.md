---
name: cache-safe-stop-hook-snapshotting
description: "Persist a cache-safe stop-hook context snapshot only for main session queries so later helpers can resume from stable state without fork pollution."
metadata:
  author: ychampion
---

# SKILL: Cache-Safe Stop-Hook Snapshotting
**Domain:** context-management  
**Trigger:** Apply when end-of-turn hooks need to persist enough state for follow-up helpers, but background forks must not overwrite the main session snapshot.
**Source Pattern:** Distilled from reviewed context, compaction, and memory-governance patterns.

## Core Method
Build one structured hook context at turn end, then persist a cache-safe snapshot only when the query source belongs to the main interactive session or the SDK control path. This gives downstream helpers a stable resume surface while preventing side agents and background forks from clobbering shared state with their own narrower contexts. The snapshot gate lives outside optional prompt-suggestion features so every consumer that depends on the shared state still gets it.

## Key Rules
- Create the snapshot from the full stop-hook context, not ad hoc fragments, so later consumers see the same system, user, and tool state.
- Gate snapshot persistence to the authoritative query sources such as `repl_main_thread` and `sdk`.
- Keep forked or background agents out of the shared snapshot path; their contexts are partial and will pollute resume behavior.
- Decouple snapshotting from optional background features so state persistence remains available even when prompt suggestions are off.

## Example Application
If a REPL turn finishes and `/btw` or another side-question helper may run next, save a cache-safe snapshot from the main turn’s hook context. If a background memory extractor reaches the same stop-hook code, skip the snapshot so the main session state remains authoritative.

## Anti-Patterns (What NOT to do)
- Do not let every subagent write to the same cache-safe snapshot location; later helpers will resume from polluted or incomplete context.
- Do not tie snapshot persistence to an unrelated feature flag when multiple consumers depend on it.
