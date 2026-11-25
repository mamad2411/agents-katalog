---
name: conflict-detection
description: >
  Detects contradictions and under-specified decisions across planning docs (raw/)
  and flags them for human judgment — triggers on a weekly cron sweep (an
  adopter-provided worker script, e.g. Mon 06:00 team time) or on explicit human
  request; detection and surfacing only, never resolution.
version: 0.1.0
author: Loremaster
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [conflict, wiki, scrum, PM, detection, governance]
    related_skills: [refine-wiki]
---

# Conflict Detection Skill (weekly safety net + manual auxiliary check)

The LLM detects; **a human judges.** You only *find and surface* contradictions — you never choose which side is right and never fix anything.
**In v2, primary conflict handling happens locally in `backlog-complete` (pre-push; a local, developer-side client-template skill that lives outside this repo) — this skill is the weekly cron safety net (via an adopter-provided weekly sweep worker) that catches missed completes, plus a manual auxiliary check run when a human asks (PROJ-79).**

## Absolute rules (never violate)
- Do not resolve conflicts. Do not choose which side is right.
- Do not rewrite, summarize, merge, or refine documents.
- Do not privilege one side (no "the newest doc / the PRD is probably right" assumptions). Present both claims side by side.
- Report only what is actually written. Never invent conflicts that are not there. When in doubt, report (an omission is worse than an over-report).
- Never mark anything superseded or update the wiki without human judgment.

## Scope of operation
- **Targets:** the documents/topics the user specifies. If unspecified, target the **raw docs changed by recent pushes** (identified via `git log` in the lore vault) and compare them against all of raw.
  **Weekly cron mode** (the worker passes the target list in the prompt): targets = **raw docs changed by pushes in the last 7 days** — the worker computes them with `git log --since='7 days' --relative -- raw/` and hands them over. Check only the list you were given; do not expand the scope on your own.
- **Comparison baseline:** all of `wiki/` + all of `raw/` whose `status` is not `superseded` (**including subdirectories — `raw/**/*.md`**). Raw layout = `raw/PRD.md` (planning) + `raw/decisions/*.md` (per-backlog decision details, e.g. `raw/decisions/<proj>-N.md`). **progress is not part of this pipeline** (do not read it). Do not assume fixed filenames like `raw/PRD.md, raw/DECISIONS.md` — glob all of raw.
- **No re-reporting (dedup):** never create a new file for a conflict that matches an existing CONFLICT file in `conflicts/`, regardless of its status (`open` or `resolved`) — same topic and same two sides means the existing open file is already awaiting judgment (append evidence rows to the existing file if needed).
- **Known filter:** mismatches that match an entry in `conflicts/KNOWN.md` (tracked lags — e.g. "PRD update awaiting Slack draft submission", "awaiting deferred judgment") must **not be reported as conflicts.** KNOWN.md is human-managed — never add or remove entries yourself. If the file does not exist, proceed without the filter.
- `raw/decisions/` is normally **human-authored input** synced from the project repo. Decision details can contradict the PRD (e.g. PRD says "Google" but a decision says "Kakao SDK") — surface that as a conflict. Most are conflict-free (simple detail additions) and pass straight through to refinement.

## Using the schema
- Read frontmatter: `authority` / `status` / `updated` / `supersedes` / `doc_type` / `tags`.
- Narrow the comparison to docs whose `tags`/`doc_type` overlap. Exclude `superseded` docs from comparison.
- Report `authority` differences alongside, but **never auto-retire** — go no further than proposing a "superseded candidate".

## Detection types (7)
1. Direct contradiction  2. Number/spec mismatch  3. Timeline conflict  4. Definition/terminology drift
5. Decision reversal  6. Orphaned reference  7. Under-specified decision (stated like a decision, but missing a concrete value needed for implementation)

### ⚠️ Relax type 7 (under-specified) for `raw/decisions/*.md` (implementation decisions)
For implementation decisions, **details being filled in by code is normal.** Things like *"schema columns and exact policy values to be finalized in code"* are **not conflicts — pass them through** to the wiki (most docs flowing through conflict-free is the point of this model). Raise type 7 **only when another document (PRD or another decision) *depends* on that concrete value and it is missing, or when different decisions state the same value differently.** In short: catch types 1–6 (direct contradictions, spec mismatches, reversals, **package/integration conflicts**, e.g. auth via Firebase vs RLS using Supabase auth.uid()), but do not flag "details to be settled in implementation".

### ⚠️ Explicit deferrals are not conflicts (all docs, PRD included)
Items **deliberately postponed** — *"delivery channel and frequency policy to be decided later"*, *"payments deferred to next quarter"*, *"web version reviewed after launch"* — are roadmap gaps, not contradictions — **do not flag them as type 7.** It is enough for the wiki to **record** the gap, e.g. *"Notifications: planned, policy TBD (to be decided later)"* (pass it through; do not stop the build). In particular, a single sentence/section saying **"do X + X details later"** is one coherent statement, not an A-vs-B conflict. Type 7 applies **only when another document actually depends on that value and it is empty, or when two sources state the same value differently** (e.g. PRD says 30 memos vs a decision says 50).

## Output: `conflicts/CONFLICT-<number>_<YYYY-MM-DD_HHMM>.md` (one file per conflict; **team-timezone date+time** suffix for dedup and history)
- **All timestamps use the team's timezone** — the filename suffix and every date inside the file. Always pass an explicit timezone so filenames and dates match the team's wall clock: in the terminal use `TZ="$TEAM_TZ" date +'%Y-%m-%d_%H%M'` (for filenames) and `TZ="$TEAM_TZ" date +%F` (for body dates) (set `TEAM_TZ` to your team's IANA timezone, e.g. `America/New_York`). A date-only suffix collides on same-day reruns, so include **minutes (HHMM)** to disambiguate.
Output **exactly this structure** (for readability and comparison):
```
# CONFLICT-NNN · <one-line topic>

**Type** <one of 1–7> · **Severity** high|medium|low · **Status** open · **Tags** <area>

> **Judgment question** — <the one line the team must decide. Do not write the answer>

| Position | Verbatim quote | Source |
|:--:|---|---|
| **A** | "<one verbatim quote>" | `<file:line>` |
| **A** | "<another quote supporting the same A>" | `<file:line>` |
| **B** | "<verbatim quote>" | `<file:line>` |

**Proposal** — <"superseded candidate" level only when the authority difference is clear; otherwise —>
```
**Table rules (strict):**
- **One row = one quote + one source.** Never mix multiple quotes, multiple sources, or commentary into one row (it breaks the table and is unreadable).
- If one position has multiple pieces of evidence, **repeat the position letter (A/A/A)** to split rows.
- Position = one letter per opposing document/claim: A, B, C, D…
- Quotes are verbatim (no summarizing, no commentary). Escape `|` inside quotes as `\|`.
- Source is `file:line`. If authority/updated is present, append `· authority N` after the source (omit if absent).
- Number = the current maximum in `conflicts/` + 1.

## Follow-up actions
- This skill's output ends at the `conflicts/CONFLICT-*.md` files. **Commit only — do not push and do not send to Slack** — in weekly mode the worker (the adopter-provided weekly sweep script) handles push and summary delivery.
- On manual invocation, if there is even one conflict: tell the human to **halt wiki refinement for that topic**.
- No superseded processing and no automatic wiki updates without human judgment.

## Isolation
- Read only this project's (channel/lore vault) documents. Never pull in another project's documents.
