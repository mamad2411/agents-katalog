---
name: goal-driven
description: |
  Goal-driven methodology for initiatives where the destination is clearer
  than the path. GOAL.md is the stable compass — the General Line plus falsifiable
  success criteria. The record captures what was tried, what was observed,
  and whether each criterion is still served. The agent writes both files;
  the human approves edits via chat.

  Use this skill for multi-week initiatives where upfront design is the
  wrong tool: research, exploratory features, learning projects with a
  shippable output, writing a book or article series, job search,
  side-business launches. Trigger on phrases like "set a goal", "track
  my progress on X", "this is exploratory", "I know the goal but not
  the path", or when starting a months-long initiative without a clear
  technical shape.

  Do NOT trigger for single-task work, bug fixes, week-long features
  with a clear plan, vague aspirations ("be healthier", "write more"),
  habit tracking, or general life management — this skill is overkill
  for those. A TODO list, notebook, or habit tracker serves better.

  Pairs with design-driven. Goal-driven manages why and how-far;
  design-driven manages what-shape. Use both when a project is uncertain on
  direction AND structure. Each works alone — they cross-reference but do
  not depend on each other.

  Supports arguments: `/goal-driven set` to interview-drive an initial
  GOAL.md and scaffolding, `/goal-driven review` for strategic
  checkpoint plus protocol maintenance, `/goal-driven close` to wrap
  up a finished initiative with a retrospective and archive.
argument-hint: "[set | review | close]"
---

# Goal-Driven

A mini methodology for initiatives where the destination is fixed but the
path isn't. Human owns the compass; agent walks the path and keeps the log.

GOAL.md is the institutional memory of *why*. The record is the
institutional memory of *what was tried*. Together they let a fresh agent —
or future-you — pick up a months-long initiative without losing direction.

## Commands

When invoked with an argument, dispatch to the corresponding file:

- `/goal-driven set` → Read and follow `commands/set.md`.
  First run: interview the human and produce the initial GOAL.md,
  plus scaffolding. Re-run: update mode — refreshes the agent-config
  blocks (including cross-references to sibling skills installed
  since), re-checks plumbing. Doesn't re-interview the goal; for
  re-assessment use `review`.
- `/goal-driven review` → Read and follow `commands/review.md`.
  Strategic checkpoint plus protocol maintenance: re-assess where the
  project stands against GOAL, surface drift, propose corrections.
- `/goal-driven close` → Read and follow `commands/close.md`.
  Wrap up a finished initiative: draft retrospective, mark GOAL closed,
  archive `goals/`.
- No argument → continue with the methodology below (the normal loop).

**Which command when:**

- New initiative → `set`
- A sibling skill was installed/removed and agent-config cross-
  references feel stale → `set` again (update mode; no re-interview)
- ≥ 2 weeks since last review, record feels overgrown, midpoint of an
  explicit timeline, or you sense you've drifted → `review`
- Initiative is done, abandoned, or superseded → `close`
- Mid-work, just logging progress → no argument (normal loop)

## When to use this skill (and when not)

**Good fit:**
- Multi-week or longer; ≥ 3 uncertain decision points likely
- The path is genuinely unclear — you'd rewrite a detailed plan in 2 weeks
- Success criteria can be stated, even if some are observable proxies

**Bad fit:**
- One-off scripts, bug fixes, week-long features with a clear plan → use a
  TODO list
- Pure execution where the path is known and only the doing remains → use
  design-driven blueprints
- Goals you can't articulate at all → spend an hour writing first; come
  back

