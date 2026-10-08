---
name: daily-plan
description: Generate today's daily plan — a priority-anchored, project-heavy checklist for the day, written to Plans/Week of <Mon>/(C) YYYY-MM-DD.md. Use whenever the user says "daily plan", "/daily-plan", "plan my day", "what should I do today", "give me today's plan", or asks for a plan/checklist for the day's work. Reads the ranked Priority List in GOALS.md and anchors on P1 (overridable), asks how many hours they have, formulates two original daily goals from P1's longer-term goal, supplements them with open next-steps from P1's Iteration Logs plus at most one from P2, and sizes the day to fit. Trigger this proactively at the start of a work day even if the user doesn't name the skill.
---

# Skill: Daily Plan

Generate the user's plan for **today** — a short, project-heavy checklist sized to the hours they actually have. The plan has two halves: **two original daily goals you formulate** that push the project's longer-term goal forward, plus **2–3 items pulled from the real backlog** (`Iteration Logs/`). This is the morning generator half of the Progress loop in the root `CLAUDE.md`; the evening reckoning (planned-vs-done, sidetrack call-out) is **not** this skill's job — that lives in the daily Progress synthesis. Keep this skill a clean morning tool.

The whole point is to fight the user's documented failure modes: disorganized priorities, trivial tasks ballooning to eat the day, and getting sidetracked. So the plan is deliberately **short, project-weighted, and honest about time** — a plan you can actually finish beats an ambitious one you abandon. The two original goals exist so the plan is driven by where the project *should* go, not just by whatever happens to be sitting in the backlog.

## When to Use

- User says "daily plan", "/daily-plan", "plan my day", "give me today's plan", "what should I work on today".
- The start of a work day, when the user wants direction — trigger proactively even without the exact phrase.

Optional argument: a **project name** to override P1 for today (e.g. `/daily-plan Golf`). This overrides the plan, **not** the Priority List — never rewrite the ranking in `GOALS.md` because of a one-day override.

## Core principles (why this skill is shaped the way it is)

- **Generative, not just consumptive.** The backbone of the plan is **two original daily goals you formulate** from the project's highest-priority longer-term goal — concrete moves toward it that are *not* already written down in the backlog. The backlog (2–3 items) supplements these; it does not lead. This is the deliberate fix to the old behavior, where the plan was nothing but a backlog-priority queue and never asked "what's the right next move toward the goal?"
- **Priority-anchored, with one center of gravity.** The plan is driven by the ranked **Priority List** in `GOALS.md`, not by a project frozen for the week. Both original daily goals come from **P1**; at most **one** backlog item may come from **P2**; P3 and below get nothing. Rank moves with deadlines, but a single day still has one center of gravity — that's what keeps this from decaying into the multi-project sprawl the old weekly rule existed to kill. Only a thin slice goes to the daily non-negotiables; too many non-negotiables become their own distraction, as the user said explicitly.
- **Time-budget fit only.** Tasks are sized by effort and packed into the hours available. There is deliberately **no automatic "you finished X% yesterday, so shrink today" scaling.** That was considered and rejected: unseen life circumstances (not capacity) leave plans undone, and a rate-based algorithm misreads that as low capacity → permanently pessimistic plans, a death spiral. Intensity is a **manual dial** the user controls.
- **One round-trip.** Draft the whole plan, show it, let the user accept or swap an item or two, then write. Mornings need to be fast; a multi-turn interrogation kills the habit. Approving the plan *is* the commitment to it.

## Procedure

### 1. Resolve P1 and P2 from the Priority List

Read the **`## Priority List`** section of `GOALS.md` (vault root). It is an **ordered** list — position 1 is P1, position 2 is P2. Only the **numbered** entries are eligible; everything after any `—— … ——` divider (`below the line`, `done`, or similar) is **out of scope** for the plan entirely.

- If a project name was passed as an argument, that project is **today's P1**. The list's real P1 becomes P2 for today (unless the argument already names P1). Do **not** edit `GOALS.md`.
- Otherwise take P1 and P2 straight off the list.
- If the `## Priority List` section is missing, **ask** the user to name their top two priorities for today, use those, and note that adding a `## Priority List` section to `GOALS.md` makes this automatic next time.
- If the list has only one eligible entry, that's fine — the plan runs on P1 alone and simply carries no P2 item.

Confirm each resolved project has a folder under `Projects/` (subprojects may be nested, e.g. `Projects/Interview Prep/Company/Google Interview Prep/`).

### 2. Read the intensity dial + run the weekly checks

