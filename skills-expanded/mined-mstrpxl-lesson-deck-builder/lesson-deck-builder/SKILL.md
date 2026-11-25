---
name: "lesson-deck-builder"
description: 'Build a polished, hand-drawn slide-style HTML lesson or presentation as one self-contained .html file (slide engine, paper or six chalkboard boards, Arabic or English, visual card library, validator). Use WHENEVER the user wants a deck, slides, a lesson, an explainer or a visual walkthrough on any topic, or says "explain the attached file", and for a learning journey or its next lesson. It routes itself: an attached lecture or document (PDF or PPTX) follows the bundled slides rulebook and ends with a self-marking quiz; a teaching request without one follows the bundled lessons rulebook; pitches and showcases use the base workflow. Earlier decks attached as HTML carry the course''s choices and memory; nothing else is attached. Once per course or journey it asks the canvas (paper, or chalkboard and its board) and, for English decks, the reading level (A2-C1); it asks Arabic or English unless the route fixes it. NOT for native .pptx (use the pptx skill) or the locked deck-infographics system.'
---

# Lesson-Deck-Builder

Produce one standalone `.html` file that opens in any browser as a calm,
navigable slide presentation. The look is **Sketchbook** — a teacher's
notebook on ruled paper, or a blackboard in chalk, that draws itself while you
watch: calm, visual-first, and understandable by a complete newcomer to the
subject. The slide engine, theming, component library, and a
validator are all bundled; assembling a deck is mostly **planning the narrative
and filling slides**, not writing CSS or JS from scratch.

## How to read this skill (goals first)
- **Fixed:** the goals (a deck that teaches or informs, correct, readable at the
  reader's level), the user's choices (canvas, board, language, English level,
  length), and the technical contracts that keep a deck working (the engine
  script, `validate.py`, one self-contained file, no storage APIs).
- **Defaults, not limits:** the workflow, the numbers, the component
  suggestions, the tool tips, the rulebooks' procedures and the general notes
  were written and tested for the models and tools of their date. When you can
  meet the goals better (a better reading tool, a clearer structure, a stronger
  or faster check, a component the catalogue lacks), do it, and name what you
  changed and why in the closing report ("Departures"). Never trade away a goal
  or a user choice for speed.
- **Ask only what is the user's to decide;** decide the rest and report it.

## What this skill produces
A self-contained HTML deck: a hand-drawn Sketchbook canvas (bright ruled paper,
or a chalkboard in one of six boards), hand-lettered Arabic/Latin typography,
one slide per screen, arrow/keyboard/swipe navigation, a progress
bar, slide counter, dots, and content built from a reusable card vocabulary
(window mockups, chat, feature grids, comparison tiers, flows, code windows,
icons, etc.). It renders in **Arabic (RTL)** or **English (LTR)** — the user
picks, and the layout, fonts, and navigation adapt to that choice. English decks
are written at the reader's level, from A2 to C1 (step 2b).

## Two kinds of deck — decide once, early
- **Teaching deck** — the goal is that the reader *can do or understand
  something new* afterward (lessons, explainers, tutorials, every deck in
  roadmap mode). Teaching decks follow the **teaching arc** and end with the
  **question set + adaptive loop** (both below).
- **Presentation deck** — the goal is to *inform or persuade* (a pitch, a
  product intro, a showcase, a report). Presentation decks use the classic arc
  and skip the challenge/questions machinery entirely.

If the request is ambiguous, one tappable question settles it. When in doubt
about a deck built to explain a concept, treat it as a teaching deck.

## Bundled resources — read these as you go
- `assets/template.html` — the deck engine, in Sketchbook. **Always start by
  copying this.** It contains all CSS (both canvases, all six chalkboard boards,
  the bridge tokens, the shared SVG defs), the navigation/reveal/build
  JavaScript (engine v2 — do not edit the engine part of the script; component
  code goes after it), and three example slides between the `BEGIN/END SLIDES`
  markers. The canvas is one attribute pair on `<html>` (step 6).
- `references/style-system.md` — **Sketchbook, its two canvases and six
  boards, the five global laws, and the drawing vocabularies kept from the
  retired families.** Authoritative for visuals: read it before planning, and
  follow its scene-brief procedure to generate per-topic illustrations. Its
  pre-ship checklist is mandatory.
- `assets/style-samples/` — exemplar decks: `sketchbook.html` (paper),
  `sketchbook-chalkboard.html` (chalkboard; the top-bar dots preview every
  board and paper) and `sketchbook-kit.html` (the mechanics ported from the
  retired families — stepper skeleton, skins stepper, lab, tray, footnotes,
  duo panes, token journey, spotlight cover, smudge panels, key passage). Study them for vocabulary and mechanics —
  never reuse their illustration subjects (Law 2).
- `references/design-system.md` — aesthetic rules, the canvas attributes,
  font pairings, direction handling, and the reading-time → slide-count budget.
- `references/components.md` — copy-paste HTML for every slide block, each with a
  ranked **Suggested for** list of use cases. **Read before filling slides.**
- `references/use-cases.md` — the catalogue of teaching jobs (use cases): each
  explained once with examples, plus a reverse index of the components that
  suit it, best fit first. **Read while planning (step 5).**
- `scripts/validate.py` — a fast sanity check on the finished file.
- `scripts/use_cases.py` — maintenance check for the skill itself: keeps the
  components' Suggested-for lists and `use-cases.md` in sync (`--write`
  refreshes the reverse index). Run it after editing either file.
