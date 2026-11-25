---
description: Build a curriculum for a goal — pull vetted resources (papers, Wikipedia, blogs, tutorials), sequence them into modules, schedule against your hours, and compile a cited course doc per module. Second stage of a course; consumes /goal, hands off to /tutor.
argument-hint: <slug> (an existing goal) — or <topic> [by <deadline>] [<H> h/week] to scope inline; or "edit <slug>"
allowed-tools: Read, Write(course/**), Glob, Bash(date:*), Bash(sh .claude/src/pyrun:*)
---

Build the **curriculum** for a course on **$ARGUMENTS** — like a university syllabus:
**pull factual, verifiable, widely-used resources** (papers + Wikipedia + blogs +
tutorials/docs), sequence them into modules (foundational → core → advanced), schedule
them against the deadline and hours, and **compile one cited course doc per module**.

This is the second stage of the learning pipeline — it consumes the goal and hands off
to the tutor:

```
/goal <topic>   →  course/<slug>/goal.md   (target + scope + knowledge audit)
/curriculum <slug>  →  plan.md + schedule.md + modules/ + initialized progress.md
/tutor <slug>       →  each session: reading list → teach → (test|honor) → advance
```

Output lives under `course/<slug>/`:
- `plan.md` — module map, resources, weekly plan, feasibility
- `schedule.md` — hour-by-hour breakdown driven by your weekly hours
- `modules/<n>-<slug>.md` — compiled, **cited** learning material per module
- `progress.md` — initialized so `/tutor` has a populated item list from the first session

Fetched material — a full **concept web** (built via `/autoexplore`) — goes into this
course's **per-course library** `course/<slug>/library/`, laid out in vault-style type
subfolders `sources/`, `papers/`, `concepts/` — *not* the personal `sources/`, and kept
**out of the retrieval index** (resolved by filesystem; graduates into personal `sources/`
only when `/tutor` promotes a mastered item). Module docs cite it at
`../library/<kind>/<file>.md`, `plan.md` at `library/<kind>/<file>.md`. **Every library
source records the resource's canonical URL** (`url:`/`source_links:`) so `/tutor` can build
a reading list of real paper/blog/Wikipedia links.

Orchestrates **`/autoexplore`** (resource acquisition), `/web`, `/alphaxiv`, `/collate`,
`/retrieve`. **Read `.claude/AGENTS.md` "Page conventions"** before writing any module doc.

If **$ARGUMENTS** starts with `edit `, extract the slug and jump to **Edit Mode**.

---

## Step 1 — Resolve the course and load the goal

Slugify **$ARGUMENTS** to kebab-case and look for `course/<slug>/goal.md`.

- **Goal exists** → read it. Take the **target**, **scope** (in/out), **deadline**,
  **hours_per_week**, and **Knowledge Audit** (covered / pulled / untested /
  missing) straight from it — that scope is what you pull resources against. This is
  the normal path.
- **No goal** → the goal stage hasn't run. Offer to run `/goal <topic>` first
  (recommended). If the user would rather not, scope inline: parse topic + deadline
  (`date +%Y-%m-%d`, `"open-ended"` if absent) + **hours per week** (the only time budget;
  suggest 5 h/week — do not assume a per-day rate), draft an in/out scope, and write a
  minimal `course/<slug>/goal.md` from `.claude/Templates/goal.md` before continuing.

If `course/<slug>/plan.md` already exists, ask: update it (→ **Edit Mode**) or
overwrite?

## Step 2 — Build the library concept web (delegated to `/autoexplore`)

Fill the goal's `missing`/`pulled` gaps by **running the `/autoexplore` concept-web build**
against this course, so the curriculum is designed over a real interlinked web, not just flat
abstracts. Invoke `/autoexplore` with **destination `course/<slug>/library/`**, **`--hops 0`**
(search-only — citation snowball is the slow part, and the queries already surface the
canonical papers; bump to `--hops 1` only if the user wants citation-depth), **topic/scope** =
the goal's target + in/out scope, and **skip the standalone synthesis page** (the module docs
are the synthesis). It writes the type-subfolders `papers/<slug>.md`, `concepts/<slug>.md`,
and `sources/alphaxiv_*`/`sources/web_*` (Wikipedia + vetted blogs, credibility-scored). Keep
volume modest — this is the most expensive step.

**Constraints (enforced by `/autoexplore`, restate when invoking):**
- **Never write the personal `sources/`/`papers/`/`concepts/`** — only the course library.
- **Reuse, don't refetch:** if the file already exists in this library, another course's
  `course/*/library/`, or the personal `sources/`, cite/copy it instead of re-fetching.
- **Canonical URL on every kept file** (`url:` web, `source_links:` papers) — `/tutor`'s reading list.
- If the paper pull fails (no `.env`/network), say so and continue with web + base only.

Track every kept source with its `kind` and credibility `tier` for the Resources list.

## Step 3 — Design the module sequence

Cluster the **library concept web** (the `concept_*` pages + their `paper_*`/`web_*`
sources, plus anything audited from the personal base) into **modules** (thematic units),
ordered foundational → core → advanced. Use the concept web's cross-links to spot natural
module boundaries and the prerequisite chain:
- earlier publication year / survey (`is_review`) / encyclopedic overview → earlier;
- a concept many others link *to* (a foundational hub) → earlier;
- more overlap with what's already in the base → more accessible → earlier;
- a resource/concept introducing many not-yet-covered concepts → more advanced → later.

Give each module a name, level label, assigned resources, and learning objectives.
Aim for 3–6 modules unless the timeline is long. The module order is also the
**prerequisite chain** the tutor uses for mastery gating.

## Step 4 — Schedule against the timeline

- **Estimates:** ingest+read a new paper ≈ 4 h; read a compiled module doc ≈ 1–2 h;
  Wikipedia/overview ≈ 0.5–1 h; tutorial/blog ≈ 1 h; exercises ≈ as noted.
- **Weekly plan** (`plan.md`): group modules into weeks given `hours_per_week`.
- **Hour-block schedule** (`schedule.md`): break each week into **~1-hour blocks** sized
  by `hours_per_week` (e.g. 3 h/week → `Hour 1`, `Hour 2`, `Hour 3` that week), **anchoring
  each block** with a `## Week <W> · Hour <H>` heading and naming the module it covers —
  `/tutor` reads these to pick the next session's teaching target. **Do not schedule by
  day or assume a per-day rate** — the week's hours are the only budget, and the learner
  spends them whenever they like.
- **Feasibility:** compare total estimated hours to available hours. If it overflows,
  flag clearly and ask: extend deadline, cut scope, or keep ambitious.

## Step 5 — Compile module docs

For each module, write `course/<slug>/modules/<n>-<slug>.md` from `.claude/Templates/module.md`,
synthesising **only** that module's cited sources, **per AGENTS.md "Page conventions"** and
`/collate` semantics. Cite every claim inline with a relative link to its library file
(`../library/concepts/<slug>.md`, `../library/papers/<slug>.md`,
`../library/sources/{web,alphaxiv}_<slug>.md`) or a base page (`../../../{papers,concepts}/…`).
Include learning objectives, key equations, further reading, and a rich **`## Self-check`** —
the seed pool `/tutor` draws live flashcards from, so cover every learning objective. You may
delegate synthesis to `/collate` where a clean page maps to a module.

## Step 6 — Write plan.md, schedule.md, and initialize progress.md

- **`plan.md`** from `.claude/Templates/curriculum.md`: timeline + feasibility, module map
  table, weekly plan, resources list with tiers, notes. (Target/scope/audit stay in
  `goal.md`.) In the resources list, link each item both to its library file
  (`library/<kind>/<file>.md`, e.g. `library/papers/<slug>.md`) **and** to its canonical URL
  — the plan doubles as the reading list `/tutor` will surface.
- **`schedule.md`**: the hour-by-hour breakdown with `## Week <W> · Hour <H>` anchors.
- **`progress.md`** from `.claude/Templates/progress.md`: **initialize** it so `/tutor` starts
  with a full item list — every module's learning items in the Item Progress table at
  `Score: untested, Bloom: —, Streak: 0`, and a Module Mastery row per module at
  `0% · available` (`locked` for modules whose prerequisite isn't first). Set
  `coverage_pct: 0`, `course_mastery_pct: 0`.
- **Sync `goal.md`**: update the Knowledge Audit `Status` to `pulled` for items you
  pulled resources for this run.

## Wrap up

Per AGENTS.md "Review": report `course/<slug>/` written (plan + schedule + N module
docs + initialized progress); counts of resources pulled by kind/tier and any dropped
(low-credibility) ones; anything left out; whether the schedule fits the hours. Then
ask whether the user is happy or wants to co-edit — loop via
`/edit course/<slug>/modules/<n>-<slug>.md` (or `plan.md`) until they're happy. **Do
not reindex manually** — the background poller rebuilds the index after edits settle.
Finally, point them to **`/tutor <slug>`** to start learning: each day it hands over a
reading list of the real paper/blog/Wikipedia links, teaches the module, prompts you to
ingest what you read into your personal base, then (if you opt in) tests you — or trusts
the honor system — before advancing.

---

## Edit Mode — `/curriculum edit <slug>`

Adjust an existing curriculum without rebuilding from scratch.

1. **Load** `course/<slug>/goal.md` + `plan.md` (+ `schedule.md`); show current state.
2. **Ask what to change** (several allowed):
   - Change deadline or hours (→ recompute the weekly plan + hour-block schedule).
   - Add/remove a module or a resource (pull new ones via Step 2 for just that topic).
     Adding/removing a module also adds/removes its rows in `progress.md`.
   - Mark modules/items done.
   - Add free-form notes.
3. **Apply** the edits; if timing changed, redo Step 4's assignments.
4. **Write** the updated `plan.md`/`schedule.md` (+ any new module docs, + synced
   `progress.md` rows) and report what changed. Do not clobber learner scores already
   in `progress.md` — only add/remove rows.
