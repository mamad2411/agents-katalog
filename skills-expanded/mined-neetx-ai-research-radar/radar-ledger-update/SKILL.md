---
name: radar-ledger-update
description: |
  Safely update TRENDS.md (the AI Radar ledger): append evidence, move stages, manage observation_queue, source_rotation and strategy_notes without breaking the file contract. Use every time TRENDS.md is edited, before committing radar updates, and when promoting or archiving trends.
---

# Update the ledger safely

`TRENDS.md` is the single source of truth and later sessions parse it. The
structure is a contract.

## File contract (do not change)

- Header: `# Trend ledger — AI Radar`, then `Last updated: YYYY-MM-DD`, then the
  stage legend.
- Sections, in this order: `## Active trends`, `## observation_queue`,
  `## source_rotation`, `## strategy_notes`, `## study_shelf`, `## calibration`.
- `## source_rotation`, `## strategy_notes` and `## calibration` are POINTER stubs only: their real
  append-only content lives in `logs/source_rotation.md` and `logs/calibration.md`
  respectively. Keep the two stub headers (the section order is the contract) but
  NEVER inline log lines back into TRENDS.md — appends go to the `logs/` files.
- Trend block: `### [id: slug-NNN] Title` with fields `alias`, optional
  `pinned: true`, `stage`, `confidence`, `first_observed`, `last_evidence`,
  `evidence:` (list), `notes:`.
- Evidence line: `- YYYY-MM-DD — URL — one line of context`. Keep the context clause to
  roughly 80-120 words: the artifact, the independence/routing call, and the cap-rotation
  note. Extended reasoning, cross-trend framing, or historical narrative belongs in the
  trend's `notes` field ONLY when it binds a future run — do not let it balloon the evidence
  bullet itself. (Amendment W43-P2, applied 2026-10-31 W44 — motivated by the log-verbosity
  metric in `logs/calibration.md`; does not relax the 10-evidence-item cap or any hard rule.)

## Rules

- Match findings to existing trends via id and `alias` before creating a new
  trend. New trends take the next free NNN and start at `seed` or `emerging`.
- ROUTE a captured primary, don't default to "queue it": (a) if it lands on an
  EXISTING trend's axis, append it as EVIDENCE there — a single primary suffices
  for an existing trend; the ≥3-source bar is only for CREATING a trend; (b) if
  the queue now holds ≥3 independent groups on one untracked sub-theme, promote
  that cluster to a `seed` trend; (c) else it stays a queue item. Leaving an
  on-axis primary in the queue (hoarding evidence) or a named primary in report
  prose only is a routing failure.
- Max 10 evidence items per trend — drop the oldest. Keep `last_evidence` equal
  to the newest evidence date.
- Stage moves: at most ONE stage up per trend per day, only on new independent
  evidence, justified in `notes`. Demotions are always allowed. 21+ days without
  evidence → `dormant`; at 45+ days the weekly pass moves the entry to
  `ARCHIVE.md` as a one-line post-mortem.
- Pinned trends (`pinned: true`): NEVER auto-archived, no matter how long
  without evidence — they are the curator's standing-watch axes. They still
  follow the normal stage rules, INCLUDING going `dormant` when quiet (the
  ledger stays truthful about activity); they simply never leave the board.
  Only the curator adds/removes a pin (or the agent proposes it via amendment).
- `observation_queue` items are dated and marked "unverified" unless opened. It
  is a WORKING SET (signals pending verification), not a knowledge store — keep it
  bounded to a soft cap of ~25 live items by a CAP-DRIVEN burndown that runs every
  session, including quiet/no-evidence passes: while the queue is OVER the cap,
  resolve the oldest items toward the cap that run regardless of what the scan
  found; at/under the cap it stops on its own (resolve only the 1–2 oldest if
  stale). This is owed every run, never deferred to the weekly — a no-evidence
  pass is not a no-op for the queue. Items leave ONLY by resolution: promoted to a
  trend (the signal is captured there) or dropped with a one-line reason in the
  day's/week's report (write-once, permanent). NEVER silently delete — because
  every removal is either a promotion or a recorded drop, shrinking the queue
  loses no knowledge. Re-date an item only if it is genuinely still worth watching.