- `rulebooks/` — the route rulebooks and their kit, read when a route needs
  them (step 0b): `slides-rulebook.md` (lecture route; its phone rules also serve the lesson route),
  `questions-rulebook.md` (its final quiz), `lessons-rulebook.md` (lesson
  route), `deck-notes-general.md` (experience from earlier decks, not rules),
  `deck-tools/` (language checker, quiz walk, code snippets, build and
  screenshot helpers; `snippets/README.md` maps them; run `setup_tools.sh` once
  per session from your working folder) and `rulebooks-changelog.md` (history,
  not needed for a run).

---

## Workflow

### 0 — Detect the environment (repo mode vs chat mode)
The skill runs in two environments, and behavior differs. Detect which one
this is before anything else:

- **Repo mode** — invoked from Claude Code (or any session with a persistent
  working folder). The skill turns the repo into a learning environment and
  controls its files directly. On a new journey in an empty (or learning-free)
  repo, scaffold this layout, creating only what is missing:

  ```
  docs/TOPIC.md        confirmed topic + aim (output of the topic conversation)
  docs/ROADMAP.md      the living roadmap: readable path + spec + changelog
  docs/NOTES.md        cumulative learner notes
  lessons/             the decks: 00-roadmap.html, 01-<step-slug>.html, …
  answers/             each pasted answer block saved verbatim: lesson-01.txt, …
  ```

  Canonical state lives on disk: read `docs/` before building, write results
  back after. Never overwrite or reorganize files that aren't the skill's own;
  if the repo already has unrelated structure, fit the learning folders in
  alongside it, and ask when placement is ambiguous. If the repo is
  git-initialized, commit after each artifact with a clear message
  ("lesson 03: transformers — attention", "notes: lesson 02 answers").

- **Chat mode** — invoked on Claude web/app, with no persistent repo between
  sessions. Default to a **single-deck lesson** per request: topic
  conversation, then one self-contained teaching deck. The full series
  machinery (roadmap, NOTES.md, answers archive) is repo-native — offer it as
  "this works best from a folder with Claude Code" if the user asks for a
  series, and only if they still want it in chat, use the fallback: the
  roadmap spec and the learner notes travel as HTML comments inside each
  lesson file (`ROADMAP-SPEC` and `LEARNER-NOTES`, the same content as
  `docs/ROADMAP.md` and `docs/NOTES.md`). The user re-attaches only the latest
  lesson; never ask them to save or re-send Markdown files.

### 0b — Route the request (one line is enough)
The user may send as little as "use /lesson-deck-builder to explain the
attached file". Choose the route from what is attached and asked:

| Route | When | Follow |
|---|---|---|
| **Lecture** | a file to explain is attached: lecture slides or a document, as PDF or PPTX | `rulebooks/slides-rulebook.md`, ending with the final quiz of `rulebooks/questions-rulebook.md` |
| **Lesson** | a teaching request without such a file: a topic, "the next lesson", a learning journey | `rulebooks/lessons-rulebook.md`, with this skill's roadmap and notes machinery |
| **Presentation** | a deck that informs or persuades (pitch, product intro, showcase, report) | this file alone |

- **The user's words beat the files:** "a short pitch from this PDF" is a
  presentation. When the route is unclear, one tappable question settles it.
- **Everything else ships with the skill:** the rulebooks, the general notes
  (`rulebooks/deck-notes-general.md`) and the tools (`rulebooks/deck-tools/`).
  Use the tools where they help.
- **What the user attaches:** the file to explain and, for a later deck of a
  course or journey, the previous deck (HTML). Its record (`COURSE` or
  `DECK-SETTINGS`) holds the standing choices and the course's memory, and the
  deck is the shell. No earlier deck attached means a first deck: ask the
  canvas, the board and the English level before building. Older decks are not
  attached; ask for one only when you need a figure or a glossary wording from
  it.
- **A course deck without its new lecture:** when a deck with a `COURSE`
  record is attached but no new file to explain, ask for the new chapter's PDF
  (or PPTX) before doing anything else: no planning, no building, and no
  switch to the lesson route. Not when the user asks to change the attached
  deck itself (fix it, add a quiz, switch the board), and not for a deck with
  `DECK-SETTINGS` (a lesson journey needs no file).
- **No Markdown goes back and forth.** Never ask the user to attach or save
  notes, rulebooks or tool archives, and don't send them. What a run learns
  goes into the deck's record (facts about this course or journey) or on the
  report's "Proposed for the skill" line (anything that would help every deck).
  The skill's own files change only in a maintenance session.
