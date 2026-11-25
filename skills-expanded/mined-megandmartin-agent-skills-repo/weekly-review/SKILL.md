---
name: weekly-review
description: Runs a Friday weekly review — wins, unfinished carryover, metrics check-in, next week's top 3 — and appends it to a running weekly-reviews.md log. Use when the user says "run my weekly review", "weekly review", "wrap up my week", "what did I ship this week", or wants a scheduled end-of-week reflection. Don't use for the daily morning kickoff (use morning-brief) or extracting actions from one meeting (use meeting-notes-actions).
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Productivity, Reflection, Automation]
    related_skills: [morning-brief, meeting-notes-actions, file-organizer]
    blueprint:
      schedule: "0 17 * * 5"
      prompt: "Run my weekly review"
---

# Weekly Review

Closes the week with a four-part review — wins, carryover, metrics, next week's top 3 — and appends it to a running `weekly-reviews.md` so the log compounds into a real track record. The standard: evidence over vibes (wins name artifacts, metrics have numbers or an honest "not tracked"), and the log file is append-only — never rewritten.

## When to Use

- Scheduled Friday run (the blueprint fires at 17:00 Fri with "Run my weekly review").
- "Wrap up my week", "weekly review", "what actually got done".
- **Not for:** the daily morning kickoff (use `morning-brief`) or extracting actions from one meeting (use `meeting-notes-actions`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Week bounds | `date -v-monday "+%Y-%m-%d"` (macOS) / `date -d "last monday" +%F` (Linux) |
| Find the log | `find ~/Documents -maxdepth 3 -name "weekly-reviews.md" 2>/dev/null` |
| Read last entry | `tail -60 "weekly-reviews.md"` |
| Week's file evidence | `find <projects-dir> -newermt "$(date -d 'last monday' +%F)" -type f 2>/dev/null \| head -20` |
| Append entry | `cat >> "weekly-reviews.md"` (append only — never `>` overwrite) |

## Procedure

1. **Precheck** — locate `weekly-reviews.md` (`find`, or the path remembered from prior runs). Missing? Ask where to create it (default `~/Documents/weekly-reviews.md`), then start it with a `# Weekly Reviews` header. Compute the week's Mon–Fri dates with `date` for the entry header.
2. **Gather last week's promises** — `tail -60` the log and pull the previous entry's "Next week's top 3." These are this week's scorecard.
3. **Collect evidence** — from what's available: daily notes, files modified this week (`find -newermt`), calendar events, anything the user tells you. Then ask the user 3 quick questions: biggest win? what stalled? any metric moved? Their answers outrank inference.
4. **Draft the entry** — Wins (concrete, artifact-named); Carryover (unfinished items + one-word reason: blocked/deprioritized/underestimated); Metrics (number, delta vs. last entry if logged, or "not tracked"); Next week's top 3 (specific, finishable, at most 3). Score last week's top 3 as done / partial / dropped.
5. **Confirm** — show the full drafted entry. On explicit approval, proceed; edits first if requested.
6. **Append** — `cat >> weekly-reviews.md` with the entry preceded by `\n---\n`. Append-only: never open the file with `>`, never edit past entries. Confirm with `tail -5` that the new entry is at the bottom.

## Output Template

```
---
## Week of {Mon YYYY-MM-DD} → {Fri YYYY-MM-DD}

**Last week's top 3 — scorecard:** {done: n}/{3} ({item: done/partial/dropped}, ...)

### Wins
- {win — artifact/evidence}

### Carryover
- {unfinished item} — {blocked | deprioritized | underestimated}

### Metrics
- {metric}: {value} ({delta vs last week | "not tracked"})

### Next week's top 3
1. {specific, finishable}
2. ...
3. ...

*Logged {YYYY-MM-DD HH:MM}*
```

## Pitfalls

- **Log file overwritten instead of appended** — a `>` where `>>` belonged deletes months of history. Always `>>`; verify afterward with `tail -5` plus a line count sanity check (`wc -l` should grow, never shrink). If history was lost, check for editor backups/Time Machine immediately and tell the user before doing anything else.
- **Wins are vague vibes ("made good progress")** — every win names an artifact: a file, a shipped feature, a sent proposal, a number. If no artifact exists, it goes to Carryover, not Wins.
- **No previous entry exists, so the scorecard breaks** — first run is legitimate: write "First entry — no scorecard" and set the top 3 so next week's review has something to score.
- **Scheduled run fires with the user absent and no answers to the 3 questions** — degrade gracefully: build the entry from file/calendar/notes evidence, mark it `(auto-draft — confirm wins with me)`, and still append so the chain never breaks. Don't fabricate answers on the user's behalf.
- **Top 3 becomes top 7** — the cap is the discipline. Three items maximum; everything else is a backlog note inside Carryover.

## Verification

- [ ] Entry matches the template — all four sections plus scorecard present
- [ ] Entry was appended (`tail -5` shows it at the bottom; `wc -l` grew; earlier entries untouched)
- [ ] Every win cites an artifact; every metric has a number or an explicit "not tracked"
- [ ] Last week's top 3 were scored, or "First entry" is stated
- [ ] Exactly 3 (or fewer) next-week priorities
- [ ] User approved the entry before append (or auto-draft is labeled as such)
