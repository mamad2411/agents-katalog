---
name: habit-tracker
description: Maintains a habits.csv log — records daily check-ins, computes streaks with python3, and reads out weekly patterns with compassionate, guilt-free framing. Use when the user says "log my habits", "did my workout", "check in", "how's my streak", "habit report", or wants to start tracking a routine. Don't use for one-off task management or the weekly work review — use weekly-review — or for decision logging — use decision-journal.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Productivity, Habits, Tracking, Wellbeing]
    related_skills: [weekly-review, decision-journal, morning-brief]
---

# Habit Tracker

Keeps an honest, low-friction habit log in a plain `habits.csv` and turns it into streaks and weekly patterns the user can actually learn from. The house rule is **compassionate framing**: a broken streak is data plus a restart plan — never guilt, never "you failed", never streak-shaming. The tool exists to make restarting easy, because restarting is the whole game.

## When to Use

- Daily check-in: "log meditation done", "I skipped the run today".
- Status: "what's my streak", "how did this week go", "habit readout".
- Starting or retiring a tracked habit.
- **Not for:** project tasks or work retrospectives — use `weekly-review`. Not for logging choices and their reasoning — use `decision-journal`.

## Quick Reference

| Action | Command / Call |
|---|---|
| File format | `habits.csv` header: `habit,date,done` (date ISO `YYYY-MM-DD`, done `1`/`0`) |
| Initialize | `echo "habit,date,done" > habits.csv` (only if missing — never overwrite) |
| Log today | `echo "meditation,$(date +%F),1" >> habits.csv` |
| Guard against double-log | `grep -c "^meditation,$(date +%F)," habits.csv` |
| Streaks + weekly pattern | python3 stdlib script (Procedure step 4) |
| List tracked habits | `cut -d, -f1 habits.csv \| tail -n +2 \| sort -u` |

## Procedure

1. **Precheck** — locate `habits.csv` (ask once where it lives, then remember). If missing, offer to create it with the header — append-only from then on; this skill never rewrites or deletes history rows.
2. **Log** — for each habit the user reports, first run the double-log guard; if today's row exists, confirm before appending a correction (append a new row rather than editing — last row for a date wins). Append `habit,date,done` with `done=0` for an honest skip. Skips get logged too: a `0` is information, not a verdict.
3. **Confirm the write** — `tail -3 habits.csv` and echo back what was recorded in one friendly line.
4. **Compute** — for streaks and the weekly readout:

   ```bash
   python3 - <<'EOF'
   import csv, datetime as dt, collections
   rows = {}
   for r in csv.DictReader(open('habits.csv')):
       rows[(r['habit'], r['date'])] = r['done'].strip() == '1'   # last row wins
   habits = sorted({h for h, _ in rows})
   today = dt.date.today()
   for h in habits:
       done = {dt.date.fromisoformat(d) for (hh, d), ok in rows.items() if hh == h and ok}
       streak, day = 0, today
       if day not in done: day -= dt.timedelta(1)      # today not logged yet ≠ broken
       while day in done: streak += 1; day -= dt.timedelta(1)
       week = [(today - dt.timedelta(i)) for i in range(6, -1, -1)]
       bar = ''.join('█' if d in done else '·' for d in week)
       best = 0; run = 0
       for i in range((today - min(done)).days + 1) if done else []:
           d = min(done) + dt.timedelta(i)
           run = run + 1 if d in done else 0
           best = max(best, run)
       print(f"{h}: streak {streak} (best {best}) | last 7d {bar} {len([d for d in week if d in done])}/7")
   EOF
   ```

   Success: one line per habit with current streak, best streak, and a 7-day bar.
5. **Read out, compassionately** — report per the template. For any habit at streak 0 that previously had a run: name the restart, not the break — "Meditation paused after 9 days; the 9 days still count. Restart plan: 2 minutes tomorrow after coffee." Pair the habit with an existing anchor and shrink the ask. Look for patterns worth one sentence ("runs happen Mon–Thu, never Fri — plan around that, don't fight it").

## Output Template

```
# Habit Check-in — {date}

Logged: {habit} → {✅ done / ⏭️ skipped (logged, no drama)}

| Habit | Streak | Best | Last 7 days | Week |
|---|---|---|---|---|
| {habit} | {n}d | {n}d | █·███·█ | {n}/7 |

**Pattern worth knowing:** {one observation, stated neutrally}

**Restarts (if any):**
- {Habit}: paused after {n} days — those days banked. Tomorrow: {tiny version} after {existing anchor}.
```

## Pitfalls

- **Guilt framing sneaks in** ("you broke your streak", "only 2/7") — this is the one hard rule of the skill. Recovery: reread the output before delivering; rewrite any judgment language into data + restart plan; "only" and "failed" are banned words here.
- **Unlogged today counted as a broken streak** — the user checks in at 9 a.m. before doing the habit and their 30-day streak "dies". Recovery: the script already skips today if unlogged; never report a streak break for a day still in progress.
- **Editing history instead of appending** — rewriting rows corrupts the file's audit trail and risks data loss. Recovery: corrections are new rows (last-wins semantics in the script); if the file was damaged, restore from the most recent copy before continuing.
- **Double-logging inflates streaks** — two `1` rows for the same day are harmless to the script but confuse `wc -l` sanity checks. Recovery: the grep guard in step 2; dedupe awareness lives in the script, not in file surgery.

## Verification

- [ ] New rows visible via `tail` and match what the user reported (including honest `0`s)
- [ ] Streak numbers come from the python3 output, not mental math
- [ ] Zero guilt language — every paused habit has a concrete, smaller restart plan
- [ ] History rows untouched; file only ever appended to
- [ ] Header intact: first line of `habits.csv` is `habit,date,done`