- Read the **`**Intensity:**`** field in `GOALS.md` (`low` | `normal` | `high`). If absent, assume `normal`.
- Determine this week's Monday (see the date snippet below) and check whether `Plans/Week of <Mon>/` already contains any plan files.
- **If this is the first plan of a new week** (folder empty or missing), run two quick checks in a single question:
  1. **Intensity survey** — "How's the intensity this week — scale up, down, or keep it at `<current>`?"
  2. **Priority-list check** — show the current top three and the `> **Re-ranked:**` date, then ask "Still the right order?" Apply any reorder to `GOALS.md` and stamp a new `Re-ranked:` date.

  Both edit a non-`(C)` file the user authored — doing it here is the skill's job, but say what changed.
- On any other day of the week, read both silently. **Do not offer to re-rank mid-week.** If the user asks to re-rank anyway, do it — but say plainly that reordering the list is not progress on it.

> The surveys are weekly, not daily, by design: daily re-asking invites mood-driven over/under-correction, and daily re-ranking turns the priority list into a procrastination surface. Both failure modes are documented in `GOALS.md`. The `weekly-update` skill also maintains these fields; this is the safety net so neither goes stale.

### 3. Ask for today's schedule

Prompt once, in one line: **"How many hours do you have for focused work today, and any fixed commitments (class, gym, plans with people)?"**

The journal is usually empty this early, so asking is the lowest-friction accurate input. Use the answer to compute the **available focused hours** for project work (subtract fixed commitments).

### 4. Formulate two original daily goals (the backbone)

Read **P1's** `Goals/` files and pick the **highest-priority longer-term goal** (`type: goal`). If priority is ambiguous, pick the goal that best explains why P1 is ranked first right now; if there are no `Goals/` files at all, ask the user for the project's current longer-term aim before proceeding.

Both original daily goals come from **P1 only** — never split them across P1 and P2. That split is exactly how the day loses its center of gravity.

From that one long-term goal, **formulate two original daily goals** — specific, concrete moves that advance it and that can realistically land *today*. Rules:

- They must be **your own framing**, not copied from an `Iteration Logs/` next-step. Read the backlog (next step) precisely so you can avoid duplicating it.
- Each must be a concrete deliverable for today ("draft the auth-token refresh flow and test the happy path"), not a vague theme ("work on auth").
- Each must visibly ladder up to the chosen long-term goal — name that goal in the plan so the link is explicit.
- Assign each an effort estimate (`S`/`M`/`L`) so step 5 can budget it.

These two are the heart of the plan. The backlog items below fill out the rest of the day around them.

### 4b. Pull 2–3 supplementing backlog items

Read open `type: next-step` files (frontmatter `status: open`) from **P1's** `Iteration Logs/`, and separately from **P2's**. Each carries `effort` (`S`/`M`/`L`) and `goal`.

- Rank within each project by **goal priority first** (steps advancing the highest-priority goal win), then by effort.
- Select **2–3 total**, subject to a hard rule: **at most one may come from P2**, and only if the remaining budget still fits it after P1's items. Nothing below P2 is eligible, ever.
- The P2 item exists to keep the second priority from going cold, not to split the day. If the budget is tight, P1 wins and P2 gets nothing today.
- Avoid items that just restate the two original goals.
- **If P1's backlog is empty**, that's fine — the plan still stands on its two original goals, and the one P2 item may still come along. Flag the empty backlog and suggest adding `type: next-step` files so future plans have depth. Don't dead-end, and don't interrogate.

### 5. Size the day (time-budget fit)

Convert effort to rough hours, scale the budget by intensity, and select tasks until the budget is filled:

| Effort | Hours |
|---|---|
| S | ~0.5 |
| M | ~1.5 |
| L | ~4 (half-day) |

| Intensity | Budget multiplier |
|---|---|
| low | 0.7 |
| normal | 1.0 |
| high | 1.3 |

`effective budget = available focused hours × intensity multiplier`. Fill in strict order of precedence:

1. The **two original P1 goals** (the backbone — they are never dropped for a backlog item).
2. Top-ranked **P1 backlog** items that fit.
3. **One P2 item**, only if budget remains after 1 and 2.

Target shape: **2 original goals + 2–3 backlog items** (≈4–5 project tasks). On a short day the two original goals may already consume the budget — carry **fewer or zero backlog items** rather than overpacking. Hard cap the whole checklist at **~6 items** so it never sprawls.

These numbers are rough on purpose — the dial exists precisely so the user corrects for systematic over/under-estimation rather than the skill pretending to precision it doesn't have.

### 6. Compose the plan

- **Body, in two tiers:**
  - **Today's goals** — the two original daily goals you formulated from P1, each a checkbox, with the long-term goal they advance named once at the top of the section (`**Advances:** [[(C) <Goal>]]`). These have no `Iteration Logs/` link because you invented them; that's expected.
  - **From the backlog** — the 2–3 selected next-steps, each a checkbox linking back to its `Iteration Logs/` next-step file. **Tag the P2 item with its project name** so the one context-switch in the day is visible rather than smuggled in.
