---
description: Set a learning goal — define the target and scope, audit your knowledge base against it, and classify what you already know vs what must be pulled in. First stage of a course; hands off to /curriculum.
argument-hint: <topic> [by <deadline>] [<N> hours/week] — or "edit <slug>" to adjust an existing goal
allowed-tools: Read, Write(course/**), Glob, Bash(date:*), Bash(sh .claude/src/pyrun:*)
---

Set the **goal** for a course on **$ARGUMENTS**: define the target and scope, audit
the knowledge base against it, classify what's already known vs missing, and write
`course/<slug>/goal.md`. This is the first stage of the learning pipeline:

```
/goal <topic>   →  course/<slug>/goal.md   (target + scope + knowledge audit)
                   └─ auto-hands off to ↓ (goal + curriculum are linked)
/curriculum <slug>  →  pulls resources, builds modules + schedule
/tutor <slug>       →  daily: reading list → teach → ingest → (test|honor) → advance
```

`/goal` does **not** pull resources or build a schedule — that is `/curriculum`'s job; keep
this stage about *what* to learn and *where you stand*. The two stages are **linked**: once
the goal is confirmed, `/goal` **auto-hands off to `/curriculum <slug>`** (see **Wrap up**).

If **$ARGUMENTS** starts with `edit `, extract the slug and jump to **Edit Mode**.
If **$ARGUMENTS** is empty, ask the user for a topic, then continue with Step 1.

---

## Edit Mode — `/goal edit <slug>`

Adjust an existing goal without rebuilding from scratch.

### E1 — Load
Read `course/<slug>/goal.md` and `course/<slug>/progress.md` (if present). Show the
current state: target, scope, subgoals, knowledge audit.

### E2 — Ask what to change
Offer (user may pick several): change deadline / hours; tighten or widen scope;
add/edit/remove a subgoal; re-run the audit for a new sub-topic; add free-form notes.

### E3 — Apply changes
Make the edits. If a new sub-topic is added, re-run retrieval (Step 3) for just that
topic and fold the findings into the audit. Do not touch `plan.md`/`schedule.md` —
if the scope changed materially, tell the user to re-run `/curriculum <slug>`.

### E4 — Write
Overwrite `course/<slug>/goal.md`. Report what changed.

---

## Step 1 — Gather inputs

Parse **$ARGUMENTS** to extract:
- **topic** — what to learn (required; ask if missing)
- **deadline** — target date, e.g. "by 15 July", "in 4 weeks" (optional; convert
  relative phrases to absolute dates with `date +%Y-%m-%d`; store as `YYYY-MM-DD`;
  use `"open-ended"` if not given)
- **hours_per_week** — available study hours per week (optional; suggest 5 default). This
  is the **only** time budget — do **not** assume a per-day rate or split the week into
  days; `/curriculum` schedules in **hour-blocks** within each week.

Ask for anything important that's missing before continuing.

## Step 2 — Slug and existing check

Slugify the topic to kebab-case. Check whether `course/<slug>/goal.md` exists.
- **Exists** → ask: update it (→ Edit Mode) or start fresh (overwrite)?
- **Does not exist** → continue.

## Step 3 — Scope the topic

Draft an explicit **in-scope / out-of-scope** definition (e.g. for flow matching:
*in — CNFs, the FM objective, probability paths, sampling; out — GANs/VAEs except as
contrast, deployment*). Show it to the user and refine before auditing — the scope is
what `/curriculum` will pull resources against, so it must be right.

## Step 4 — Audit the knowledge base

```bash
sh .claude/src/pyrun .claude/src/retrieve_cli.py --retrieve "<topic>"
```

Each output line is `<file path>\t<title>`. Read each result and follow relevant
`[[wikilinks]]` (1–2 hops) with `sh .claude/src/pyrun .claude/src/retrieve_cli.py --resolve "<link>"`.
Collect relevant files across `sources/`, `notes/`, `papers/`, `concepts/`.

## Step 5 — Read existing scores

If `course/<slug>/progress.md` exists (written by `/tutor`), read its Item Progress
table and map each scored item to its retrieved file, so the audit reflects tested
mastery, not just presence.

## Step 6 — Classify knowledge state

`Status` is a single **readiness ladder** — how ready each item is in your base. Assign each
item the highest rung it has reached:

| Status | Rung — what it means | Condition |
|--------|----------------------|-----------|
| `missing` | **0 — not in your base.** In scope but you have nothing on it yet; `/curriculum` must pull a source. | In scope / referenced (wikilinks, `concepts_mentioned`) but no source or page exists |
| `pulled` | **1 — raw source only.** A source sits in `sources/`/`notes/`, but it hasn't been written up into a page yet. | Source exists in `sources/`/`notes/`, no synthesised `papers/`/`concepts/` page |
| `untested` | **2 — page exists, untested.** You have a synthesised page but `/tutor` hasn't tested you on it. | Page exists in `papers/`/`concepts/`, no score yet (incl. honor-system `read`) |
| `revisit` | **2 — page exists, tested but shaky.** Tested, but you scored `partial`/`wrong` — go back to it. | Page exists **and** latest `/tutor` score is `partial` or `wrong` |
| `covered` | **3 — page exists, tested solid.** The top rung: a page exists and you tested `confident`. | Page exists **and** latest score is `confident` |

The ladder encodes two axes: (a) **is it written up?** (`missing`/`pulled` = no page;
`untested`/`revisit`/`covered` = a page exists) and (b) **has `/tutor` tested it?**
(`untested` = not yet; `revisit`/`covered` = tested).

## Step 7 — Target and subgoals

Draft `## Target` (one sentence: what the learner will understand or be able to do by
the deadline) and `## Subgoals` (one per thematic cluster of the scope).

## Step 8 — Write goal.md

Create `course/<slug>/` if needed and write `course/<slug>/goal.md` from
`.claude/Templates/goal.md`. Frontmatter `type: goal`, `hours_per_week`, `tutor_prompt_mode: unset`,
`testing_mode: unset` (set later by `/tutor` to `test` | `honor`), `coverage_pct: 0` (no
`hours_per_day` — the week is the only budget). Knowledge Audit is the 6-column table (`Item | Type | Status |
Score | Last tested | Source`); untested items carry `—` for Score/Last tested.

`coverage_pct` and the Score/Last tested columns are kept in sync by `/tutor`; leave
them at their initial values here.

## Wrap up

Report: `course/<slug>/goal.md` written; counts of covered / revisit / untested /
pulled / missing items.

Then **auto-hand off to `/curriculum`** — a goal and its curriculum are linked, so do
not stop at the goal:

1. Tell the user you'll now build the curriculum, and that `/curriculum` will pull
   vetted resources (papers + Wikipedia + blogs) into this course's library — the most
   expensive step. Give them a chance to adjust the scope first (`/goal edit <slug>`) or
   to skip the auto-handoff if they only wanted the goal for now.
2. Unless they decline, **invoke `/curriculum <slug>`** straight away (it reads the goal
   you just wrote and continues the pipeline through to an initialized `progress.md`).
3. If they decline, point them to run `/curriculum <slug>` themselves when ready, and to
   `/goal edit <slug>` to adjust the goal.
