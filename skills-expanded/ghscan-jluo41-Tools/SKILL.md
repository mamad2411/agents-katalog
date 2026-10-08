---
name: haipipe-paper-ideation
description: >-
  The reader-facing Paper Page Type for one research
  direction and the research questions raised under it: every Idea is written
  as the question it asks, and that question is the Idea's name. It projects
  haipipe-ideation I1/I2 sync packets and the final I3 selection handoff into
  Direction, Discovery Landscape, Opportunity Map, question comparisons,
  evidence gaps, and Story routes without becoming a second semantic or
  selection authority. Use to
  create, refresh, read, or check a Paper Ideation Page; route idea generation,
  novelty testing, pressure testing, and selection to haipipe-ideation.
metadata:
  version: "1.1.2"
  last_updated: "2026-09-29"
  group-token: "Story00"
  outline:
    mode: grammar
    source: "this SKILL.md"
    shape: "the Page Face is Opening → Outline → Content → Aims; Content division 1 is Direction, division 2 is Discovery Landscape, division 3 is Opportunity Map, and division 4 is Ideas (ranked); for a dynamic set of K admitted ideas, divisions 5 through K+4 are Idea 1 through Idea K, each headed `Idea <n>: <research question>` and carrying Research Question · Origin / Opportunity · Hypothesis · Method · Minimum Experiment · Expected Outcomes · Discovery Basis · Core Claims / Novelty Check · Counterevidence · Pilot Result · Journal / Venue Fit · Risk · Reviewer's Likely Objection · Recommendation · Next Evidence Action; division K+5 is Eliminated / Merged / Deferred Ideas, K+6 is Next Evidence Queue, and K+7 is Suggested Execution Order and G0 Readiness"
---

# /haipipe-paper-ideation · one evergreen Paper view of an evidence-tested direction

For a concrete Page update load `haipipe-page`, `haipipe-page-workflow`, the
current Run Workflow/Spec owner, `haipipe-paper-workflow`, then this PageType.
For semantic idea generation/testing/selection, enter `haipipe-ideation`; this
adapter only loads Page work when its projection or Page content is involved.
Declare `page-type: ideation`. Load `haipipe-ideation` and its
`references/manifest-and-sync.md` for an I1/I2 sync; also read
`references/receipts.md` for a final I3 handoff. The schemas stay with their
semantic owner and are not copied into this skill.

For version-3 Ideation decisions, workflow/selection.yaml is the current view
of the immutable snapshot named by the handoff. Project each candidates[] row:
only explicit select/defer/abandon answers change a verdict; open stays open.
Use that row's posture, risks and exact target/category/contract version. The
top-level decision and route lists are compatibility projections, not a global
winner or a disposition for every row. Reject mismatched selection/sync
versions before opening Story routes; preserve prior snapshots and handoffs.
Follow Ideation's receipts.md mapping; Page creates no second decision.


## Paper ownership and entry

This skill owns the Paper Ideation Page and its
`page-type: ideation` reader contract below. The repo is minted WITH this Page,
so there is no entry gate and the Page may exist while every candidate is still
unverified. `haipipe-ideation` is the sole semantic owner of Direction and Idea
Cards, the I1 Generate and I2 Test state, the machine portfolio recommendation,
and the I3 human selection receipt. This Page projects those records from I1
onward; it does not regenerate them or make a second decision.

Exit through gate G0 for each selected idea only after the final handoff points
to the sole `workflow/selection.yaml`: per-claim novelty is bounded, a Task-owned
pilot or explicit waiver exists, deep venue fit uses a current Venue contract,
and the person selected the Idea plus intended target/category. The Page may
then display verdict, target, and `went to` exactly as that receipt records
them. `haipipe-paper-workflow` tests G0 from the same receipt and reciprocal
Story links; it never asks for another selection tick. The Page itself always
runs through `/haipipe-page` and `haipipe-page-workflow`
(CONTEXT → OUTLINE → EVIDENCE → CONTENT → CHECK), never a private lifecycle.

## 🔌 Semantic adapter and single authority

One evergreen `Story00-ideation` Page receives two adapter states owned by
`haipipe-ideation`:

```text
I1 GENERATE ─┐
             ├─ projection/paper-ideation-sync.yaml ─▶ same Paper Ideation Page
I2 TEST ─────┘                                  revisions 1, 2, 3, ...

I3 SELECT ── workflow/selection.yaml ── handoff/paper-ideation.yaml
                                             │
                                             └─▶ verdict · target · went to
```