**For personal use specifically.** This skill works for personal
initiatives that look like projects, not for general life management.
The threshold is four conditions held together: multi-week+ horizon;
articulable falsifiable criteria (or paired proxies); willingness to
engage with the agent ≥ weekly; the cost of failure warrants the
friction. Below that — vague aspirations ("be healthier", "write
more"), weekly habits, generic quarterly planning — a notebook or habit
tracker serves better. Concrete fits: book / article series, learning
projects with a shippable output, job search, side-business launch,
training plans with concrete metrics. Concrete misfits: anything where
"how would I know I'm done?" can't be answered without hand-waving.

## Directory structure

```
project/
└── goals/
    ├── GOAL.md                  ← Stable compass (General Line, criteria, invariants)
    ├── OPEN-STOPS.md            ← Index of unresolved STOP signals
    ├── record-2026-04.md       ← Past month
    └── record-2026-05.md       ← Current month (auto-rotates monthly)
```

Two stable files (GOAL.md, OPEN-STOPS.md) plus monthly records. No
`archive/` directory by default — old months stay in place. If `goals/`
becomes crowded after a year, move them under `goals/record-archive/`
manually; the convention is informal.

## The compass / path asymmetry

GOAL.md is the compass. It changes rarely, by deliberate human decision.
The path is everything else: what you're trying this week, what you tried
last week, what worked, what didn't.

The path mutates constantly. The compass mutates only when:

- A success criterion turns out to be the wrong measure (replace it)
- The General Line itself is questioned by new evidence (rethink it)

Both are deliberate, human-approved events. They are NOT what happens when
"I tried X and it didn't work, let me try Y" — that's just walking.

This asymmetry is the whole point. If GOAL.md and the record change at the
same rate, you don't have a compass; you have a notebook.

## Permission gradient

| File | Who writes | When | Human's role |
|---|---|---|---|
| `GOAL.md` | agent | Only at initial set or explicit GOAL change | Approves each section, line by line |
| `record-YYYY-MM.md` | agent | End of session, or on STOP / rotation | Reviews entry draft in chat before write |
| `OPEN-STOPS.md` | agent | When a STOP is created or resolved | Confirms the line in chat |
| STOP signals | agent surfaces | When trigger condition hit | Decides: change path / change goal / agent misjudged |

**Never let the agent silently edit GOAL.md.** Every change must be echoed
in chat first. Even adding a single criterion is a deliberate event.

The agent is not a passive scribe — it drafts, proposes, surfaces. The
human is not a writer — they approve, redirect, decide. This asymmetry
prevents two failure modes at once: human laziness ("I'll write the goal
later") and agent drift (silent rewording into something subtly different).

## The three-moment protocol

The agent's default behavior — drafting, exploring, summarizing — is
usually fine. But three moments bias toward silent drift if left to
defaults: when first articulating the goal (premature commitment to fuzzy
wording), when ending a work session (forgetting what just happened and
why it matters to the criteria), and when evidence threatens the goal
(rationalizing past inconvenient signals to keep moving). The protocol
intervenes at exactly those moments. Outside them, normal work.

### Moment 1 — Setting the goal (creating GOAL.md)

The agent interviews the human via chat. It does **not** draft GOAL.md
alone and present it for review. It asks, in order:

1. **General Line** — "In one or two sentences, what should be true when
   this is done?"
2. **Success criteria** — for each thing implied: "How would you know
   that's achieved?" Push for falsifiable; if soft, push for a proxy
   indicator.
3. **Invariants** — "What must stay true regardless of how we get there?"
4. **Non-goals** — "What's tempting but explicitly out of scope? What
   would an outsider lobby for that we've already decided against, and
   why?" Push back if a candidate is just an inverted goal — non-goals
   are forbidden zones, not goals restated in the negative.

The agent **echoes each section back as it's drafted**, gets confirmation,
moves on. GOAL.md is written only after all sections are confirmed. See
`commands/set.md` for the full interview script.

### Moment 2 — End of every work session

Before the session ends, the agent drafts a record entry **in the chat**:

```
Entry draft:
- What I did: ...
- Observations: ...
- Criteria check:
    C1 ✓ (cite specific evidence)
    C2 ✗ (cite specific evidence)
    C3 unclear (no observation this session)
- Judgment: path-level / goal-level / no change
Confirm and append?
```

The human confirms or edits in chat. Only then does the agent append to
the current month's record.

**The criteria check is the heart of the discipline.** Each ✓/✗ must cite
a concrete observation from the session. `C1 ✓` without evidence is
forbidden — it must be `C1 ✓ (ran 30 queries, recall 76%)` or
`C1 unclear (no test this session)`. Bare verdicts hide drift.

**Verdicts include time.** Some criteria are met or not at the moment
they're checked (latency under 500ms either is or isn't true today).
Others accumulate toward a deadline ("200 paid subscribers by Sep 30"),
and in the run-up they're neither met nor failed — they're on a
trajectory. Judge them by trajectory: one plainly on pace is
`✓ (on pace: <evidence>)`; one whose trajectory has visibly diverged is
`✗ (off pace: <observation> projects <gap>)`. The evidence rule still
applies — "on pace" needs an observation, not optimism. This is the same
verdict vocabulary, used with awareness that what counts as "served"
depends on when the criterion is supposed to land.

**Identify the principal tension.** Attention is finite. At any moment
one tension dominates — the one whose resolution would most unblock the
rest. Name it in the judgment ("this week the binding constraint is C1
pace; C2 stable; C3 not under pressure") rather than treating all
criteria symmetrically; this tells the next session where to spend
attention first. The dominant tension shifts as the project moves through
phases — re-identify it each session from current observations, not
from habit.

**If a session is interrupted before the human confirms.** Append the
draft directly with a `[unconfirmed draft]` prefix in the title; the next
session ratifies or revises it before continuing other work. A protocol
that breaks when sessions don't close cleanly is worse than one that
absorbs the common case.

### Moment 3 — STOP signals

Two types of STOP, each with a different escalation path. Both halt work
until the human decides.

**Type A — Criterion not served.**
A criterion is failing now, or evidence makes its future failure visible
in time to act. The point of STOP is to surface infeasibility while
there's still room to redirect — waiting for a deadline to confirm what
trajectory already shows wastes that room.
- Example (current violation): "C2: P95 < 500ms" but production shows
  720ms after three attempts at different storage layers.
- Example (predictable violation): "C1: ≥ 200 paid subs by Sep 30" with
  22 at end of month one — linear extrapolation lands near 66, not 200.
  The criterion isn't violated yet, but the path is.
- Agent surfaces in chat, proposes three options:
  - (a) Change path (try Y instead of X)
  - (b) Change criterion (require human-approved GOAL edit)
  - (c) Agent misjudged

**Type B — General Line questioned.**
Criteria are met (or close), but new evidence suggests the goal itself
solves the wrong problem.
- Example: criteria all green, but user research reveals users wanted
  topic clustering, not semantic search.
- Agent surfaces in chat, proposes:
  - (a) Reframe the General Line (deliberate GOAL edit)
  - (b) Stay course because the evidence is weak

**Critical:** STOPs are never silently logged and walked past. The agent
must surface them in chat AND wait for the human's choice before continuing
work. A STOP entry in the record without a chat exchange is a protocol
violation.

## Anti-flattery: the evidence rule

Agents writing their own progress reports have an obvious bias toward ✓
verdicts (they want to keep working, not stop and wait for review). The
defenses, in order of strength:

1. **Every ✓ must cite an observation from THIS session.** Not "criterion
   still reasonable", not "no reason to think it broke". A specific thing
   that happened.
2. **If no observation touches a criterion this session, the verdict is
   `unclear`, not ✓.** Default to unclear. ✓ is earned, not assumed.
3. **`unclear` accumulating across many sessions is itself a signal** —
   that criterion isn't being measured. The review command catches this
   and nominates such criteria for retirement or for explicit
   instrumentation.

This rule is the single biggest reason this skill might survive contact
with reality. Without it, the criteria check decays into checkbox theater
within weeks.

## Maintenance

Three things rot if untended: record volume grows unboundedly, open
STOPs across files get forgotten, GOAL.md drifts inconsistent after
edits. The protocol handles each — month-bounded record files cap
volume once the project is long enough to warrant them, OPEN-STOPS.md
indexes unresolved STOPs across files when more than one is in flight,
and `/goal-driven review` periodically reconciles all three plus
re-assesses strategy. See `commands/review.md` for what review covers;
`references/templates.md` for record, STOP, OPEN-STOPS, and carry-over
formats.

Review when ≥ 2 weeks pass since the last one, ≥ 30 new entries
accumulate, the project hits the midpoint of its explicit timeline, a
fresh agent picks up the project, or things just feel off.

## Stories — opt-in interpretation layer

GOAL.md is normative and terse — one line per criterion, one line per
invariant. That's good for fast reading and for keeping the compass
hard to change accidentally; it's insufficient for explaining *why*
each choice was made or what each criterion really means in nuance.

The optional `goals/stories/` directory is a second layer: per-topic
explanatory documents that interpret GOAL.md's terse text. Stories are
mutable (they evolve as understanding deepens), narrative (prose, not
bullet lists), and topic-organized rather than chronological.

```
goals/
├── GOAL.md                              ← terse spec, hard-change
├── stories/                             ← opt-in interpretation layer
│   ├── why-200-paid-subs.md
│   ├── what-counts-as-paid.md
│   ├── channels-considered-and-rejected.md
│   └── ...
└── record-2026-08.md
```

### What goes in a story

Each story is a topic-named markdown file (kebab-case). Typical topics:

- Why a specific criterion is set as it is, including data or context
  that informed the number or threshold
- What an ambiguous term in GOAL.md means in practice
- Background on the choice of General Line — what alternatives were
  considered, why this framing won
- Trade-offs explicitly accepted (what you're giving up to chase this)
- How understanding of a criterion has evolved through STOPs and
  resolutions

Stories don't enforce 1:1 mapping to GOAL items. One story can span
multiple criteria; one criterion may have no story (terse text is
self-explanatory).

### When stories are created

Triggered by:

- **Set time**: at the end of `/goal-driven set`, the agent proposes
  2–3 initial stories based on the interview ("why this initiative",
  "how criteria were chosen") — human picks which to write.
- **STOP resolution**: if resolving a STOP involved re-understanding
  what a criterion really means, the agent proposes adding or updating
  a story.
- **Review trigger**: during `/goal-driven review`, if a criterion
  has been ambiguous through several STOPs, the agent proposes a
  story to clarify.
- **User-initiated**: "let me explain why I'm doing this" — the agent
  helps draft.

### Modification protocols — different shapes for different artifacts

| Artifact | Modification | Frequency |
|---|---|---|
| `GOAL.md` | Line-by-line echo + Revisions log entry; deliberate event | Rare |
| `stories/X.md` | Paragraph-level echo + human approval + write + bump `Last updated`; evolving update | Occasional |
| record entry | Draft + confirm + append; routine | Per session |

The shape of friction differs more than the magnitude. GOAL changes
are **discrete events** — formal, with audit trail in Revisions —
because they invalidate prior criterion checks and any STOPs that
depend on the old wording. Story updates are **evolving** — a
paragraph here, a paragraph there, no formal log needed because they
describe rather than prescribe. Record entries are **continuous** —
every session adds one, structured but quick.

Don't conflate "more chat turns" with "more important". A multi-
paragraph story update may take more turns than a one-line GOAL
revision but is less consequential — the GOAL revision changes what
"done" means; the story update only changes how we explain it.

Each story carries a `_Last updated: YYYY-MM-DD_` footer. A story
untouched for many months while related GOAL items have shifted is a
candidate for refresh — surfaced during review.

### Distinction from record (don't conflate)

| Aspect | record | stories |
|---|---|---|
| **Role** | Event log — raw observations as they happened | Synthesis — current curated understanding distilled from accumulated events |
| Organization | Chronological (by month file) | Topical (by file name) |
| Tense | Past ("today I did X") | Present ("this criterion now means …") |
| Mutability | Append-only | Freely editable |
| Count | A few files over a project | 5–15 typical |
| Use | Reconstruct what happened | See what we currently believe |

Content can overlap; roles differ. A record entry "today's work
shifted my understanding of C2" is the *trigger* for updating
`stories/c2-meaning.md`; the story IS the synthesized current view
that absorbs many such triggers. Read record to reconstruct the
sequence of events; read stories to see the current settled
understanding distilled from those events.

### Cross-references

- record entries can point to stories: "see stories/what-counts-as-paid.md"
- STOP entries can reference stories or trigger story creation
- GOAL.md can footnote stories: `C2: P95 < 500ms (see stories/c2-rationale.md)`

### Default behavior

`/goal-driven set` does not create the `stories/` directory. The first
story being approved is what brings the directory into being. For
single-attempt projects with self-explanatory criteria, stories are
overhead — skip them; the agent only proposes them when there's
something nontrivial to interpret.

## Standalone vs paired with design-driven

Goal-driven works alone. Shape decisions, when they come up in an
exploratory project, live as observations or named alternatives in the
record — no separate proposal flow needed. This is the default mode and
what the rest of this document assumes.

If design-driven is also installed in the project, the two divide labor:
goal-driven owns *why* and *how-far*; design-driven owns *what-shape*.
Each manages its own files; cross-references go by ID, not content (a
record entry says "adopted decision 003"; a decision says "blocks goal
STOP 2026-05-02 if rejected").

**When to bring in design-driven from a goal-only project.** The signal
is: you can describe the system's shape in 2–3 sentences and an outside
engineer would build the same mental model. At that point, run
`/design-driven bootstrap` to extract the implicit shape into DESIGN.md.
Goal-driven keeps running alongside; design-driven takes over the "how"
question. Until that signal, defer — premature DESIGN.md gets rewritten.

Four interaction points to watch when both are present:

1. **Goal pivot crosses design boundaries** → also open a
   `design/decisions/NNN-*.md` proposal. The record entry doesn't
   replace the design proposal flow.
2. **Design proposal would violate GOAL invariants** → trigger a goal
   Type A STOP first; don't let design adopt and then quietly fail
   criteria.
3. **STOP resolution requires shape change** → resolve the goal STOP
   first, then open a design decision.
4. **Cross-checks during periodic inspection** — goal-driven's review
   surfaces design decisions not reflected in the record; design-driven's
   audit surfaces GOAL invariants potentially at risk. (The two skills
   use different command names — `review` vs `audit` — for the same
   periodic-inspection role.)

A third sibling skill — evidence-driven — overlays build-time discipline
on top of design-driven (TDD cycle, falsifiable verification, evidence-
trail State). Goal-driven doesn't read or write to evidence-driven's
domain directly, but the rigor it provides at the execution layer makes
the upward feedback loop trustworthy: STOP signals citing build
observations are only credible if those observations have evidence
behind them.

## Structure follows need

The scaffolding around GOAL.md — OPEN-STOPS.md, monthly record rotation,
periodic reviews — earns its cost when it's load-bearing. A short, single-stream
initiative with no STOPs in sight doesn't need an OPEN-STOPS index; the
one STOP, if it ever appears, lives visibly in the record. A six-week
project doesn't need monthly rotation; a single `record.md` carries it
until it doesn't.

Add structure when the absence starts to hurt: create OPEN-STOPS.md when
a second open STOP exists and you can no longer hold both in mind; rotate
to monthly files when one record becomes too long to scan. The directory
layout shown above is the mature shape, not the starting shape — start
small and grow into it.

GOAL.md is the exception. It's the compass, not scaffolding. Even a
two-week initiative benefits from articulating it. If GOAL.md feels like
overhead for what you're doing, this skill isn't what you need; use a
notebook.

## Example walkthrough

For a concrete end-to-end example — set, several record entries,
two STOP scenarios, resolution — see `references/example.md`.
