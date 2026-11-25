---
name: decision-journal
description: Appends structured entries to a decisions.md journal — context, options considered, the choice, a two-failure-mode premortem, and a review-by date — and runs reviews when decisions come due. Use when the user says "log this decision", "I decided to...", "add to my decision journal", "review my decisions", or is weighing a significant choice worth recording. Don't use for daily habit check-ins — use habit-tracker — or for weekly work retrospectives — use weekly-review.
version: 1.0.0
author: Gen AI Hub
license: MIT
metadata:
  hermes:
    tags: [Productivity, Decisions, Journaling, Judgment]
    related_skills: [weekly-review, habit-tracker, pipeline-tracker]
---

# Decision Journal

Builds the highest-leverage feedback loop a founder can own: a plain `decisions.md` where every significant choice is recorded *before* the outcome is known — context, options, choice, a premortem of the top two failure modes, and a date to come back and score it. The standard: entries are written at decision time (no retro-fitting), the journal is append-only, and due reviews actually happen.

## When to Use

- The user just made — or is about to make — a decision with real stakes (money, direction, people, commitments).
- "Log this decision", "add to the journal", "I'm going with option B because...".
- Review time: "any decisions due for review?", "score my past calls".
- **Not for:** trivial reversible choices (don't journal lunch), habit tracking (`habit-tracker`), or general weekly reflection (`weekly-review`).

## Quick Reference

| Action | Command / Call |
|---|---|
| Locate the journal | `ls decisions.md` in the user's notes folder (create with a `# Decision Journal` header if missing) |
| Next entry ID | `grep -c "^## D-" decisions.md` then +1 |
| Append an entry | write the filled template to the END of `decisions.md` — never edit old entries |
| Find due reviews | `python3` due-scan (Procedure step 5) |
| Today / review-by math | `date +%F` · `python3 -c "from datetime import date,timedelta; print(date.today()+timedelta(days=90))"` |

## Procedure

1. **Precheck** — locate `decisions.md`; create with header if missing (confirm location with the user first time). Determine the mode: **logging** a new decision or **reviewing** due ones.
2. **Gather (logging mode)** — pull from the user, prompting only for what's missing: the context (what situation forced a choice, in 2–3 sentences with the key numbers), the real options considered (minimum two — "do nothing" counts and often should be listed), and the choice with the primary reason. Write in the user's words; this is their judgment on record, not the agent's.
3. **Premortem — exactly two failure modes** — ask or propose: "It's {review date} and this decision went badly. The two most likely reasons?" Each failure mode gets one line plus an early-warning sign to watch for. Two, not five — forcing the top two is what makes the premortem sharp.
4. **Set review-by and append** — default review horizons: 30 days (tactical), 90 days (most business decisions), 180+ (strategic); compute the date with python3. Fill the template, assign the next `D-{n}` ID, and append to the end of the file. Show the user the entry before writing; append only on their OK. Never modify prior entries — corrections become new dated notes under the entry.
5. **Review mode** — scan for due entries:

   ```bash
   python3 - <<'EOF'
   import re, datetime as dt
   text = open('decisions.md').read()
   today = dt.date.today()
   for m in re.finditer(r'^## (D-\d+): (.+?)$(.*?)(?=^## D-|\Z)', text, re.M | re.S):
       body = m.group(3)
       due = re.search(r'Review by: (\d{4}-\d{2}-\d{2})', body)
       reviewed = 'Outcome:' in body
       if due and not reviewed and dt.date.fromisoformat(due.group(1)) <= today:
           print(f"DUE {m.group(1)}: {m.group(2)} (review by {due.group(1)})")
   EOF
   ```

   For each due entry: reread it with the user, then append a dated **Outcome** block — what happened, verdict (good call / bad call / good process-bad luck / bad process-good luck), whether either premortem failure mode fired, and the one lesson. The process/luck distinction is the point of the whole journal.
6. **Deliver** — confirm what was appended (`tail -20 decisions.md`) and surface any still-due reviews so they don't rot.

## Output Template

```
## D-{n}: {Decision title}
Date: {YYYY-MM-DD} · Review by: {YYYY-MM-DD} · Status: open

**Context:** {2–3 sentences, key numbers included}
**Options considered:**
1. {Option A} — {one-line case for it}
2. {Option B / do nothing} — {one-line case}
**Choice:** {what was decided} — because {primary reason}.
**Premortem (top 2 failure modes):**
1. {Failure mode} — early sign: {observable warning}
2. {Failure mode} — early sign: {observable warning}

<!-- appended at review time -->
**Outcome ({date}):** {what happened}. Verdict: {good call / bad call / good process, bad luck / bad process, good luck}.
Premortem hit? {1 / 2 / neither}. Lesson: {one sentence}.
```

## Pitfalls

- **Entry written after the outcome is known** — hindsight contaminates the record and the journal becomes a highlight reel. Recovery: log at decision time; if backfilling an old decision, mark it `(backfilled — hindsight risk)` so future-you discounts it honestly.
- **Premortem sprawls to five vague risks** — "it might not work" teaches nothing. Recovery: exactly two failure modes, each concrete enough to have an observable early-warning sign; if a risk has no observable sign, sharpen it until it does.
- **Reviews never happen** — the journal fills, the loop never closes, no learning. Recovery: run the due-scan at every journal touch (and during `weekly-review`); a due entry blocks the "all clear" report until reviewed or explicitly deferred with a new date.
- **Outcome graded on results alone** — a lucky bad process gets reinforced. Recovery: the verdict vocabulary forces the process/luck split; if the verdict line says only "it worked", it isn't done.
- **Old entries edited to look smarter** — never; the journal is append-only. Recovery: corrections and updates are new dated lines under the entry.

## Verification

- [ ] Entry appended at file end; all prior entries byte-identical (no edits above)
- [ ] Options ≥2, premortem = exactly 2 failure modes, each with an early-warning sign
- [ ] Review-by date computed, in the future, and ISO-formatted
- [ ] Due-scan run this session; due entries reviewed or explicitly re-dated
- [ ] Entry shown to the user before writing; wording is theirs