- **Precedence on a rulebook route:** the user's words, then the deck's
  record, then the rulebook, then this file where the rulebook is silent (each
  rulebook's §2 lists what it overrides).

### 1 — The topic conversation (required before anything is built)
On the **lecture route** the attached file is the topic: skip this step (the
slides rulebook's W5 asks only what needs deciding). On the **lesson route** it
runs as below until the topic is known; then the lessons rulebook takes over.

Every **new learning journey** starts with a short discovery conversation
whose only goal is to confirm, together, the right topic — because a
mis-aimed topic silently corrupts every deck built after it. No deck, no
roadmap, no scaffolding happens before this conversation ends in an explicit
confirmation. (Skip it only when continuing an existing journey whose
`docs/TOPIC.md` already records a confirmed topic.)

How to conduct it:
- **Assume zero knowledge and stay non-technical.** Questions are about what
  the learner wants to be able to do or understand, never about jargon they'd
  have to already know to answer.
- **Map the territory out loud.** List the candidate topics around what they
  said — including neighbors and overlaps they might actually mean — with a
  one- or two-line plain-language sketch of each, so the learner becomes
  aware of what the options really are before choosing. Simplify for now;
  precision comes later. Prefer tappable choices where the interface allows.
- **Remap and reconfirm — even when they're precise.** If the learner states
  exactly what they want, don't just accept it: restate it in your own words,
  place it on the map ("that sits inside X, next to Y, and excludes Z"), and
  ask them to confirm the restatement. The conversation may be short in this
  case, but it is never skipped.
- **End on one thing.** The conversation closes only when a single topic — or
  a single, exactly-worded learning aim — is explicitly confirmed by the
  learner.

Record the outcome: in repo mode, write `docs/TOPIC.md` (confirmed topic,
what it includes and deliberately excludes, the learner's aim restated, date).
In chat mode, restate the confirmed topic in one short message before moving
on. Only then ask the canvas (1b) and the language (2) — they may share one
message; both are answered before any planning.

### 1b — Ask the canvas (required — never decide silently)
The only style is **Sketchbook**; what the user chooses is its canvas. After
the topic is confirmed, run the canvas gate as a **suggest-and-confirm**
question, always in this shape:
1. **Canvas.** Lead with the best fit and a ONE-line reason, and list both:
   **Paper** (bright ruled notebook) · **Chalkboard** (dark board, chalk
   pens). Suggest paper by default; suggest chalkboard when the user's context
   implies night or long screen reading, or when they chose it before.
   Tappable options where the interface allows, suggested one first.
2. **Board** — only when chalkboard is picked, in a short follow-up: lead with
   **Slate re-inked** (the default) unless the user's record says otherwise,
   and list all six with a few-word identity: **Slate re-inked** (green-black
   slate) · **Midnight blue** (deep blue) · **Olive gold** (dark olive,
   leans yellow) · **Dusk indigo** (blue-violet) · **Deep teal** (blue-green) ·
   **Red graphite** (charcoal with an oxblood tint). Preview: the top-bar dots
   of `assets/style-samples/sketchbook-chalkboard.html`.
3. Build nothing until the user picks; their choice is final even against the
   suggestion. For an English deck, ask the English level (2b) in the same
   message.
Never skip the menu, never present only the suggestion, and never choose on
the user's behalf. In a lesson series or a course, ask once and record the
choice (canvas + board) in the deck's record; re-ask only if the user wants a
change. Then read
`references/style-system.md` and skim the exemplars before planning slides.
Playroom, Nocturne, Terra and Classic were retired in v1.3: if a user asks for
one, say so, offer the canvas gate, and mention that their mechanics live on
in `components.md §32`.

### 2 — Ask the language (required, before any planning)
Before planning or generating anything, ask the user which language they want the
deck in: **Arabic or English**. This is mandatory for every presentation/lesson —
do not assume or default. The exceptions: the user already stated the language
(e.g. "make an English deck about…"), or the route fixes it (both rulebooks
build English decks). Prefer a single
tappable question ("Arabic / English"). The chosen language drives the whole
setup:
- **Arabic** → `dir="rtl" lang="ar"`, the Sketchbook Arabic pairing (Playpen
  Sans Arabic 800 + IBM Plex Sans Arabic, `style-system.md §4`), Arabic nav labels
  (`‹ السابق` / `التالي ›`), Arabic UI/eyebrow text.
- **English** → `dir="ltr" lang="en"`, Caveat + Karla, English nav labels
  (`‹ Prev` / `Next ›`), English UI/eyebrow text.

See `design-system.md` §3 (font pairings per language) and §4 (direction
handling). The engine's keyboard/swipe logic flips automatically from `dir` — no
JS edits needed. For bilingual teaching decks (e.g. an English lesson explained in
Arabic), pick the base language for `dir`/fonts, then mix the second language
inside the content as needed — reduce the L1 (support) language as the level rises.

### 2b — Ask the English level (English decks)
Ask the reader's English level once per course or journey, in the same message
as the canvas, and record it in the deck's record: **A2 · B1 · B2 · C1**, the
suggested one first (lecture route B1, lesson route B2, presentations B2), each
with a few words of meaning. Skip it when the record or the user's words give
it. Arabic decks don't ask it. It is the reader's English, not their knowledge
of the subject (that is the intake's audience level).

| Level | Reader | Words | Sentences: cap · usual |
|---|---|---|---|
| A2 | basic | everyday words; anything harder is a taught term | 15 · 8–12 |
| B1 | independent, early | common words; a B1 word when no simpler one fits | 20 · 10–14 |
| B2 | independent | common words; B2 words freely | 25 · 12–18 |
| C1 | proficient | precise and formal words where they are the right ones; no idioms | 30 · 15–20 |

At every level: at least 98% of running words known (taught terms and field
words count), one idea per sentence, every term taught before it is used.
`rulebooks/deck-tools/plain_check.py --max-level <level>` measures it, and its
sentence cap follows the level. The 98% target and the 20/25-word caps come
from research and a standard (the rulebooks' evidence tables); the A2 and C1
caps and the usual ranges are design choices.

### 3 — Scope & mode (broad subjects only)
Judge the **scope** of the confirmed topic before intake. In **chat mode** the
default outcome is always a single deck (see step 0); the roadmap option below
is for repo mode unless the user explicitly insists otherwise:

- **Narrow topic** — a single concept, technique, tool, or question ("knight
  forks", "how vaccines work", "what is a Docker image"). Skip discovery; go
  straight to Intake and build one deck as usual.
- **Broad subject** — a whole field someone could study for weeks (DevOps,
  machine learning, backend engineering, personal finance). This is
  roadmap-suitable: ask ONE tappable question — how do they want to approach it?
  - **Overview** — one thorough deck covering the whole subject at altitude: a
    complete lesson, not a teaser. ~30 min is the *cap* (≤~20 slides); if the user
    asks for shorter, honour it and tighten to the smaller budget.
  - **Roadmap + Lesson 1** — map the field into a validated learning path, deliver
    a standalone roadmap deck, then build the first lesson. See §3a.
  - **Deep dive** — the user narrows to one subtopic; build a single focused deck
    on just that.

Rule of thumb for "broad": *could a person reasonably spend weeks learning this?*
If yes, offer the three modes; if no, skip and proceed to Intake.

#### 3a — Roadmap mode (repo-native; only when "Roadmap + Lesson 1" is chosen)
Extra intake, real research, and two output files. Order matters:

1. **Shape the journey — ask first.** Before researching, ask 2–3 tappable
   questions so the path matches the learner, e.g.:
   - **Style:** hands-on with projects · theory-first foundations · balanced.
   - **Business lens:** include market / "how industry uses this" framing · keep
     it purely technical.
   - **Destination:** job-ready depth · a solid working mental model · general
     literacy.
   Adapt them to the subject. These answers shape **emphasis, ordering, and
   framing — never correctness or completeness.** Don't let a preference drop a
   load-bearing step (a "theory-first" path still keeps the practical checkpoints
   it needs to make sense).
2. **Research the roadmap — required.** Run real web searches before writing the
   path, so it is **current and valid**: right sequence, no outdated tooling or
   dead practices, nothing important missing. Verify the field *today*, not from
   memory. This is *structural* research (what to learn, in what order) — **not**
   the deep per-subject research, which is deferred to each lesson (item 5 below).
3. **Produce the standalone roadmap deck** (its own file — in repo mode,
   `lessons/00-roadmap.html`). A thorough, comprehensive deck that lays out the
   whole path — each phase with what it covers, why it is there, and how it
   connects — shaped by the answers from the shaping questions (item 1). Use
   the roadmap slide (components.md §18) as the spine. Then record the
   **Claude-facing spec** where the environment dictates:

   - **Repo mode:** write `docs/ROADMAP.md` — the canonical living roadmap. It
     holds a human-readable version of the path, the spec JSON below in a
     fenced code block, and the changelog. Every roadmap change is written
     here; the deck is just its rendering.
   - **Chat mode (series fallback only):** embed the spec as a hidden HTML
     comment in the roadmap deck, and carry the current copy forward in every
     lesson file:

   ```
   ROADMAP-SPEC {"subject":"…","version":1,"updated":"YYYY-MM-DD",
        "shape":{…the shaping answers…},
        "steps":[{"n":1,"title":"…","goal":"…","volatility":"fast|solid",
          "research":"the angles, sources, and freshness checks Claude should run
          when building THIS lesson later"}, …],
        "changelog":[]}
   ```

   (`validate.py` strips HTML comments before its checks, so the embedded copy
   never affects the render or the validator.) The roadmap is a **living
   document**, and its update channels are deliberately asymmetric:
   - **Field drift (the primary channel — applied by Claude).** Lessons in a
     series are typically taken days to weeks apart, so parts of the field move
     between them. After every lesson, before building the next, re-check the
     roadmap's validity and freshness against real-world frameworks and
     directions. Tag each step's `volatility` to scale the depth of that check:
     `"fast"` steps (tooling, model choices, evolving practice) get
     re-researched; `"solid"` steps (fundamentals, stable theory) need only a
     light verification — but the check itself happens every lesson.
   - **Learner-approved proposals (the exception — never applied silently).**
     Answers NEVER change the path on Claude's own judgment; they flow into the
     notes file and personalize lesson *content* instead (see "Question set &
     the adaptive loop"). Only when the notes show a persistent gap may Claude
     *propose* a path change, and it applies only after an explicit yes.
   Every roadmap change bumps `version` and appends a `changelog` entry
   (`{"v":2,"date":"…","cause":"research|approved-proposal","change":"…"}`) so
   any future session can reconstruct why the path looks the way it does.
4. **Build Lesson 1** — a teaching deck (its own file) on the first step:
   **introduction · big picture · why.** Put a **roadmap slide** near the front
   (map / linked-cards) showing the full path with the current step highlighted
   and completed steps marked, so the reader always sees where they are and
   what is already behind them.
5. **Later lessons (2, 3, …)** — each its **own file** (repo mode:
   `lessons/NN-<step-slug>.html`), built in this order:
   1. **Load the current roadmap.** Repo mode: `docs/ROADMAP.md` is the single
      source of truth. Chat fallback: the newest lesson file's ROADMAP-SPEC
      comment, then the roadmap deck.
   2. **Read the learner notes** — repo mode: `docs/NOTES.md`; chat
      fallback: the newest lesson's `LEARNER-NOTES` comment (ask for that
      lesson if it isn't attached). If a freshly pasted answer block is in the
      conversation, process it first: in repo mode save it verbatim to
      `answers/lesson-NN.txt`, then fold it into the notes.
   3. **Re-check the roadmap's freshness** against real-world frameworks and
      directions — every lesson, depth scaled by each step's volatility.
      Apply research-driven updates directly: bump `version`, log the change
      with `cause:"research"`, flag it on the roadmap slide.
   4. **Raise a proposal only if the notes justify one.** If NOTES.md shows a
      persistent gap (the threshold in "Question set & the adaptive loop"),
      ask explicitly — in chat, or as a `PROPOSAL:` line inside the next
      deck's answer box — e.g. "Your answers across the last two lessons
      suggest X is shaky. Want me to add a short preparation deck to the
      roadmap at the right point?" Change the path only on an explicit yes
      (`cause:"approved-proposal"`). Never silently.
   5. **Build the lesson** — deep web research for its specific subject guided
      by the step's stored directives, then the deck itself, **personalized
      from NOTES.md**: prior misses re-tested early in new clothing, closed
      gaps named, examples and depth tuned to what the notes show — with the
      roadmap slide reflecting the current path: completed steps marked,
      current step moved, any changed step visibly flagged (components.md §18).
   6. **Write state back (repo mode).** Update `docs/ROADMAP.md` and
      `docs/NOTES.md` with anything that changed, save the deck into
      `lessons/`, and commit if the repo uses git.

### 4 — Intake (gather the rest, briefly)
Language is already settled in step 2. Now gather the rest — if the user already
specified something, skip it. Prefer a short multiple-choice intake (tappable
options) over open prose:

- **Topic & angle** — what is the deck about, and what should the reader walk
  away knowing?
- **Audience level** (knowledge of the subject; the English level is step 2b)
  — complete beginner, generally informed, or expert? Default to "explain so a
  newcomer gains real understanding."
- **Length** — reading-time budget (≈10 / 20 / 30 min). Default ~20 min.
(The look is already settled by the canvas gate, step 1b.)

For an **Overview** deck, ~30 min is the *ceiling* — one file; if the user wants
it shorter, use the smaller budget. For a **Deep dive**, treat the chosen
subtopic as the whole deck.

Don't over-ask. One compact intake round is enough; then proceed.

### 5 — Plan the outline (the narrative arc)
Before touching files, sketch the slide list.

**Teaching arc** (default for teaching decks):

1. **Cover** — title + a one-line promise.
2. **Opening challenge** — a real problem that the deck's core idea solves,
   posed *before any teaching*, with the reader committing to an answer (a
   tappable-style MCQ beat or a "decide before you continue" prompt).
   Calibrate to **attemptable-but-uncertain**: not obvious (no gap to close),
   not impossible (noise, not learning). The reader should have a guess and
   not be sure of it.
3. **Ground the newcomer** — define the subject in plain language; if any term
   must be used later, introduce it here first. Never use an unexplained
   technical idea.
4. **Overview / map** — a feature-cards slide previewing what's coming, plus
   one line on **what this lesson unlocks** in the bigger picture. In roadmap
   mode this *is* the roadmap slide, current step highlighted.
5. **One idea per slide** — walk the concepts in a logical order, each on its
   own slide, each earning a visual (see the click trio under Teaching
   principles).
6. **Transition slides** — when moving between major parts, use an eyebrow like
   "المرحلة الثانية" so the shift is felt.
7. **Challenge revisited** — return to the **exact same** opening problem and
   solve it with the ideas just taught. The same problem, never a similar one:
   the point is the visible before/after. This slide is mandatory in every
   teaching deck.
8. **Recap/flow slide** — phrased as capabilities, not topics: "you can now …",
   where each item was demonstrably out of reach at the cover.
9. **Question set + answer box** — see "Question set & the adaptive loop".
10. **Closing** — the message in one line + a simple next step.

**Presentation arc** (pitches, intros, showcases): Cover → Ground → Map → one
idea per slide → transitions → recap flow → closing, exactly as before — no
challenge, no question set.

Map the length budget to a slide count using the table in `design-system.md`
(~60–90s per slide). Stay within it; tighten rather than add. The challenge
pair and question set are part of the budget, not on top of it.

**Match every slide to a teaching job.** For each planned slide, name its job
from `use-cases.md` (define a term, show a mechanism, correct a misconception…),
then choose a component from that job's reverse index. The rankings are
suggestions, not rules: the first-ranked component is the usual fit, not the
required one. Vary components across the deck, and pick a lower-ranked or
unlisted component whenever the content argues for it.

### 6 — Set up from the template
- Copy `assets/template.html` to your working file.
- Apply the **language chosen in step 2**: set `<html dir lang>`, the `<title>`,
  and the brand label; use that language's font pairing (design-system.md §3);
  and for English (LTR) swap the two nav button labels/arrows to `‹ Prev` /
  `Next ›` (design-system.md §4). The template ships Arabic-ready by default.
- Apply the **canvas chosen in step 1b** on `<html>`: `data-canvas="paper"`, or
  `data-canvas="chalkboard" data-board="<board>"` (`slate-reinked` ·
  `midnight-blue` · `olive-gold` · `dusk-indigo` · `deep-teal` ·
  `red-graphite`). Every token follows; never hand-edit a board's colours.
- **Do not edit the engine part of the `<script>`** (engine v2) —
  keyboard/swipe/direction handling is automatic. Component code goes AFTER the
  engine, inside the same `<script>`. The engine provides builds (`data-build`,
  components.md §25), the `data-capture` guard for drag/arrow widgets, and the
  `slideenter` / `build` events components can listen to.
- The **bridge tokens** that components §22–§32 read are already in the
  template for both canvases (`style-system.md §7`) — nothing to paste.

### 7 — Build the slides
Replace the example slides between the `BEGIN/END SLIDES` markers with your
planned slides, assembled from `components.md`. While building:

- **Visual-first:** put an illustration on every slide that earns one. A slide
  that is only text is a missed opportunity — reach for a window mockup, a
  cards grid, a tier comparison, a flow, a linked-cards timeline, a chart, or at
  least an icon motif.
- **Text in HTML, shapes in SVG.** Never place Arabic (or any) text inside
  `<svg>` — shaping/direction breaks. Build text-bearing visuals (mockups, chat,
  cards) with HTML/CSS; use SVG only for icons and abstract shapes. Figure
  labels are HTML pinned in the figure's viewBox units (components.md §22) —
  a label is not an actor (Law 3).
- **Animate entrances.** Wrap revealed elements in `class="reveal"` and stagger
  with inline `style="--d:.2s"` (grow the delay ~0.06–0.08s per element).
- **Keep the first slide `class="slide active"`** and no other.
- **Logical properties only** for any custom inline CSS (`margin-inline`,
  `inset-inline-start`, `padding-inline-start`…) so the layout mirrors correctly
  in both directions. Avoid hard `left/right` in inline styles.
- **One idea per slide; let it breathe.** If a slide feels crowded, split it.

### 8 — Validate, then present
- Run `python scripts/validate.py <your-file>.html` and fix anything it flags
  (slide count, a stray duplicated `style=`, an over-budget length, etc.).
- **Repo mode:** save the deck into `lessons/` (`NN-<step-slug>.html`), write
  back any changed `docs/` files, and commit if the repo uses git.
  **Chat mode:** save the final file to the outputs directory and present it.
- Keep the closing chat message short: what was made, how to navigate, and an
  offer to adjust canvas/board/length/slides. Don't over-explain. On a rulebook
  route the closing message is that rulebook's report, with its "Departures"
  and "Proposed for the skill" lines.

---

## Teaching principles (how teaching decks teach)
These apply to every teaching deck, on any subject, at any level. They exist
because attempting before instruction, closing loops visibly, and anchoring
ideas in mechanism are what turn a deck from *information shown* into
*capability gained*.

- **Attempt before instruction.** People learn most from the gap between what
  they expected and what turned out to be true. A challenge attempted, then
  taught, then solved teaches more than the same content merely presented —
  which is why the teaching arc opens with a committed guess and returns to it.
  Committing to an answer is what arms the gap; a challenge merely *shown* does
  nothing.
- **The click trio.** Every load-bearing concept earns all three, or it has
  not landed:
  1. **Structure** — a visual/structural diagram (flow, cards, mockup, tiers).
  2. **Mechanism** — the *why underneath*. Not what it does; why it works.
  3. **Application** — a real scenario where the concept visibly matters.
  Two out of three is a definition, not understanding. Interleave rather than
  stack: the diagram anchors, the mechanism explains the diagram, the
  application proves the mechanism.
- **Close every loop inside the deck.** The revisited challenge is
  non-negotiable, and every teaching deck must deliver at least one complete,
  demonstrated capability in a single sitting. A deck that ends on "more next
  time" with no closed win is a failure of this section — split the content
  across decks rather than defer the payoff.
- **Feedback is data, never judgment.** When the reader gets something wrong
  (in the question set, or in a mid-deck check): immediately explain what
  broke at the mechanism level, then give a chance to re-apply. No scolding
  tone, no consolation padding, no "unfortunately" — state the miss, state the
  why, move forward.
- **Make progress visible.** The reader should never have to infer that they
  are progressing. Roadmap slides mark completed steps, recaps name new
  capabilities, and when a previously missed concept is answered correctly in
  a later lesson, the deck says so explicitly (see the adaptive loop). Silent
  progress wastes the strongest motivator a lesson series has.

## Question set & the adaptive loop (teaching decks)
Every teaching deck ends with a short question set and a copyable answer box.
This — together with NOTES.md — is the series' memory: it is how the next
lesson knows what to build on.

**In this deck:**
- A short set of **MCQs + 1–2 open questions** covering the deck's
  load-bearing concepts.
- Include **1–2 stretch questions**, tagged `[stretch]` — transfer questions
  one step beyond what was directly taught, designed so a miss is informative
  rather than discouraging. Getting them wrong is an expected, useful outcome.
- The final page carries a **single copyable text box** containing everything
  in question-then-answer form (with the `[stretch]` tags, and any pending
  `PROPOSAL:` line), formatted to be pasted back into the chat. The box is an
  editable `<textarea>`; the engine ignores navigation keys (arrows, Space,
  Home/End, PageUp/Down) and swipe starts while focus is inside any editable
  field, so typing answers never flips slides — this guard ships inside the
  engine script and `validate.py` fails any deck missing it.

**When the reader pastes the answer block into chat:**
1. **Update the learner notes** (see "The cumulative notes file") — extract
   observations and evidence-tag them. Repo mode: write `docs/NOTES.md` now,
   even when no lesson is being built yet. Chat mode: fold them into the
   `LEARNER-NOTES` comment of the next lesson you build; if the paste comes
   without a request for one, say that the next lesson will carry it (the user
   pastes the answers with the previous lesson attached).
2. **Answer the reader's answers**: for each miss, give the mechanism-level
   explanation immediately in chat (data, never judgment).

**In the next deck of a series (built from NOTES.md, not raw answers):**
- **Re-test earlier misses early**, in new clothing — same concept, different
  surface — so the gap gets a second pass while it is still fresh. A gap stays
  *active* in the notes until a later deck's own questions re-test it
  successfully; only then is it marked closed.
- **Name the update when it lands.** When a concept missed last lesson is now
  answered correctly, say so on the slide ("missed last lesson — solved now").
  The visible before/after is the point; silent correction wastes it.
- **Personalize the content, not the path.** Tune examples, analogies, depth,
  and emphasis to what the notes show — strengths to build on, recurring
  confusions to approach from a new angle, interests surfaced in open answers.
- **Calibrate from the pattern, not a curve.** Use the `[stretch]` tags to
  distinguish a designed miss from a genuine gap: repeated misses on core
  questions mean re-teach; a missed stretch question means the next lesson has
  its opening challenge ready-made.
- **Answers never restructure the roadmap on Claude's judgment — hard rule.**
  A single answer, however strong or weak, is a single data point. Never skip
  or compress a step on inferred mastery: revisiting familiar material is
  cheap at the reader's own pace, and each topic's real gaps are measured by
  *that topic's own deck questions*, not inferred from another deck's answers.
  The only path from answers to the roadmap is a **proposal**: when the notes
  show the same foundational gap across **two or more lessons** (or a core
  miss that survived its re-test), ask explicitly — "Your answers suggest X
  is shaky. Want me to add a short preparation deck to the roadmap at the
  right point?" — in chat or as a `PROPOSAL:` line in the answer box, and act
  only on an explicit yes. Even then, prefer folding a remedial segment into
  an existing lesson over changing the path when it would do the job.

## The cumulative notes file (NOTES.md)
Roadmap mode maintains a third artifact beside the roadmap deck and the
lessons: **NOTES.md**, Claude-written, cumulative, and read **before building
any lesson**. In repo mode it lives at `docs/NOTES.md` and is read and written
directly; in a chat-mode series the same content lives in each lesson's
`LEARNER-NOTES` comment and travels with the deck.

Structure — keep it small and current:
- **Header** — subject, roadmap version it refers to, last-updated date.
- **Live picture** (the part future builds actually use): active gaps (each
  with the question(s) that produced it and the lesson that will re-test it),
  strengths to build on, observed preferences (what kinds of explanation
  landed, from the open answers), and pending flags being watched.
- **Per-lesson log** — date, step, what the answers showed, in a few lines.
- **Closed gaps** — moved out of the live picture with the date and the
  question that closed them.

Every observation is **evidence-tagged**: which question(s) produced it, and
whether it is a single data point or a repeated pattern. Single data points
personalize tone and examples at most; only repeated patterns may justify a
proposal. Prune ruthlessly — a stale note misdirects personalization as badly
as no note at all.
## Content principles (the calm voice)
- **Calm, not techy, not naive.** Warm, plain, confident prose. Short sentences.
  No hype, no jargon walls, no childish over-simplification.
- **Assume zero prior knowledge** unless told otherwise. Define before you use.
  Offer a one-line plain-language gloss for any new term, often in an `.aside`.
- **Lead with the "what" and "why" before the "how".** Never drop a deep idea
  without a gentle ramp.
- **One promise per deck.** The cover promises something; the closing pays it off.
- **Respect the reader's time.** Fit the budget. Brevity is part of the calm.

## Design principles (the calm look)
`references/style-system.md` is authoritative (canvas, boards, type, motion
law, depth mechanics, skin vocabulary); `design-system.md` holds the
practical setup. The five global laws — depth never reflows the scene ·
skeleton ≠ skin · one coordinate system per figure · one motion law ·
little text, louder message — apply to EVERY deck. The essentials:
- Paper, not white; board, not black. Ink, not black; chalk, not white.
  One dominant pen + quiet supports.
- Hand-made depth: wobbly frames, tape, sticky notes, long soft shadows. No
  neon, no glow, no glass, no purple-on-white "AI slop".
- Hand-lettered display type (Caveat / Playpen Sans Arabic 800) over a clean
  body face (Karla / IBM Plex Sans Arabic).
- Generous whitespace; every slide must fit the viewport (the engine adds
  internal scroll as a fallback, but design so scrolling isn't needed).

## Hard rules (avoid these failure modes)
These are the contracts and the user's choices; everything else is a default
("How to read this skill").
- Do **not** let hidden depth reflow the scene: hover/tap content must use one
  of the four legal mechanics (reserved flow · fixed tray · overlay ·
  final-geometry) from `style-system.md`. If an expansion changes an
  element's width, it MUST use final-geometry (pre-measured `--dh`).
- Do **not** reuse an exemplar's illustration subject or content (its
  chessboard, chalk trace, footpath, review cards, captions). Skeletons — a
  stepper, a spotlight, a token route, a lamp budget — are generic and
  reusable; every skin is invented for the topic via the scene-brief procedure.
- Do **not** float HTML actors over an SVG scene — a figure's actors live
  inside its viewBox, one coordinate system (Law 3).
- Do **not** let a draw-in stroke be visible before its animation: gate with
  opacity, not dash math alone.
- Do **not** mix motion laws; Sketchbook's draw-in easing governs everything
  in the deck, ported components included.
- Do **not** build any deck without the canvas-gate answer (1b) — and on the
  chalkboard, the board.
- Do **not** hand-edit a board's colours inside a deck, or rebuild a retired
  family's look (Playroom, Nocturne, Terra, Classic palettes, fonts, glow,
  springs). Borrow their mechanics from `components.md §32` instead.
- Do **not** put Arabic/RTL text inside SVG.
- Do **not** edit the deck-engine part of the `<script>` (navigation, builds,
  reveal, swipe); add component code after it.
- Do **not** ship a drag or arrow-key widget without `data-capture` on it —
  without it the engine turns the page mid-drag.
- Do **not** put `data-build` and `.reveal` on the same element.
- Do **not** treat a component's first-ranked use case as an obligation, or
  build every slide from its "rank 1" component — rankings are suggestions.
- Do **not** leave more than one slide with `active`, or a duplicated `style=`
  attribute on any element (the validator catches both).
- Do **not** exceed the reading-time budget by padding slides (the rulebook
  routes size decks their own way).
- Do **not** use `localStorage`/`sessionStorage` — keep all state in memory.
- Do **not** build a teaching deck without the opening-challenge /
  challenge-revisited pair and the question set; do **not** bolt them onto a
  presentation deck (pitch, intro, showcase) where they don't belong.
- Do **not** swap the revisited challenge for a different problem — it must be
  the same one the reader committed to at the start.
- Do **not** change the roadmap based on answers without an explicit,
  affirmative reply to a proposal — and never skip or compress a step on
  inferred mastery. Research-driven freshness updates are the only
  Claude-applied roadmap changes.
- Do **not** build a roadmap-mode lesson without reading the learner notes
  first (repo: `docs/NOTES.md`; chat: the previous lesson's `LEARNER-NOTES`).
- Do **not** ask the user to attach, save or re-send Markdown files (notes,
  rulebooks, tool archives): they ship with the skill, and memory travels in
  the decks.
- Do **not** build any deck, roadmap, or scaffold for a new journey before the
  topic conversation ends in an explicit confirmation.
- Do **not** touch, overwrite, or reorganize repo files that are not the
  skill's own (`docs/TOPIC.md`, `docs/ROADMAP.md`, `docs/NOTES.md`,
  `lessons/`, `answers/`).

## Quick example — turning a request into a plan
**Request:** "Make me Arabic slides explaining how vaccines work, for someone
with no science background, about 15 minutes, calm and reassuring."

**Plan:** Teaching deck; Sketchbook · paper (gentle daytime reading); Arabic RTL; ~14 slides → Cover ·
opening challenge ("a new virus appears — which trains your body better:
catching it once, or a rehearsal without the danger? Commit to an answer") ·
"what is a vaccine, in one breath" · the body's defenders (plain analogy) · the
map of what's coming · how a vaccine rehearses the immune system (diagram +
mechanism + a real outbreak scenario) · types in brief (tiers) · what happens
after the shot (timeline/linked-cards) · safety & testing · challenge
revisited (answer it now, with the mechanism) · recap as capabilities ·
question set + answer box (one `[stretch]`: "why do some vaccines need a
second dose?") · closing. A visual on every slide; reassuring plain voice;
define every term on first use.
