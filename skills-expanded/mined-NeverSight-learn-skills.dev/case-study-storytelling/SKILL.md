---
name: case-study-storytelling
description: Shape product-design case-study storytelling by turning a story draft, webpage, or existing deck into an evidence-led argument, causal narrative arc, and sequential slide-by-slide story map with artifacts and story gaps. After the storyline is explicitly approved, use the same skill for slide-aligned talking points, emotional tension, performance preparation, and evidence-grounded interviewer follow-up questions with structured answer scaffolds. Use before visual design or implementation for a live talk, interview, portfolio review, or self-guided deck.
---

# Case Study Storytelling

Shape the argument before the visuals. Read
[storytelling-principles.md](references/storytelling-principles.md), then follow this
workflow. Read [html-review-output.md](references/html-review-output.md) only when
producing the review file. If `references/local-profile.md` exists, read it as an
installation-specific extension. It may add an audience lens, workflow preference, or
downstream handoff, but it must not weaken the evidence guardrails or replace the core
workflow.

## Mode router

When the skill is explicitly invoked with a mode, route directly to that workflow:

- `/plan` — run or revise story architecture through the approval gate. This is the
  default when no mode is supplied.
- `/script` — add slide-aligned spoken structure and emotional beats to an approved or
  explicitly accepted clear story plan. Read [script-prep.md](references/script-prep.md)
  completely before acting. Produce structure, not a verbatim script, unless explicitly
  requested.
- `/follow-up` — add evidence-grounded interviewer questions and answer architecture to
  an approved or explicitly accepted clear story plan and its completed performance
  script or talking points. Read both inputs, then read
  [interview-follow-up-prep.md](references/interview-follow-up-prep.md) completely before
  acting. If no script or talking-point layer exists, ask the user to run `/script` or
  supply an existing script before preparing follow-ups.
- `/revise` — incorporate the user's comments into the current story-planning artifact
  using the active mode's rules. Preserve unaffected content and do not silently advance
  to another mode.

Treat the slash-prefixed word as a skill-local mode, not as a Codex system command. A
mode selects a workflow; it does not waive its evidence requirements or approval gate.

## Three-stage contract

Use three sequential stages:

1. **Story architecture** is the default and mandatory first pass. Establish the
   argument, evidence, causal arc, lows, turns, ending wisdom, and slide sequence.
2. **Script preparation** is an additive second stage. It creates slide-aligned talking
   points and emotional beats only after the storyline is approved and the slide
   sequence is relatively stable.
3. **Follow-up preparation** is the final stage. It reads the approved story plan and
   the completed script together, then prepares interviewer questions and answer
   structures from both visible and spoken claims.

Never generate a later stage during an earlier one. If the user asks for all stages at
once, complete the story architecture, surface the review decisions, and wait for
approval before starting script preparation. Complete or receive the script before
starting follow-up preparation. Do not let sentence-level delivery work hide an
unresolved causal or evidentiary problem.

## Guardrails

- Use only supplied or explicitly cited sources; never import another case study's context.
- Do not invent evidence, metrics, ownership, collaboration, or outcomes.
- Never invent a stake, conflict, failure, turning point, consequence, or lesson to
  complete an arc. A plausible story is not a truthful story.
- Distinguish what shipped from what remained exploratory.
- Preserve the creator's voice, but make claims concrete only with supplied facts.
- Adapt emphasis to the supplied audience without turning the story into a competency checklist.
- Do not design or implement the eventual deck. The HTML is only a review surface.

## Workflow

### 1. Inspect

- **Story draft:** extract events, decisions, evidence, agency, and outcomes.
- **Webpage:** inspect the whole page and meaningful artifacts; do not mirror scroll
  sections into slides.
- **Existing deck:** inspect slides, notes, appendix, and artifacts; retain source slide
  numbers for revision mapping.
- **Target context:** inspect supplied JD, company material, founder notes, and candidate
  rubric. Separate explicit signals from working hypotheses.