- `kind: paper-ideation-sync` is the working-state adapter. It carries the
  Direction, Discovery Landscape, Opportunity Map, every admitted card and
  test state, the canonical machine-only `portfolio_recommendation`, and open
  gaps. Its `selection_authority.status` remains `none`; it cannot authorize a
  Story.
- `kind: paper-ideation-handoff` is the selected-state adapter. It points to
  the latest sync plus the sole I3 selection receipt and selected Idea-target
  routes. It does not create a second portfolio or decision.
- Material Generate or Test changes increment `sync_revision` (the only source
  identity; no content hash), classify the change as `state`, `portfolio`, or `structure`,
  and route the packet through the current `haipipe-page` update boundary. A
  `state` change refreshes the generated working projection. A `portfolio`
  change refreshes it by stable `idea_id` and checks whether the authored shell
  is affected. A `structure` change stops at the Page OUTLINE/SHAPE workflow
  when a shape decision is needed. The Page workflow receipt records the
  packet path, consumed revision, projection surface, and timestamp; a
  mismatched working revision is stale, not current. The Paper-specific
  `paper_projection` extension lives inside the normal Page controller receipt. The
  adapter reads that Page-owned receipt and remains the only writer of the sync
  packet's nested `paper_page` status.
- When `paper_page.state: missing`, use `/haipipe-page` to mint or bind the one
  canonical Ideation Page and leave all three surfaces `not-requested` until a
  projection is actually recorded. When it is `blocked`, preserve the
  canonical path and each last honest surface revision/receipt, report the
  named gap, and do not mint a surrogate Page, a second projection receipt, or
  a local Ideation Run.
- A formal Page-level CONTENT pass may adopt the working projection only after
  all planned Page Runs and required evidence Results are ready. It then builds
  the declared delivery once before CHECK. A sync, working receipt, Page
  approval, or CHECK acceptance never bypasses that release barrier. The
  `release` and `delivery` surfaces each require their own matching receipt.
- Raw Result Cards, facts, BibTeX, Task output, Venue rules, and Discovery notes
  remain with their owners. The adapter and Page carry interpretations and
  pointers only.

### 🧱 Ideation source and Page surfaces

Keep the semantic source and three Page surfaces visible whenever the Ideation portfolio changes:

```text
Ideation source       cards + sync packet                 sync revision
working Ideation view       Outline/preview/Bullet Workspace    working receipt
released Ideation view      adopted Content                     release receipt
delivery              generated output                    delivery receipt
```

The semantic sync is not an interactive Page Run and does not mint a writing Run.
Only a person's bounded feedback or acceptance request uses the Page Run/Step
contract. When the Ideation working view is current but the released view still
points to the prior revision, report that split explicitly; never label the
older Markdown or delivery as the latest Ideation Page. Portfolio reordering never
silently renumbers Page-global paragraph identities; the stable key is
`idea_id`, not list position.

## 🌱 Grain and home

One Ideation Page holds ONE research direction and a dynamic number of
candidate ideas raised under it. It is the story group's PAGE ZERO (0.4.0) —
no separate group; it sits in the same group as the Stories its selected ideas
become, before them:

```text
Paper-<Slug>/
└── A1-Story/                          the story group, at the paper root (0.8.0)
    ├── Story00-ideation/              THIS PAGE · one direction, its ideas, ranked
    └── StoryA-misq-phytrait-discretion/                       what the first selected idea became:
        ├── StoryA-misq-phytrait-discretion.md                 one idea · one prospective paper blueprint
        └── draft/                     its Page workflow records
    (a second surviving idea is StoryB-<desk>-<idea-slug>/ · the letter identifies the Story)
```

