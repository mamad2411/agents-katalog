---
name: memory-hygiene
description: Maintains an agent's memory and notes files — dedupe entries, prune stale facts, convert relative dates to absolute, and verify claims are still true before re-asserting them, on a weekly sweep. Use when the user says "clean up memory", "the agent keeps repeating outdated info", "memory sweep", "my notes file is a mess", or on the scheduled weekly maintenance pass. Don't use for managing what loads into a live session's context — that's context-budget-manager.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Agent Mastery, Memory, Maintenance, Hygiene, Notes]
    related_skills: [context-budget-manager, heartbeat-standup]
---

# Memory Hygiene

An agent's memory files are load-bearing: every session reads them as ground truth, so one stale fact gets confidently repeated forever. This skill is the maintenance discipline — dedupe, prune, absolutize dates, and verify before re-asserting — run as a weekly sweep with a diff the user approves before anything is deleted. The standard: everything in memory is true today, dated, and said exactly once.

## When to Use

- Weekly scheduled sweep of `MEMORY.md` / notes files (pairs with `heartbeat-standup` cadence).
- The agent asserted something outdated, contradictory, or duplicated in a session.
- Before a high-stakes task that will lean heavily on memory (sales call prep, reports, planning).
- After a big project change (pivot, rename, migration) that invalidates a cluster of remembered facts.
- **Not for:** deciding what to load into a session (`context-budget-manager`), or writing brand-new memory entries mid-task (just write them well: dated, absolute, sourced).

## Quick Reference

| Check | How |
|---|---|
| Inventory | List memory files + `wc -l` each; flag any file >150 lines for split/prune |
| Dedupe | Sort entries by topic; same fact stated twice = merge into the better-dated one |
| Relative dates | `grep -niE "yesterday|last week|recently|next month|currently|soon|this (week|month)" <file>` |
| Staleness | Any entry older than 90 days or undated → verify or prune |
| Contradictions | Same topic, conflicting values (two "canonical DB" claims, two prices) → resolve to one |
| Verification | Check the claim against its source (file, URL, DB, user) before it survives the sweep |
| Undo path | `git commit` or dated `.bak` of every file BEFORE applying the sweep |

## Procedure

1. **Inventory** — list every memory/notes file the agent reads (memory dirs, `MEMORY.md`, topic files). Record line counts. Success: a complete list; a file you forgot is a file that stays dirty.
2. **Dedupe** — group entries by topic. Where the same fact appears twice, keep one entry — the most recent, best-sourced version — and fold any unique detail from the duplicate into it. Where near-duplicates differ, that's a contradiction: flag for step 4.
3. **Absolutize dates** — run the relative-date grep. Rewrite every hit against the file's edit date, not today: "last week" in a note written 2026-07-10 means early July, not mid-July. Every entry ends up with an absolute date ("as of 2026-07-24"). Undatable entries get flagged for verification or pruning.
4. **Verify before re-asserting** — for each flagged, stale (>90 days), or contradictory entry, check the source of truth: open the file it describes, hit the URL, query the DB, or ask the user (batch the questions, don't drip them). Outcomes per entry: CONFIRM (re-date it), UPDATE (correct + re-date), PRUNE (no longer true or no longer worth remembering). Never "probably still true."
5. **Prune with a dry run** — present the full change set as a diff: entries merged, rewritten, and deleted, each deletion with a one-line reason. This sweep edits the agent's ground truth — get explicit user approval before writing. Keep the pre-sweep copy (git commit or a dated `.bak`) as the undo path.
6. **Apply and log** — write the approved changes, then append a one-line sweep record ("swept 2026-07-24: 41→28 entries, 6 verified, 4 pruned") so the next sweep knows where it stands.
7. **Fix the intake habit** — if the sweep found many relative dates or unsourced claims, the write habit is the real bug: from now on, new entries are written dated-absolute-sourced at creation time. Note this in the sweep report.

## Output Template

```
## Memory sweep — <date>
Files: <list> | Entries before/after: <n> → <m>

| Action | Count | Examples |
|---|---|---|
| Deduped | <n> | "<topic>" (2 entries → 1) |
| Dates absolutized | <n> | "recently" → "as of 2026-07-10" |
| Verified & confirmed | <n> | <topic> (source: <file/url/user>) |
| Updated | <n> | <old> → <new> |
| Pruned | <n> | <entry> — <reason> |

Contradictions resolved: <topic>: kept "<value>" (source), dropped "<value>"
Undo path: <git sha | backup path>
Intake fix needed: <yes — what | no>
```

## Pitfalls

- **Verifying by memory** — "I remember that's still true" is the exact failure mode this skill exists to stop. Recovery: every CONFIRM must cite a source checked during THIS sweep (file, URL, query, or the user's answer); no source, no re-assert — flag or prune.
- **Aggressive pruning loses context** — an entry looked stale, got deleted, and next week the agent re-learns it expensively (or asks the user something it was already told). Recovery: restore from the undo path; adjust the rule — prune what's false or worthless, ARCHIVE (move to a dated archive file) what's true-but-dormant.
- **Relative dates anchored to the wrong day** — rewriting "next Friday" against today's date instead of the entry's write date, shifting a deadline by weeks. Recovery: always resolve against file/entry timestamps (`git log -p` shows when a line appeared); when the anchor is unrecoverable, ask the user rather than guess.
- **Merging contradictions instead of resolving them** — two conflicting values kept "to be safe," so the agent keeps flip-flopping. Recovery: one topic, one truth — pick via source-of-truth check, record the loser in the sweep log (not in memory), and note WHY the kept value won.
- **Sweep skipped for a month** — memory rot compounds and the next sweep is huge and risky. Recovery: do a triage sweep (dates + contradictions only) immediately, schedule the full pass, and wire the weekly cadence into `heartbeat-standup` so it can't silently lapse.

## Verification

- [ ] Every surviving entry has an absolute date and states each fact exactly once
- [ ] Relative-date grep returns zero hits on the swept files
- [ ] Every CONFIRM/UPDATE cites a source checked during this sweep
- [ ] User approved the diff before writes; undo path (commit/backup) exists and is noted
- [ ] No memory file exceeds ~150 lines without a split/archive decision recorded
- [ ] Sweep log line appended; next sweep date on the calendar/standup cadence