Use the appropriate file-reading capability. Prefer the latest explicit source when
materials conflict. Infer missing audience, format, duration, or count only when safe,
and label the assumption. Explicitly set `audience mode` to `interview`, `portfolio`, or
`self-guided`; this controls whether candidate-fit findings appear in the output.

### 2. Build a private evidence ledger

Record the stable elephant, any deeper active blocker, the tension question, stakes,
role, collaborators, beliefs, decisions, evidence, artifacts, outcomes, metrics,
confidence horizon, highs and lows, five-second turn, earned wisdom, and unresolved
questions. Track learning progress separately from organizational traction. For each
artifact, record its intended message and proof. Do not output the ledger unless useful.

Separate validation of the problem, system, interaction model, and feature priority.
Enthusiasm is not priority; a written claim is not proof.

When target context is supplied, select 2–4 audience signals the case can credibly
prove. Do not force every case to cover every trait. Record the moment, action,
constraint, and outcome that prove each signal. Keep this mapping private unless the
audience mode is `interview`. If target context is absent, skip signal selection; never
render candidate-fit material outside `interview` mode.

### 3. Diagnose the story and audience fit

State the current and recommended arguments in one sentence each. Identify the primary
proof, strongest beat, biggest risk, broken causal links, and the unresolved question
that carries the middle.

Run a story-foundation check before treating the map as complete. Confirm from supplied
facts:

- the highest defensible customer or business stake for the first narrative beat after
  the lightweight cover;
- a causal chain from problem through changed decisions to outcome;
- a real challenge that made success genuinely hard, threatened the outcome, or forced
  a meaningful change; routine friction does not count;
- one specific ending wisdom earned through the project.

If any foundation is absent, still build a useful **provisional plan**. Begin the visible
output—before diagnosis or slides—with `This story is not complete yet` and name what is
missing in plain language. Assign each missing foundation a stable `GAP-##`, place it
where it belongs, and turn it into a targeted review question. Do not write slide claims
that depend on facts the user has not provided. Prefer a real failure or lesson when one
exists, but never force literal failure. If the source shows no challenge that genuinely
affected the project, mark a gap and ask: `What made this project genuinely hard?`

In `interview` mode, integrate the 2–4 audience signals this case can credibly prove into
the same diagnosis. Do not repeat the recommended argument as a separate candidate
thesis. Keep the visible diagnosis to one story contract plus no more than three short
findings; use ratings only when they change an editorial decision, and do not output a
comprehensive scorecard.

### 4. Shape one integrated story map

Build a decision-and-evidence arc, not a process diary. Every slide needs:

- one job and one primary type;
- a conclusion-led title;
- a privately tracked format and live-talk budget;
- minimum on-screen content and one named artifact plus the message it must land;
- at most one audience signal, only when the slide genuinely proves it;
- one talk-track focus and a causal handoff.

Start with a standalone `COVER-00` before `SLIDE-01`. Apply the lightweight-cover rule
from `storytelling-principles.md`: project name, one-sentence premise, minimal
role/context, and one hero artifact; budget 15–30 seconds. Let `SLIDE-01` establish the
highest defensible stake. Do not make the first narrative slide do double duty as the
cover.

Budget content slides at 60–120 seconds and covers, transitions, or payoffs at 20–45
seconds. Split or cut when a slide exceeds two minutes, has two jobs, gives two
artifacts different messages, or makes text compete with the artifact. Choose
`standard`, `hero artifact`, `reveal`, `embedded experience`, or `transition`. Hero
artifacts get only a conclusion-led title and one focal annotation.

Do not turn every story beat into a slide. Put connective context in the talk track;
combine time-based beats in a timeline; use a separate slide only when the audience
must pause, reinterpret the story, or inspect distinct evidence. When persistence is
central, show a decision point, its opportunity cost, and the convictions that made
continuing rational. When an external event opens a strategic window, show the
preparation runway that made the moment actionable.

