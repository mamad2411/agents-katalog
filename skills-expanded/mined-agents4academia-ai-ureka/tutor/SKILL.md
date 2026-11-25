---
description: Learn a course in scheduled hour-blocks — the tutor hands over a reading list of the real paper/blog/Wikipedia links, teaches the session's module, suggests ingesting what you read, then (if you opt in) drills adaptive flashcards or trusts the honor system, tracks mastery, and advances. Third stage of a course.
argument-hint: <slug> — next session; or "<slug> hour <N>", "<slug> review", "<slug> drill [module|topic]"
allowed-tools: Read, Write(course/**), Write(sources/**), Glob, Bash(date:*), Bash(cp:*)
---

Drive a course **session by session** for **$ARGUMENTS**, one scheduled hour-block at a time —
the third stage of the `/goal → /curriculum → /tutor` pipeline. Each session runs the steps
below: reading list → teach → suggest ingest → (test | honor) → recap → advance, tracking
mastery in `course/<slug>/progress.md`.

**Modes** (parse from **$ARGUMENTS**):
- `<slug>` — the next scheduled session (reading list + teach + ingest + test/honor +
  recap). Default.
- `<slug> hour <N>` — run a specific scheduled hour-block instead of the next one.
- `<slug> review` — spaced-repetition only: skip the reading list, teaching, and ingest
  prompt; drill all due items (test track only).
- `<slug> drill [module|topic]` — **on-demand** flashcards for a module or sub-topic,
  ignoring due dates. Scores are still recorded.

If **$ARGUMENTS** is empty, glob `course/*/goal.md`, read each `title`, list the
courses, and ask which to run.

---

## Step 1 — Load the course

Read `course/<slug>/goal.md`, `plan.md`, `schedule.md`, `progress.md`, the `modules/`
docs, and the **`course/<slug>/library/`** files (the fetched resources — their
frontmatter holds the **canonical URLs** and credibility tiers you need for the reading
list). Extract the target, `tutor_prompt_mode`, `testing_mode`, `deadline`,
`hours_per_*`, the module map (the prerequisite chain), and the Item Progress + Module
Mastery tables. If `plan.md`/`progress.md` are missing, offer to run `/curriculum <slug>`
first.

## Step 2 — Set preferences (first run only)

If `testing_mode` is `unset` in `goal.md` frontmatter, ask how the learner wants their
knowledge level updated:

> How should I gauge your progress each session?
> 1. **Test me** — drill adaptive flashcards and score me (mastery is measured)
> 2. **Honor system** — no flashcards; I'll ingest only material I've actually read and
>    you trust that as progress

Write the chosen value (`test` | `honor`) to `goal.md` frontmatter. It can be overridden
per session if the user asks.

If `tutor_prompt_mode` is `unset`, also ask (governs `/edit`'s re-test reminders):

> After you edit a page this course covers, when should I remind you to re-test?
> 1. **At session end** — once per edit session, at the very end (recommended)
> 2. **After 3 edits** — prompt after every 3 edits to covered pages this session
> 3. **Never** — I'll run `/tutor` manually

Write `session-end` | `after-3-edits` | `never` back to `goal.md`. `/edit` reads it —
see **Tutor prompt trigger** at the bottom.

## Step 3 — Pick this session

(`review` and `drill` modes skip teaching and ingest — jump to Step 7.)

Get today's date (`date +%Y-%m-%d`) — used only for spaced-repetition intervals, **not**
to gate the schedule (the learner studies whenever they like). In `schedule.md`, find the
first un-ticked `## Week <W> · Hour <H>` block; the module(s) it names are **this
session's target**. For `hour <N>`, use that block. If every block is ticked, tell the
user the schedule is complete and switch to `review` mode. From `plan.md`'s Resources list
(and the module's `sources:` frontmatter), gather **this session's resources** — the
specific library files / links assigned to this hour-block's module.

## Step 4 — Hand over the reading list

Before teaching, give the learner the session's **reading list of real sources to go read on
their own** (in Zotero / Notion / Obsidian) — **the actual links, not the `library/.md`
files**. For each resource, pull from its `library/<file>.md` frontmatter and present:

- **Title + canonical link** — the `url:` (web) or `source_links:` arXiv/blog URL, clickable.
- **Kind · credibility tier** (paper / Wikipedia / blog · canonical / reputable).
- **TLDR (one line)** — *why you recommend it* and *what the learner will get* (e.g. "the
  original CFM objective + Gaussian/OT paths — read this for the derivation").
- **Quick-browse** — a pointer to the `library/<file>.md` summary to skim if they don't want
  the full source now.

Frame it as *go read and annotate these from the source; the summaries and lecture are your
quick reference.* Keep it tight — only this session's resources, ordered as the module uses them.

## Step 5 — Teach

Present a tight, grounded synthesis of this session's scheduled module sections, read straight
from `course/<slug>/modules/<n>-<slug>.md` — this is the "lecture", and the quick-browse
companion to the reading list. **Never invent**: explain only what the cited module
content covers, in the session's ~1-hour budget. Offer to go deeper on any part before moving on.

## Step 6 — Suggest ingesting into the personal base

After teaching, **suggest in plain prose** (a short list — **no `AskUserQuestion` or pop-up
box**) that the learner ingest the session's material into their personal base. For each
resource:

1. **Suggest the matching helper command using the resource's real title**, not the library
   slug — `/zotero "attention is all you need"` (PDF + annotations), `/alphaxiv …` (arXiv), or
   `/web <url>` (Wikipedia/blog). The learner reads and annotates the source themselves, then
   ingests those annotations.
2. **Dedup-check first**: glob `papers/`/`concepts/`/`sources/`/`notes/` for a match. If one
   exists, suggest an **update** instead of a duplicate (re-ingest for fresh annotations, or
   re-run `/collate`/`/edit <page>`) — naming the file it matches.

This is a suggestion, not a gate — continue to Step 7 without waiting, noting anything the
learner says they ingested. (Invoke a helper only if they explicitly ask you to ingest for them.)

## Step 7 — Test or honor (branch on `testing_mode`)

### Track A — `test`: adaptive flashcards

Drill this session's items and **update the knowledge level from both the curriculum material
and what's now in the personal base** (papers/sources/concepts/notes ingested in Step 6
or earlier).

**7A.1 — Build the flashcard queue.** Candidate items come from the Item Progress table.
Order them with **streak-graded spaced repetition** — an item is *due* when days since
`Last tested` ≥ its interval:

| Streak | Retest interval |
|--------|-----------------|
| 0 | 1 day |
| 1 | 3 days |
| 2 | 7 days |
| 3+ | 14 days |

Queue priority (first → last): **wrong → partial → untested → confident & due**.
Confident items not yet due are skipped. Within a tier, oldest `Last tested` first.

- **This session**: items from this session's module that are due, plus any resurfaced due
  items from *mastered* earlier modules.
- **`review`**: every due item across all modules.
- **`drill`**: every item in the named module/topic, due or not.

**Adapt to mastery (Bloom escalation).** Each item carries a `Bloom` level
(remember → understand → apply → analyze → evaluate). Generate each flashcard **live**
from the module content at the item's current level — but for items from a *mastered*
module, pose the **next level up** (a `remember` definition becomes an `apply`/`analyze`
prompt). Tell the user the queue size (~3 min/item); they can type "done" anytime to end
early and still save scores.

**7A.2 — Question loop.** For each queued item, generate one flashcard from its module
page, varying type across the session (don't repeat a type twice in a row):

| Type | When | Example |
|------|------|---------|
| Definition | first-time / `remember` | "Define a probability path $p_t$ precisely." |
| Mechanism | a described process | "Walk through how the CFM loss is computed." |
| Comparison | two related items | "How does the OT path differ from the diffusion path?" |
| Application | `partial`/`revisit`/`apply`+ | "When would you prefer rectified flow, and why?" |
| Maths | pages with equations | "Write $\mathcal{L}_\mathrm{CFM}$ and explain each term." |

For maths, quote the LaTeX so the precision expected is clear. Accept: an **answer** →
score it; **"skip"** → no score change, move on; **"show"** → display the cited passage,
move on without scoring; **"done"** → end the session.

Score each answer:

| Score | Criterion |
|-------|-----------|
| `confident` | Correct and precise; no significant gaps |
| `partial` | Mostly right but missing a key detail or a minor error |
| `wrong` | Missed the core idea or significantly incorrect |

After scoring: show the relevant cited passage, give 1–2 sentences of feedback, and
update the item's **streak** (`confident` → +1; `partial`/`wrong` → reset to 0) and its
**Bloom reached** (raise it when the learner answers a higher-level prompt correctly).
When an item is also backed by an ingested personal-base page, you may draw the
follow-up/feedback from that page too — the knowledge level reflects curriculum **and**
personal base.

**7A.3 — Mastery gating (advisory).** A module is **mastered** once ≥80% of its items are
`confident`, each with streak ≥2 (the canonical rule lives in `.claude/src/curriculum_utils.py`).
If this session's module isn't mastered yet, recommend staying on it but let the user advance.
Don't surface a downstream module's items until its prerequisite module is mastered (`locked`).

### Track B — `honor`: trust what was read

No flashcards. The learner has self-reported reading the session's sources and (Step 6)
ingested them. **Update the knowledge level from the new personal-base material alone**,
on the honor system — you trust that the learner only ingests material they've actually
finished:

- For each of this session's items now backed by an ingested page/source in
  `papers/`/`concepts/`/`sources/`/`notes/`, mark its Item Progress `Score: read` (the
  honor marker — distinct from a tested `confident`), set `Last tested` to today, and
  leave `Streak` at 0.
- Items with no ingested backing stay `untested`. Briefly note which items are still
  unbacked so the learner knows what's outstanding.
- Honor `read` items count as **`untested`** in the goal audit (read, not tested) — not
  `covered`, which still requires a tested `confident`. Mention they can switch to
  `test` mode anytime to verify and raise true coverage.

## Step 8 — Recap and next steps

Print a recap:
- **Covered**: module + items learned/tested this session, and which sources were ingested.
- **Test track** — Scores (confident / partial / wrong / skipped); **shaky items**
  (`partial`/`wrong`, each with a "re-read §X" pointer); **spaced-rep forecast** (which
  items are due next and when).
- **Honor track** — items now `read`/ingested vs still outstanding; the read/ingested
  count alongside tested coverage.
- **Next session**: the next un-ticked day from `schedule.md` and its module.
- **Suggest next steps**: e.g. ingest a still-missing source, run `/collate` to fold new
  reading into a page, switch test/honor mode, or (test track) re-test shaky items.

If a module crossed the mastery threshold this session, add an **end-of-module milestone
recap**: module mastery %, deepest Bloom reached, a "you can now…" tied to its learning
objectives — then unlock the next module.

## Step 9 — Write progress.md and sync

Update `course/<slug>/progress.md`:
- **Item Progress** rows: new `Score` (`confident`/`partial`/`wrong` on the test track;
  `read` on the honor track), `Bloom`, `Last tested` (today), `Streak`. Carry over rows
  not touched this session unchanged.
- **Module Mastery** rows: recompute Mastery %, Confident, Bloom reached, Status.
- Frontmatter: recompute `coverage_pct` (**confident** items ÷ all items — honor `read`
  items do **not** count toward it) and `course_mastery_pct` (mean of module mastery %);
  set `last_updated` to today.

Then **sync `goal.md`**: overwrite the Knowledge Audit `Status`/`Score`/`Last tested` to
match — `covered` for confident items, `untested` for honor `read` items, `revisit`
for partial/wrong — and update its `coverage_pct`. **Tick** completed days in
`schedule.md` and any finished modules in `plan.md`'s weekly plan. Change nothing else.

## Step 10 — Promote mastered material to the personal base

Course material lives in the **per-course library** `course/<slug>/library/` until absorbed.
At the **end of the session** (after the recap), identify library sources eligible for
promotion. A `course/<slug>/library/<file>.md` is **eligible** when any holds:

- **Covered** — backing items all `confident` (100% covered), even before streaks reach the
  `mastered` bar. Offer as soon as a module hits 100% confident; don't wait for the retest.
- **Mastered** — its module is `mastered` (per Step 7A.3).
- **Ingested + annotated** — the learner ingested it into the personal base (the honor-track
  promotion path).

For eligible sources, **suggest promoting them into the personal `sources/`**, noting which
bar triggered it (e.g. *"Module 1 is 100% covered — add these to your personal sources?"*).
On **yes**, `cp course/<slug>/library/<file>.md sources/<file>.md` (keep the library copy).
Once in `sources/` it enters the retrieval index, so a future `/goal` audit finds it without
re-fetch and `/collate`/`/concept` can synthesise it into a page. **Never promote silently**,
and never below 100% covered (test) / ingested (honor). If the learner already ingested the
real source in Step 6, that personal page is the durable copy — no library promotion needed.

## Step 11 — Advance

Move the course forward: confirm this session's hour-block is ticked in `schedule.md`, and
point the learner at the **next hour-block's module** (or the next module if this one is
complete). Offer
to continue now (`/tutor <slug>` for the next hour-block, or `/tutor <slug> hour <N>`), or
to stop here. If the schedule is finished, suggest `/tutor <slug> review` to keep due items
fresh.

## Wrap up

Beyond the recap, promotion offers, and the advance pointer, ask:
- (Test track) Re-test any wrong/partial items now?
- Incorporate into your personal knowledge base (or update) a source you read today that isn't in the base yet?
- Open a page that revealed gaps via `/edit <page>`?

Then respect `tutor_prompt_mode` for the next `/edit` (below). **Do not reindex
manually** — the background poller handles it.

---

## Tutor prompt trigger — spec for `/edit` integration

When `/edit` finishes on a page it should respect the user's cadence:

1. Glob `course/*/goal.md`. For each, check whether the edited page's slug/title appears
   in its Knowledge Audit or the course's Module Map. If no match, do nothing.

2. For a matching course, read `tutor_prompt_mode`:

   **`session-end`** — at the very end of the `/edit` wrap-up (once per session, even if
   several pages in the course are edited), append:
   > *Course `<slug>` covers this page — remember to run `/tutor <slug>` this session.*
   Track with a flag file `course/<slug>/.session_reminded` (deleted on session start,
   created on first reminder).

   **`after-3-edits`** — read the integer in `course/<slug>/.edit_count` (0 if absent),
   increment, write back. When it reaches 3, prompt:
   > *You've edited 3 pages covered by course `<slug>` this session — run `/tutor <slug>`?*
   Then reset `.edit_count` to 0.

   **`never`** or `unset` — no prompt.