**The repo precedes the Story** (0.2.0): minting a paper's Ideation Page is
what creates `Paper-<Slug>/` — as a git submodule immediately, per the
scaffold rule — with only `board.md` and `A1-Story/Story00-ideation/` inside.
The direction's name may seed the repo slug; a direction that dies leaves the
repo standing as its own record. **A board holds exactly ONE ideation page**
(the journey fixes the story group's roles, one each): a direction that
genuinely forks is a new direction, so it mints its own `Paper-<Slug>/` with
its own `Story00-ideation`, and the two pages cross-reference through the
originating row's `went to`. Two ideas from the SAME direction that both
survive are `StoryA-<desk>-<idea-slug>` and `StoryB-<desk>-<idea-slug>` in this board (0.9.0, JL 260907: the Story
letter identifies the selected Story); the `went to` cell names the Story page
by id. Before 0.5.0 a fork could take "the next free SD number"; that reading
died when the journey fixed the roles, and 0.8.0 gives the number back its
counting job at the idea level.

Historical `SD00-ideation` / `SD01-seed` instances remain readable and are not
renamed or moved merely to satisfy this contract. When such a Page is next
revised, record its canonical `Story00-ideation` / `Story<Letter>-<desk>-<idea-slug>` role and
preserve two-way links. A filesystem rename is a separate, explicitly scoped
migration, never an implicit Page or G0 action.

The page is EVERGREEN (♻️): it never closes while the direction is alive.
Raising an idea is cheap: ideas are generated in batches, compared, optionally
ordered, and eliminated without ceremony. There is no fixed count and no
required global winner. The count is the number of distinct research
questions worth a reader's attention under this direction, and nothing else:
a batch of titled directions is not a portfolio, and eight titles are not
eight Ideas (JL 260922: "I don't need 8 ideas, I want to write the idea in
terms of the research question"). Two cards that ask the same question merge;
a card that has no question is not yet an Idea. `Ideas (ranked)` records the current comparison/attention order; it is
not a best-to-worst truth and never substitutes for a human verdict.
What is never cheap is the row: an eliminated idea's row stays forever,
because the record is what stops the same idea being re-thought in new words
six months later.

## ❓ An Idea is a research question

An Idea on this Page IS the research question it asks. The question is the
Idea's name: it heads the Idea's division, fills the `idea` cell of the
Ideas (ranked) table, and leads the Paper Workbench's Idea Card. A title such
as "Selection and ordering audit" is a topic label; a line such as "Freeze a
real physician denominator" is a method; "LLMs prefer well-reviewed
physicians" is a claim. None of them is an Idea. They are field values under
the question, and a card that offers only them is `unframed`.

```text
the question   Does <object> <relation> <outcome>, for <whom / where>, beyond <what is known>?
               one sentence · ends in ? · bounded · answerable · a null answer still informs
the handle     2–5 words derived FROM the question, for slugs and the went-to Story name
               (the Idea Card's `title`); it never stands in for the question
the chain      Direction question → Idea questions (this Page) → the selected
               Story's Primary Research Question (Story C3) → its claims (Story C5)
```

A research question is admissible when it names one object, one relation or
contrast, and one outcome; states the boundary (population, setting, period,
or comparator) inside which it is asked; has an answer form the paper could
produce; stays informative when the answer is no or null; and carries a
tension a reader would want resolved. `haipipe-ideation` sharpens a fuzzy
interest into that shape through its vendored `framing-research-questions`
reference and records the result in the Idea Card's `question`; this Page
projects it and never rewrites it. When a card reaches this Page with a
title and a claim but no question, the Page projects the card in the
disposition division as `unframed · needs a research question` and does not
mint an Idea division for it; the Ideas (ranked) row stays, with the `idea`
cell reading `⬜ unframed`, so the gap is visible instead of dressed as an Idea.

At I3, the selected Idea's question becomes the Story's Primary Research
Question verbatim. Supporting research questions on the Story are refinements
of it, never replacements; if the Story needs a different primary question,
that is a new Idea, raised here first.

## 🪟 Page face

The reader-facing Page keeps the base four-part shell. `Outline` and `Content`
are the two primary working surfaces, but `Opening` is required and `Aims`
remains a brief completion contract:

```text
## Opening   the direction question and why this decision needs a visible record
## Outline   the compact C/P/B · Feedback · Evidence · Supporting/Local Run projection
## Content   the discovery landscape, opportunity map, candidate Ideas, tests,
             evidence queue, and routing below
## Aims      short direction-level and Page-level done-when statements
```

The Paper Workbench (`haipipe-workbench-paper`, Ideation Space) reads this
contract: its Idea Card leads with the Research Question, drops the handle to
the subline, and folds the outline's writing Bullets away; a card without a
question leads with its title (the screen adds no hint, JL 260927).

Do not promote Data, Preliminary Results, Novelty Check, Feedback, Display,
States, Files, Log, or Discussion into additional top-level Page sections.
Data and preliminary results live in each Idea's Method/Minimum Experiment and
Pilot Result; Novelty Check lives under Core Claims; Journal / Venue Fit lives
inside each Idea division. Discovery Landscape and Opportunity Map are Content
divisions, not new top-level sections. Feedback/Display/Page receipts remain in
their owning Page workflow records.

Page review and Ideation selection are separate human decisions. The Page
workflow's `approved:` accepts the C/P/B Shape and its `accepted:` CHECK ruling
accepts one readable Page version. Neither selects an Idea. Only the I3
`workflow/selection.yaml` receipt can record `PROCEED`, risk-accepted `PROCEED
WITH CAUTION`, defer, or abandon and authorize a target plus `went to` Story
edge. G0 consumes that receipt and does not close this evergreen Page. Never
infer selection from Page approval, Page CHECK, comparison order, or a machine
recommendation.

## 📐 Content outline · discovery to decision

The Page makes the reasoning chain readable before it presents candidate
details: what the field establishes, what remains open, which Ideas those
openings produced, what evidence changed them, and what should happen next.
Let `K >= 1` be the number of admitted Idea Cards, including cards later
eliminated whose divisions remain as history. The number is dynamic:

```text
### 1 · Direction                         🔒 bounded question · why now · admission rule
### 2 · Discovery Landscape               🔎 direct evidence · analogues · convergence ·
                                             contradiction · unresolved territory
### 3 · Opportunity Map                   🧭 evidence-bounded openings and the Idea ids
                                             each opens, narrows, exhausts, or contradicts
### 4 · Ideas (ranked)                    🔥 one row per admitted Idea · current I1/I2/I3 state
### 5 … K+4 · Idea <n>: <research question>   one division per admitted Idea, headed by
                                             the question it asks, in current comparison
                                             order, using the fields below
### K+5 · Eliminated / Merged / Deferred  ♻️ permanent disposition history and reason
### K+6 · Next Evidence Queue             📮 Discovery · Task · Venue owner route per gap
### K+7 · Suggested Execution Order       ♻️ machine attention order · G0 readiness · selected
            and G0 Readiness                  Story routes only when I3 supplies them
```

The Discovery Landscape and Opportunity Map are decision-facing syntheses,
not a copied literature review. Landscape statements resolve to accepted
Discovery synthesis Pages or direct bundle evidence ids and retain direct
versus analogue status. Opportunity rows preserve the sync packet's id,
interpretation, evidence ids, affected Idea ids, and
`open | narrowed | exhausted | contradicted` status. Missing full-text depth,
counterevidence, and unresolved territory remain visible rather than being
smoothed into a novelty claim.

A retrofit Page whose single Idea already became the paper may retain its
historical nesting. On its next material revision, bind the available sync or
handoff and add only fields the source artifacts support; do not invent an I1,
I2, or I3 history.

Admission is the stable boundary. An idea becomes admitted when the semantic
layer assigns it a zero-padded `iNN` card (`i01`, `i02`, ...) whose `question`
states the research question it asks; from then on it keeps one division,
headed by that question, forever. A card with an `iNN` but no question is
`unframed`: its row and its disposition entry exist, its division does not,
until the semantic owner writes the question.
A duplicate phrase, overbroad claim, or framing rejected before `iNN`
assignment may appear only in the disposition division with its source and reason and
does not owe a fabricated Idea division. The Page must state which kind each
eliminated row is.

## 🔎 Discovery Landscape and Opportunity Map

Division 2 answers what the field currently establishes; division 3 answers
what that evidence leaves worth pursuing. Keep the distinction visible:

```text
Discovery Landscape                         Opportunity Map
accepted evidence and its limits            Ideation's bounded interpretation
direct physician work vs analogues          one durable opportunity id
convergent signals and contradictions       evidence ids + affected Idea ids
unresolved territory and reading depth      open · narrowed · exhausted · contradicted
```

The Landscape projects `discovery_landscape` from the current sync. It may
summarize an accepted Discovery synthesis Page and direct evidence ids, but it
cannot turn an unverified source, search hit, or copied Bib entry into support.
The Opportunity Map projects `opportunity_map` without adding new openings by
Page-author intuition. When new evidence narrows or contradicts an opportunity,
the affected Idea rows and divisions change on the same sync revision.

## 📊 Ideas (ranked) · division 4

The summary table, one row per admitted Idea, every cell a state and never a
blank:

```text
id  idea (the research question)                                     novelty      pilot      venue fit      verdict     target       went to
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
i01 Does a physician's agreeableness, read from patient reviews,     partial      ✅ Result   strong · vfit  ✅ PROCEED  JAMA · Art.  StoryA-<desk>-<idea-slug>
    predict prescribing beyond the star rating?
i02 How many fabricated physician names does an NPI registry check   ⬜ unchecked —          ⬜ pending     ⬜ open     —            —
    remove, and how many real ones does it lose?
i03 ⬜ unframed · card has a title and a claim, no question           ⬜ unchecked —          ⬜ pending     ⬜ open     —            —
```

The `idea` cell is the card's research question, one sentence ending in `?`,
never the handle. An `unframed` row says so in that cell and owes no division.

Verdict vocabulary is projected from the I3 receipt: `⬜ open`, `✅ PROCEED`,
`⚠️ PROCEED WITH CAUTION` with named accepted risk, `❄️ DEFER`, and
`🚫 ABANDON`. Before I3 every row remains open regardless of the machine
recommendation. An abandoned, merged, or deferred Idea is also recorded in the
disposition table with its reason; its summary row and admitted Idea division
stay as history. A `—` cell
is legal only where the authoritative state makes the column moot; on a live
row every cell is a state or a bound path.

For current work, the source block names the exact
`projection/paper-ideation-sync.yaml`, `sync_revision`, Ideation task address,
Direction Card, and evidence bundle. A final selected view also names
`handoff/paper-ideation.yaml` and its `workflow/selection.yaml`. Legacy
IDEA_REPORT or `ideas.md` inputs remain readable, but a new Page does not bypass
the adapter and let ideas appear from nowhere.

The row order supports comparison and attention only. The first row is not
automatically selected, and the page may end with no selected idea, one
selected idea, or several selected ideas. The I3 human receipt and `went to`,
not position, record selection; several selected rows route to distinct Stories.
For every admitted row, `venue fit` is a state backed by its Idea × Venue Fit
Card. A selected row also names the person's target and article/category;
machine recommendations stay inside the idea division.

## 📮 Next Evidence Queue and execution order

Division K+6 groups every unresolved item by its native next owner: Discovery
for external evidence, Task for a pilot or internal fact, Venue for a current
desk contract, or Ideation for Generate/Test/Select work. Each row names the
sync gap or Idea `next_route`, the exact card or opportunity it affects, and
the Result/receipt condition that would close it. It creates no Paper-local
execution Run.

Division K+7 projects `portfolio_recommendation` as the suggested attention
order and labels it machine-authored. Before I3, G0 readiness is only a gate
reading and every verdict/target/Story cell remains open. After I3, the Page
adds only the selected routes found in the final handoff and leaves deferred or
abandoned history visible.

## 🧾 Each Idea's division · one card under evidence

One division per admitted card, headed `Idea <n>: <research question>`, the
question verbatim from the card. It projects the card, Test Matrix, fit card,
and owner receipts without rewriting their conclusions. Every field below is
written relative to the question, so a reader who stops after the first line
still leaves with something to think about:

```text
Research Question             the question this Idea asks, verbatim from the card ·
                              first field, same words as the heading · ends in ?
Origin / Opportunity          which Opportunity Map row raised or changed the question
Hypothesis                    the anticipated answer, one sentence
Method                        how we would answer it, 2-4 concrete steps, plain language
Minimum Experiment            the smallest run that would move the answer
Expected Outcomes             what a yes, a no, a null, and a failed run each mean for the answer
Discovery Basis               direct work, analogues, convergence, contradiction, and open gap
Core Claims / Novelty Check   what an answer would let the paper claim: one line per claim
                              plus its exact search question,
                              closest verified work, remaining delta, limitation,
                              and novel/partial/preempted/inconclusive/unverified status
                              📮 → /haipipe-novelty-check + Discovery Run/Result
Counterevidence               the strongest evidence-bound alternative or rejection
Pilot Result                  POSITIVE/NEGATIVE/WAIVED/PENDING/HOLD + the receipt
                              📮 → task-layer Run/Result, or an explicit waiver
Journal / Venue Fit           broad screen for every admitted idea; deep fit
                              for live finalists; candidate targets, article
                              type, desk risks, missing evidence, reroute,
                              current Venue contract, and machine recommendation
                              📮 → /haipipe-journal-fit
Risk                          what could sink it
Reviewer's Likely Objection   the strongest counterargument
Recommendation               the sync packet's canonical machine-only recommendation
Next Evidence Action         exact Discovery, Task, Venue, select, defer, or abandon route
```

A retrofit page fills only the fields its receipts support and marks the rest
`⬜`; inventing history is worse than a visible blank.

For retrofit novelty, split a flat Core Claims block only where the inherited
text already states distinct claims. Reuse an archived Result only when its exact
question tests the matching claim; otherwise print `unverified` and route a
new Discovery check. Do not convert one old blob-level novelty verdict into
several claim-level passes.

## 🔬 Core Claims, checked one by one

An idea is never novelty-checked as a blob. Its division states 1-5 Core
Claims that would need to be novel; each claim is checked separately and the
table's novelty cell records the Test Matrix reading supported by the worst
claim:

```text
claim → multi-source search (≥3 query shapes · recent-years window)
      → closest prior work + the delta, per claim
      → every cited prior work verified by id/DOI before it enters the page
```

The visible claim table preserves the semantic executor's fields:

```text
claim · search question · closest verified work · remaining delta · limitation · status · Result path
```

"Applying X to Y" is not novel unless the application would reveal a
surprising finding; when the method is not novel but the finding would be, the
division says so explicitly. A prior-work citation that cannot be resolved is
written `[UNVERIFIED]`, never silently trusted. (Discipline adopted from the
ARIS `novelty-check` reference and from this workspace's own
fabricated-citation incidents.)

## 🃏 The page records; it never executes

The Ideation Page is a consumer. Searching, reading, and piloting are
Task/Discovery-layer work, and their receipts are Run/Result records this page binds by
path:

```text
Direction                  ← Direction Card through paper-ideation-sync
Discovery Landscape        ← accepted Discovery syntheses + evidence ids in sync
Opportunity Map            ← Ideation interpretations + affected Idea ids in sync
Research Question (name)   ← Idea Card `question` through sync · never authored here
Ideas + test states         ← Idea Cards + Test Matrix through sync
Core Claims lines          ← /haipipe-novelty-check + Discovery Run/Result
Pilot Result               ← /haipipe-idea-pressure-test + Task Run/Result or waiver
Journal / Venue Fit        ← /haipipe-journal-fit + Fit Card + Venue contract
Verdict · target · went to ← final handoff + sole I3 selection receipt
```

The standing semantic executor is `/haipipe-ideation`: I1 Generate authors
cards, I2 Test reconciles novelty, pressure, feasibility, and venue fit, and I3
Select owns the human receipt.
External prior-work retrieval routes through `/haipipe-discovery-search`, and
feasibility routes through the Task owner. The historical ARIS `idea-creator`
and `novelty-check` skills (Tools/references/aris) remain methodology
references: their output enters this page only after it has become an ideation
card or a discovery-/task-layer Run/Result, never by direct write.

The executor's `novel | partial | preempted | inconclusive | unverified`
vocabulary is projected without inventing a second HIGH/MEDIUM/LOW scale. Each
claim is commissioned as its own bounded Discovery question and retains its
owner-native Result lineage; the Page summarizes but does not reinterpret the
specialist receipt.

A pilot is a feasibility Result, not a paper finding: budget it small, time-box it,
and record a failed pilot as honestly as a passed one. A cell asserting a
pilot result with no Task receipt or explicit waiver behind it is a defect.

Existing regressions may be read as a retrospective pilot only through a
Task-owned Run/Result receipt that names the bounded minimum experiment, exact output
paths and execution provenance, acceptance reading, and positive/negative
result. An inherited `SKIPPED` line or manuscript claim does not satisfy G0;
it needs that retrospective receipt, a new pilot, or an explicit human waiver.

## 🎓 Projecting selected Ideas to Stories

An Idea's row may name a Story in `went to` only when the final handoff and its
sole I3 receipt establish all four:

- its Core Claims each carry a novelty reading from an independent context,
- its Pilot result binds a feasibility receipt (or records an explicit,
  reasoned waiver),
- its Venue Fit Card has a retained broad screen, complete deep fit against a
  current Venue contract, and the row names the person's intended
  target/category,
- the receipt records a person's `select` plus `proceed` or
  `proceed-with-caution`, with every accepted risk named. The Page never turns
  its machine Recommendation into the verdict, and eliminated Ideas never
  leave.

It is a two-way act: `went to` copies the exact Story path already allocated in
the receipt, normally `StoryA-<desk>-<idea-slug>`,
`StoryB-<desk>-<idea-slug>`, and so on beside this Page, or the new repo when an
Idea leaves for a different paper. That Story's C5 Source Pages and provenance
bind this Page, the final handoff, and the I3 receipt back. A row naming a Story
that does not bind back, or a Story claiming an origin this Page does not show,
is a defect on whichever side is missing.

Selection is per Idea, not per comparison table. I3 may record none, one, or
several selected candidates; every selected candidate receives one distinct
Story and passes G0 independently. The Page never declares one global best
Idea and never edits the selection receipt.

## ✋ Human authority

A machine may generate Ideas through I1, run I2 searches and pilots through
the proper owners, fill Core Claims, build Venue Fit Cards, and write the one
canonical portfolio recommendation in the sync packet. It may not author the
I3 person's identity, date, verdict, target/category, accepted risks, or Story
authorization. Selection, deferral, abandonment, targeting, and commitment are
human acts recorded once by `haipipe-ideation-select`.

Gate G0 (Ideation → Story; historical Seed wording remains readable) is tested
against each selected Idea's final handoff, its sole I3 selection receipt, and
the reciprocal Story binding. The Page summary row is a projection of those
records, not the place where another selection is minted. Paper Page workflow
receipts record projection and review only; the I3 receipt remains in the
Ideation unit.

G0 is not the Page CHECK gate. A current Page version may be accepted while no
Idea is selected, and a previously selected Story may remain valid while a
later Page version adds, defers, or eliminates other candidates.

If a later I2 revision changes an already-selected Idea, preserve the earlier
I3 receipt and handoff as historical decisions. The new evidence routes that
Idea back to `haipipe-ideation-select` for a fresh human decision; it never
automatically revokes, replaces, or rewrites the old selection.

## ✅ Closing checks

- Division 1 names one direction and what would make an idea worth a paper.
- Division 2 projects a Discovery Landscape from accepted syntheses and direct
  evidence ids without copying their Results.
- Division 3 projects the evidence-bound Opportunity Map and affected Idea ids.
- The Page Face contains Opening, Outline, Content, and Aims; Outline and
  Content are the primary working surfaces.
- Page Shape approval, Page CHECK acceptance, and the sole I3 selection receipt
  remain distinct; Paper creates no second G0 selection receipt.
- The Page names the current `paper-ideation-sync` path and working-projection
  revision; a stale or blocked sync is visible, and adopted Content/delivery
  state is reported separately. Any projection receipt is Page-owned; a
  blocked route creates no surrogate Page, local Ideation Run, or fake receipt.
- Every Idea is written as the research question it asks: the division
  heading, the first field, and the Ideas (ranked) `idea` cell carry the same
  question verbatim from the card, ending in `?`; no handle stands in for it.
- The number of Idea divisions is dynamic and equals the number of admitted
  cards that state a question; every such card has one retained division,
  filled or honestly `⬜`; an `unframed` card has a row and a disposition entry
  only.
- A selected Idea's question is the Story's Primary Research Question
  verbatim, and the Story's C3 binds back to this row.
- Every disposition row states whether it is an admitted `iNN` card or a
  rejected pre-admission framing; only admitted cards owe retained divisions.
- Every row in Ideas (ranked) has no blank cell; every verdict is from the
  fixed vocabulary and comes from I3 or remains open; current work names its
  sync packet, while a legacy source is explicitly labeled legacy.
- Comparison order and the canonical portfolio recommendation are not treated
  as selection; only the I3 receipt and `went to` authorize a Story.
- Every Idea division carries the card/test fields, filled or honestly `⬜`.
- Every Core Claims / Novelty Check line traces to a per-claim Run/Result; every
  cited prior work is verified or marked `[UNVERIFIED]`.
- Every Pilot Result binds a Task Result path or an explicit waiver.
- Every admitted Idea has a broad Venue screen; every selected Idea has a
  complete deep fit, current Venue contract, and human-selected target/category.
- Every non-open human verdict projects the sole receipt's person and date.
- Every `went to` names a distinct Story that binds this page back.
- Historical SD-named instances preserve their paths unless an explicit
  migration is authorized; canonical roles and two-way bindings remain clear.
- The disposition division holds every Idea ever merged, deferred, or dropped,
  each with its reason; nothing raised has vanished.

This variant owns no scripts. The generic Page template and workflow own the
frame, workbenches, receipts, and lifecycle.