- **Non-negotiables:** exactly one fixed checklist item — **faith / prayer** (the prime-directive guardrail; "focus" is already served by the project tasks). Everything else (a LeetCode rep, physical/sport, rest) collapses into **one condensed reminder line**, not separate checkboxes — present but not competing for attention.

### 7. Confirm, then write

Show the drafted plan in chat. Ask: **"Good to go, or want to swap anything?"** Apply any swaps. Then write the file to:

```
Plans/Week of <Mon date>/(C) YYYY-MM-DD.md
```

Create the `Plans/` folder and the week subfolder if they don't exist. The folder naming mirrors the `Progress/` structure exactly so the evening Progress synthesis can find today's plan by the same date.

End with the file path and a one-line "go get it" — and, per the user's standing preference, a suggested next action (usually: start the top task).

## Plan file template

```markdown
---
type: plan
project: <P1 project>
p2: <P2 project — omit if the day carries no P2 item>
date: YYYY-MM-DD
intensity: <low|normal|high>
hours: <available focused hours>
tags: [plan, <p1-slug>]
---

# (C) YYYY-MM-DD — <one-line headline of the day's focus>

**P1:** [[(C) <P1 project>]] · **Budget:** <effective hours>h (<available>h × <intensity>)

## Today's goals
**Advances:** [[(C) <Long-term Goal>]]
- [ ] <original daily goal 1 — concrete deliverable for today> (<effort>)
- [ ] <original daily goal 2 — concrete deliverable for today> (<effort>)

## From the backlog
- [ ] <P1 backlog task> — [[(C) <next-step file>]] (<effort>)
- [ ] **[P2 · <P2 project>]** <backlog task> — [[(C) <next-step file>]] (<effort>)

## Non-negotiables
- [ ] 🙏 Faith / prayer

_Reminders: one LeetCode rep · move (sport/gym) · protect rest._
```

The one-line headline keeps the `Plans/` Dataview table readable without opening files:

```dataview
TABLE date, project, file.link FROM #plan SORT date DESC
```

## What this skill does NOT do

- **It does not reconcile the plan at end of day.** Planned-vs-done and the sidetrack call-out are produced by the daily Progress synthesis, which reads the same-date plan file. Keeping generation and review separate keeps each tool one job.
- **It does not pull from P3 and below.** One P2 item is the entire allowance. Pulling from every project reopens the multi-project sprawl the operating principle exists to kill — the ranked list replaced the frozen weekly project precisely so rank could move, not so every project could be worked at once.
- **It does not re-rank the Priority List mid-week**, and a `/daily-plan <Project>` override never rewrites `GOALS.md`.
- **It does not auto-shrink based on past completion.** See the death-spiral reasoning above; intensity is manual.

## Date helper

The week folder uses the current week's **Monday**. To compute it on Windows:

```powershell
$today = Get-Date
$monday = $today.AddDays(-(([int]$today.DayOfWeek + 6) % 7))
"Plans/Week of {0}/(C) {1}.md" -f $monday.ToString('yyyy-MM-dd'), $today.ToString('yyyy-MM-dd')
```

## Edge cases

- **Barclays resolves as P1 or P2** → the plan file is committed to a git repo, so **never write Barclays-internal specifics** into it (no system names, ticket IDs, client or colleague names, internal architecture). Keep goals generic and skill-shaped — "write up what I learned about the deployment pipeline in my own notes", not the pipeline's details. This rule is in the root `CLAUDE.md` and is not negotiable for a day's convenience.
- **No `## Priority List` in GOALS.md** → ask for today's top two; suggest adding the section.
- **Priority List has one eligible entry** → run on P1 alone, no P2 item.
- **P1 or P2 names a project with no folder under `Projects/`** → say so and ask which project was meant; don't silently substitute the next one down.
- **`> **Re-ranked:**` date is more than ~2 weeks old** → mention it once when writing the plan, but still generate today's plan. Don't block on a re-rank.
- **No `**Intensity:**`** → assume `normal`.
- **No `Goals/` files in P1** → ask the user for the project's current longer-term aim, then formulate the two original goals from that.
- **Empty Iteration Logs backlog** → the plan still stands on the two original goals; flag the empty backlog and suggest adding `type: next-step` files.
- **Plan already exists for today** → ask whether to regenerate (overwrite) or keep the existing one.
- **Very short day (e.g. <2h)** → the two original goals alone (or one, if even that overflows) are the plan; drop backlog items rather than padding.