- **Tombstone externalization (amendment W46-P1, applied 2026-11-21 W47):**
  tombstones (DROPPED/RESOLVED/PROMOTED/LEDGER-CONSISTENCY-FIX/CAPTURE-LEAK-FIX
  lines) older than 60 days are moved VERBATIM to the append-only
  `logs/queue_history.md` as part of this run's own queue maintenance, replaced
  by (or folded into) a single one-line `POINTER:` entry noting how many
  tombstones moved and that pre-cutoff history lives there. Live (unresolved)
  queue lines are never externalized this way — only resolved tombstones.
- **Queue-line format (amendment W35-P1, applied 2026-09-05 W36):** a queue entry
  holds ONLY genuine unresolved signals, one line per signal (or one tightly
  bundled line per day listing just the still-open below-bar/adjacent/unverified
  items), in the file's own stated `date — description — link` shape. It must
  NEVER restate what a lane already routed to trend evidence, the day's dormancy
  enumeration, the capture-leak count, or source-rotation narration — that audit
  trail already lives permanently in `reports/YYYY-MM-DD.md`; duplicating it here
  is a bloat failure, not thoroughness (it drove TRENDS.md from 41KB at W24
  baseline to ~650KB by W36, with individual daily queue lines reaching 7-21KB).
  When in doubt, ask "does this line name something still awaiting a decision?" —
  if not, it belongs in the report only.
- Append one dated line per session to `logs/source_rotation.md` (the coverage
  log; not the TRENDS.md stub). Append dated corrections to `logs/strategy_notes.md`
  (the strategy log; not the TRENDS.md stub); never delete curator entries.
- `study_shelf`: newest first, format `date — [name](url) — one line of why`;
  single-artifact items allowed (the trend bar does not apply), opened primary
  sources only.
- `calibration` (now `logs/calibration.md`) is append-only and written by weekly
  runs only (see the `radar-self-eval` skill); daily runs never touch it.
- **Notes compaction (amendment W35-P2, applied 2026-09-05 W36):** once a
  trend's `notes` field exceeds roughly 1500 words, the NEXT run that touches
  that trend's notes (daily or weekly) compacts older `Update YYYY-MM-DD`
  entries into one running-summary paragraph — preserving the founding/
  anchor reasoning and the most recent 2-3 updates verbatim — rather than
  accumulating every update verbatim forever. State in that day's/week's
  report that a compaction happened and roughly how much was condensed;
  nothing is lost (the pre-compaction notes text remains readable in the git
  history of this file). This mirrors the precedent that already externalized
  `source_rotation`/`calibration` out of TRENDS.md for the same size reason.
- Update the `Last updated` line. Keep everything in English.

## Validate before commit

```bash
grep -n '^## ' TRENDS.md
# expected, in order: Active trends, observation_queue, source_rotation, strategy_notes, study_shelf, calibration
grep -c '^### \[id: ' TRENDS.md          # trend count matches expectations
grep -nE '^  - [0-9]{4}-[0-9]{2}-[0-9]{2} — ' TRENDS.md | head -3   # evidence format
grep -n '^Last updated:' TRENDS.md       # date is today
# the three externalized logs must exist and only grow (append-only):
for f in source_rotation strategy_notes calibration; do
  test -f logs/$f.md && printf '%-16s ' $f && tail -1 logs/$f.md | head -c 70 && echo
done
# TRENDS.md must NOT have regrown a log body — all three stay short POINTER stubs.
# A stub over ~10 lines means a run wrote the log INTO the ledger instead of logs/:
awk '/^## /{if(s)printf "  %-16s %d lines%s\n",s,n,(n<10?"  ok":"  <- REGROWN, move it to logs/");s="";n=0}
     /^## (source_rotation|strategy_notes|calibration)/{s=substr($0,4)} {n++}
     END{if(s)printf "  %-16s %d lines%s\n",s,n,(n<10?"  ok":"  <- REGROWN, move it to logs/")}' TRENDS.md
```

If a check fails, fix the file before committing. Commit and push per the
conventions in AGENTS.md.

The expected section order above IS the file contract. When a check finds a section
missing or out of order, RESTORE that section in TRENDS.md — never edit this list, or any
check in this block, to match the broken file. A check rewritten to accept a defect is how
a lost section stays lost: every later run validates clean against it.

Collection trends (BATCH PRODUCERS, routines/daily.md): a batch producer's collection is an
ordinary trend block — same fields, same 10-item evidence cap. Its notes point to the producer's
section in `logs/results_catalog.md`, where the individual items live one line each; an item is
promoted out to its own block only when it clears the bar by itself.
