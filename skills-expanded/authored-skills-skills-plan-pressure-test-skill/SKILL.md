---
name: plan-pressure-test
description: >-
  Pressure-test a product idea, feature, plan, or client engagement BEFORE
  committing build effort. Runs a six-question forcing interrogation,
  recommends one of four scope modes (Expansion / Selective Expansion / Hold
  Scope / Reduction), and surfaces only the genuine taste decisions for the
  operator. Use when deciding what to build, scoping a feature or product,
  prioritizing a roadmap, planning a client engagement or course module, or
  asking "is this worth building", "how should I scope this", "which should I
  build first", "should I add X", "am I overbuilding this", "is there real
  demand". Especially apt for Question Pilot product decisions, AI Agency
  Course content, and client work. NOT for executing an already-decided build,
  code review, debugging, implementation planning of a settled spec, or the
  open-ended greenfield "where do I even start with AI" case (that is
  silver-platter).
allowed-tools:
  - Read
  - AskUserQuestion
---

# plan-pressure-test — forcing questions + scope modes

Local operator skill (structure lifted from gstack `office-hours` /
`plan-ceo-review` / `autoplan`). The gstack originals are sharp but
YC/founder-voiced. This keeps the **interrogation structure and the scope-mode
ladder** and deliberately drops the pitch-culture framing — it serves the
operator's own product calls (Question Pilot), course design (AI Agency Course),
and client engagements, where the question is rarely "will this 100x" and usually
"is this the right thing to build, scoped the right way, right now."

## Why this exists

The expensive mistake in product work is not bad execution — it is building the
wrong thing, or the right thing at the wrong scope, *confidently*. The cost is
paid weeks later. This skill front-loads that cost into a few minutes of honest
interrogation: it makes the implicit assumptions behind a build decision explicit,
forces evidence where there was only enthusiasm, and lands on a scope that matches
how proven the idea actually is.

The second principle, lifted from `autoplan`: **don't make the operator
adjudicate things that have a determinate answer.** Most of a scoping pass is
mechanical — checking whether demand is evidenced, what the status quo is, whether
a wedge exists. Run that yourself. Only the genuine *taste* calls — the ones that
turn on values, risk appetite, or a bet about the future — deserve the operator's
attention. Surfacing everything is just noise that trains them to rubber-stamp.

## How to run it

A pass is one structured loop, not a rigid script. Adapt depth to the stakes — a
throwaway feature gets a quick version; a quarter of roadmap or a paid client
engagement gets the full treatment.

### 1. Frame the decision in one line

State what is actually being decided, concretely. "Should Question Pilot add
bulk-export of the diligence Q&A log?" beats "thinking about export stuff." If the
operator's request is vague, pin it down first — you cannot pressure-test a fog.

### 2. The six forcing questions

Work through all six. For each, draw on what is already in context (the
conversation, the repo, the vault, prior product notes) and **answer what you can
yourself** — only ask the operator where the answer genuinely requires information
or judgment you don't have. Record each answer plus your confidence in it; a
question you answered from assumption rather than evidence is itself a finding.

1. **Demand-reality** — Is there real, *evidenced* pull for this, or is it
   assumed? What is the proof someone wants it — a request, a repeated complaint,
   an observed workaround, a churn reason? "It would be cool" is not demand.
2. **Status-quo** — What do these people do *today* instead? Every new thing
   competes with an existing workaround (a spreadsheet, a manual step, a
   competitor, doing nothing). Name it, and name why they'd switch. If the status
   quo is "fine," the bar is high.
3. **Desperate-specificity** — Who *exactly*, in what *exact* moment, needs this
   badly enough to change behaviour? Name the specific person and situation, not a
   demographic. Breadth is the enemy here — "M&A analysts" is a market;
   "the analyst at 11pm reconciling 40 conflicting answers before a Monday IC
   meeting" is a wedge.
4. **Narrowest-wedge** — What is the *smallest* first slice that delivers real
   value to that specific person and earns the right to do more? Resist shipping
   the whole vision. The wedge is what you can build fast, prove, and expand from.
5. **Observation** — What have you actually *observed* (first-hand: usage, support
   threads, session logs, watching someone work), versus theorized at a desk?
   Separate the two explicitly. Theory dressed as observation is the most common
   way scoping goes wrong.
6. **Future-fit** — Does this still make sense as the tech and market move? Is it
   durable, or a point-in-time patch that a model upgrade or a platform shift
   erases in six months? Not every patch is wrong — but name which kind it is.

### 3. Recommend a scope mode

Based on the answers, recommend exactly one of four modes, with a one-paragraph
rationale tied to the findings above. The mode follows the evidence: strong
evidenced demand + a proven wedge points toward expansion; thin or assumed demand
points toward holding or cutting.

- **Expansion** — Broaden the scope; build more, add capability. Justified only
  when demand is evidenced, the wedge is proven, and observation (not theory)
  backs it. The rarest recommendation; demand it earn its place.
- **Selective Expansion** — Add only the single highest-leverage adjacent piece;
  keep everything else tight. The "yes, and *just* this" mode.
- **Hold Scope** — Don't change scope; ship and refine what is already defined.
  The honest default when the evidence is mixed or the current scope is untested —
  prove the wedge before touching the boundaries.
- **Reduction** — Cut scope; remove features, narrow to the core wedge. The right
  call when the idea is spread thin, demand is unproven, or the build is outrunning
  the evidence. Reduction is a result, not a failure.

### 4. Taste-decision gate

Now separate your findings into two piles, and treat them differently:

- **Mechanical / determinate** — has a defensible answer from the evidence (is
  demand evidenced? does a wedge exist? what's the status quo?). **Resolve these
  yourself** and state the resolution. Do not put them to the operator.
- **Genuine taste decisions** — turn on the operator's values, risk appetite, or a
  bet about the future that evidence can't settle (how much to wager on an
  unproven-but-promising wedge; whether a durable-but-slow play beats a
  point-in-time win; which of two defensible wedges fits the brand). **These, and
  only these, go to the operator** — ideally via a focused `AskUserQuestion` with
  the options framed and your recommendation marked.

If there are zero genuine taste decisions, say so and just give the recommendation.
Manufacturing a decision to "involve" the operator is the anti-pattern.

### 5. Output

Keep it tight — a scoping pass is a decision aid, not an essay. Use this shape:

```
## Decision
<the one-line framing>

## Forcing questions
- Demand-reality: <answer> (confidence: <high/med/low — evidence or assumption>)
- Status-quo: <answer>
- Desperate-specificity: <answer>
- Narrowest-wedge: <answer>
- Observation: <observed vs theorized, separated>
- Future-fit: <answer>

## Recommendation: <SCOPE MODE>
<one paragraph tying the mode to the findings — especially the wedge>

## Resolved (mechanical)
<the determinate calls you settled, one line each>

## Your call (taste decisions)
<only genuine judgment calls — or "none; recommendation stands">
```

## Notes

- This is an interrogation, not a cheerleader. Its value is in the honest "no" or
  "smaller" as much as the "yes." If every pass returns Expansion, it's broken.
- Lean on context first. The operator runs this *because* the relevant evidence
  (repo, vault, sessions, prior decisions) is often already reachable — go find it
  before asking. An interrogation that's all questions back to the operator has
  done none of the work.
- Pairs naturally with the vault's decision notes: a pass that lands a real
  product bet is a candidate for a `03-Decisions` note at closeout.
