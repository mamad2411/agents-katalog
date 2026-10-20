---
name: graphify-recurring-bugs
description: Use during root-cause investigation of any bug in a project that has graphify-out/graph.json — surfaces related code before grepping, flags likely duplicates of existing KNOWN_ISSUES.md entries before filing a new one, and when a match lands on a resolved entry surfaces its recorded fix so a known-good fix can be reused. No-op in any project without a built graph.
---

# Graphify-Aware Recurring Bugs

## Overview

A stack trace shows where a bug surfaced, not everywhere its root cause reaches. Grepping around
the crash site misses related call sites that share the same underlying problem — which is exactly
how the same root cause gets logged as three unrelated "new" bugs over time. `graphify` already
builds a queryable structural map of a codebase; this skill puts that map to work specifically
during bug investigation, not just general code Q&A.

**Core principle:** a recurring bug should be recognized as recurring — and its known-good fix
reused — not re-discovered as new. graphify is the linker that recalls the past occurrence;
`KNOWN_ISSUES.md` is where the fix that worked is actually recorded.

## Gate: does this apply?

Check for `graphify-out/graph.json` at the project root before doing anything else in this skill.

- **Missing** → this skill is a complete no-op. Don't suggest building a graph mid-investigation
  (that's a real side effect — leave it to `/craftsman:init`'s ask-first note, or to the user
  deciding to run `graphify .` themselves). Proceed with normal root-cause investigation.
- **Present** → continue below.

## During root-cause investigation

This slots into the evidence-gathering step of root-cause investigation (Phase 1 of the
superpowers `systematic-debugging` skill, where that plugin is installed) — run this *before*
falling back to raw grep:

1. `graphify query "<symptom or affected function/file>"` — get a scoped subgraph of related code.
   This is both cheaper in tokens than grepping the whole codebase and more thorough than reading
   only the stack trace, since it surfaces callers/dependents that share the same code path.
2. If the query surfaces other call sites of the same function/module implicated in the bug,
   treat them as suspects too — a bug in a shared helper usually isn't confined to the one call
   site that happened to trigger it first.

## Before filing a new KNOWN_ISSUES.md entry (and recall a past fix)

Don't file blind. For each existing entry in the project's `KNOWN_ISSUES.md` — **open and
resolved** — check for a structural link:

1. `graphify path "<new bug's file/symbol>" "<existing entry's file/symbol>"` — a short path
   (direct call, shared callee, same module) is a signal the new bug may be the *same* root cause
   resurfacing at a different call site.
2. If a short path is found, surface it explicitly: "this looks related to the entry from
   <date> — same root cause via `<path>`, not a new issue." Let the user or the fix decide whether
   to merge, not an automatic merge — this is a heuristic signal, not a certainty.
3. When the match lands on a **resolved** entry, that entry's one-line "how it was fixed" is a
   known-good fix for this recurrence — surface it and reuse it rather than re-deriving the fix
   from scratch. (graphify recalls *which* past issue is relevant; the fix text itself lives in
   `KNOWN_ISSUES.md`, not the graph.)
4. Only file a genuinely new entry once existing ones are ruled out this way.

## After the fix

Run `graphify update .` (incremental, AST-only extraction — no LLM cost) so the graph reflects the
fix for the next investigation. This mirrors the same rule some projects already keep in their own
`CLAUDE.md`; this skill makes it apply everywhere a graph exists, not just one project.

## What this does not do

- Does not build or rebuild a graph from scratch — that's a real side effect gated behind explicit
  user action (`graphify <path>`), never triggered implicitly by a bug investigation.
- Does not replace root-cause analysis — it's evidence-gathering *within* the investigation,
  not a substitute for establishing the cause before fixing.
- Does not auto-resolve or auto-merge `KNOWN_ISSUES.md` entries — it only surfaces a possible
  relationship for a human (or the coder agent, with the user's judgment) to confirm.