For a reveal or embed, specify `default → trigger → changed state → static fallback`;
the default must communicate the conclusion without interaction. Prefer replacing one
state with another in stable geometry instead of accumulating every layer on screen.
In timelines, compress routine activity and emphasize decisions and reversals. Require
one real iteration when available:
`before → evidence → changed decision → after → why better`.
Use a split screen, two-slide pair, or toggle. If evidence is absent, place a gap where
the iteration belongs; never invent it.

Insert a `SECTION-##` cover only at a true mode change such as
`problem → direction` or `product → delivery/outcome`. It must land one bridge thought,
answer “why are we changing topics now?”, take 15–30 seconds, and count toward total
runtime. Do not add decorative chapter dividers or repeat the previous slide's handoff.

Place every story problem where the reader encounters it:

- **Missing beat/page:** insert a gap card between the affected slides.
- **Missing information:** attach it inside the affected slide card.
- **Weak proof/artifact:** attach it to that slide's artifact field.
- **Cut/merge/move:** show the editorial action on the affected slide.

Give each unresolved truth or evidence item a stable `GAP-##` ID, needed evidence, and
truthful fallback. Give settled story beats that still need a visual, diagram, crop, or
animation an `ASSET-##` production item instead. Verify details in
proportion to narrative consequence: prioritize facts that affect ownership, causality,
magnitude, or credibility. Never output separate gap, narrative-spine, and slide-plan
sections. If a problem affects the whole story, place it in the brief diagnosis rather
than repeating it across slides.

Label evidence status:

- `supported`: inspectable evidence supports the claim;
- `stated-only`: the input asserts it without substantiation;
- `inferred`: interpretation based on named source facts; show what it is based on;
- `missing`: required evidence is absent.

Without a source fact, do not infer. Mark the claim `missing` and create a `GAP-##`.

For an existing deck, map each planned slide to source slides and mark `keep`, `revise`,
`merge`, `split`, `move`, `replace`, or `new`.

Before rendering, run the title-only arc test as an action: extract the cover's premise
or opening question and every `SLIDE-##` title in order, then write their one-line arc.
Revise the titles or sequence until the opening question and title group form a clear
arc rather than a result inventory. Run a surprise-leakage check on that sequence: if a
setup or tension title states a later insight, reversal, or emotional payoff before the
evidence earns it, rewrite the title around the immediate stake, problem, or question. Keep it
concrete and truthful; do not replace premature disclosure with vague teaser copy. Let
the reveal or payoff title state the deeper insight at the beat where it is earned. If
the cover asks a question, map it to the named `SLIDE-##` that explicitly answers it;
if no slide does, repair the story or mark the missing answer as a foundation gap. Keep
the one-line arc and payoff mapping private.

### 5. Gate script and follow-up preparation

Stop after the story map unless the user explicitly approves moving into performance
preparation. Treat the storyline as ready only when:

- the one-sentence argument is stable;
- the elephant and highest defensible stake are supported;
- the causal chain, genuine challenge or low, turning point, and outcome are clear;
- the ending wisdom is earned;
- the slide order is settled enough that no known gap would materially restructure it;
- the user has reviewed the story plan and explicitly approved the second pass.

Track the working state privately as `draft`, `clear`, or `approved`. Only `approved`
activates performance preparation by default. A user may explicitly accept a `clear`
storyline and ask to proceed; treat that as an intentional override, not automatic
approval.

When the gate passes, read [script-prep.md](references/script-prep.md) completely and
add performance preparation to the approved story plan. Preserve the original story
map; do not replace slide jobs, evidence, artifacts, gaps, or handoffs with delivery
notes. Do not write a verbatim script unless the user explicitly asks for one.

When the script or talking-point layer is complete, read it together with the approved
story plan before starting interviewer follow-up preparation. Then read
[interview-follow-up-prep.md](references/interview-follow-up-prep.md) and append its
question workspace to the review artifact. If the user supplies an existing script,
use it; it does not need to have been generated by this skill. If no script exists,
stop and ask the user to run `/script` or provide one. Treat the workspace as answer
architecture, not a memorized script.

## HTML output

Follow [html-review-output.md](references/html-review-output.md). Keep the output focused
on story decisions; do not use visual polish to make unresolved narrative structure
appear complete.
