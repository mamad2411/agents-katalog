---
name: agent-engineering
description: >-
  Decision framework for which agent-engineering mechanism, if any, fits a
  workflow problem: durable rule, skill, hard constraint, verification, eval,
  eval harness, feature map, observability, or increased automation/trust.
  Use whenever agents keep breaking something, a change isn't trusted yet,
  it's unclear if Claude can reliably do a task, agents get lost in the
  codebase, or a failure isn't understood — and before proposing any new
  skill, eval, harness, feature map, or automation, to check it's warranted
  rather than overengineering. Complements self-improve: self-improve turns
  one concrete mistake into a durable rule; this skill decides which
  category of mechanism a broader or fuzzier problem calls for. If it's
  simply one mistake that needs to not happen again, hand off to
  self-improve instead of running this whole framework.
---

# Agent Engineering

A durable decision framework for your own agent system. It exists because you
will forget the reasoning behind past choices — this skill is the memory of
*how to decide*, not a record of what you've already built.

## The one rule that matters more than any mechanism

> **Do not build agent infrastructure because it sounds useful. Let a real,
> repeated problem determine what gets promoted, and promote the smallest
> thing that reliably solves it.**

Every section below exists to serve that rule. If you're ever unsure, come
back to this sentence before adding anything.

## First questions, always: is there evidence, and has this recurred?

Before consulting anything else, ask:

- What's the actual evidence this is a problem — not a hunch, a single
  transcript, a diff.
- Did this happen **more than once**, or am I reacting to a single event?

**Default: don't promote a one-off mistake.** Just fix it and move on. If
you catch yourself wanting to build something after *one* occurrence,
that's the overengineering instinct — stop and just fix the thing.

**Exceptions require a concrete reason**, not a hunch — either:
- the cost of recurrence would be unacceptable even once (security,
  data loss, irreversible action), or
- the mechanism is genuinely cheap and strongly justified even for one
  occurrence (e.g. a one-line hard constraint that removes a whole class
  of mistake outright).

Continue below if the answer is "yes, this keeps happening," "I genuinely
don't know, and not knowing is itself the problem" (→ Observability), or one
of the exceptions above applies.

## Relationship to `self-improve`

```
self-improve
    ↓
"I found a specific recurring mistake.
 How do I make this lesson durable?"
    → turns a confirmed recurring mistake into durable project
      knowledge — normally a rule in AGENTS.md, or an update to an
      appropriate skill.

agent-engineering (this skill)
    ↓
"What kind of agent-engineering mechanism
 should exist for this problem, if any?"
    → resolves to: nothing, a rule (→ hand to self-improve), a skill,
      a hard constraint, verification, an eval, an eval harness,
      observability, a feature map, or a trust/automation step.
```

Rule of thumb: if the shape of the problem is already obviously "agent did
one wrong thing, need a standing instruction," skip straight to
`self-improve`. Use this skill when the problem is broader, fuzzier, about
*trust*, *measurement*, *navigation*, or *understanding* — or when you're not
sure which of those it is yet.

## The promotion ladder

Walk this in order. Stop at the first rung that fits — do not keep going
"just in case."

```
One-off mistake
    → fix it. Nothing durable.

Reusable/repeated mistake ("what should be true")
    → durable rule (system.md or AGENTS.md — see placement below;
       hand off to self-improve to encode it)

Repeated multi-step workflow ("how should this be done")
    → skill

Mechanically detectable violation ("can the machine reject this outright")
    → hard constraint (lint rule, type constraint, CI gate, schema)

Behavior needs concrete proof ("can we demonstrate it actually works")
    → verification (run the compiler/linter/tests/the real thing)

Need to measure whether an agent can perform a task at all, repeatably
    → eval (a single scripted task + fresh state + objective check)

Many evals exist and running them by hand is now the bottleneck
    → eval harness (only once evals themselves are the burden)

Agent behavior is hard to understand or explain
    → observability (investigate before writing more instructions)

Agent struggles to navigate a large/unfamiliar codebase
    → feature map

Verification is reliable AND trust has been earned through repetition
    → consider multiple agents / cloud agents

Verification is strong AND reliability has held up over time
    → consider automation / auto-merge
```

This is a **decision tree**, not a checklist. Most problems resolve at rung
one, two, or three. Reaching the bottom of the ladder should be rare and
should feel earned, not routine.

## Definitions — what question each mechanism answers

| Mechanism | The question it answers |
|---|---|
| **Rule** | What should be true? |
| **Skill** | How should this recurring, multi-step workflow be performed? |
| **Hard constraint** | Can the machine itself prevent or reject this mistake, so it never depends on the agent remembering? |
| **Verification** | Can we demonstrate the resulting behavior actually works — not just that code changed? |
| **Eval** | Can we repeatedly determine whether an agent can successfully perform this *class* of task? |
| **Eval harness** | Can we automatically run many such evaluations without manual effort? |
| **Feature map** | Can we give the agent a usable map of where functionality lives, so it stops getting lost? |
| **Observability** | Can we actually see what the agent did and why it failed, instead of guessing? |

Keep these distinct. A common overengineering pattern is reaching for a
skill when a hard constraint would remove the problem entirely (the agent
literally cannot make the mistake), or reaching for an eval when a plain
test already answers the question.

## Where does this belong? (placement table)

| Situation | Put it in |
|---|---|
| General operating behavior, tone, always-on agent posture | `system.md` |
| Project-specific durable rule ("what should be true here") | `AGENTS.md` |
| A recurring multi-step workflow with judgment calls | a specialized skill |
| A rule that can be mechanically checked | a test/check/lint rule/CI gate, not prose |
| "Does the change actually work" | verification, run at the narrowest useful scope while working |
| "Can an agent reliably do this class of task" | an eval |
| "We have too many evals to run by hand" | an eval harness |

If something *could* be a hard constraint instead of a rule, prefer the hard
constraint — prose rules rely on the agent remembering to read and obey
them; machine checks don't.

## Verification: the core principle

> An agent should not claim something works merely because it changed the
> code successfully.

**Use the evidence that most directly tests the behavior being changed** —
not a fixed strength ranking. A compiler isn't "stronger" than a browser
check; they answer different questions. Match the tool to the change:

```
TypeScript/type change   → compiler / typecheck
Logic / unit behavior    → unit test
API behavior             → integration / real API call
UI behavior              → browser interaction / screenshot
Generated artifact       → inspect the artifact itself
Data layer               → database query
Performance              → benchmark
```

Where more than one kind of evidence would answer the same question, prefer
the automated/objective one over the manual one — but never substitute a
cheaper check for one that actually exercises the changed behavior.

Two speeds of verification:
- **While working**: narrowest useful check — the specific test, the one
  affected path, a quick type-check. Fast feedback loop.
- **Before declaring done**: broader check — full test suite, the actual
  user-facing behavior, not just the unit under change.

"It compiled" and "the diff looks right" are not verification. Prefer
evidence that the *behavior* changed as intended, not just the code.

### Test vs. verification vs. eval — don't collapse these

| | Question it answers |
|---|---|
| **Test** | Does the software satisfy a known, fixed property? |
| **Verification** | Does *this specific change* actually work? |
| **Eval** | Can an agent successfully perform *this class of task*, repeatably? |

A passing test suite is not automatically "verification" of a given change
(it may not cover what changed), and a test is not an "eval" (a test checks
the software; an eval checks the agent's ability across attempts at a task
class). Don't let "eval" become a fancier word for "test" — that's how
eval-sounding infrastructure gets built where a plain test already answers
the question.

### A single result is not general capability

A single successful or failed task is evidence about *that run*, not
necessarily evidence about the agent's general capability at the task
class. One failure doesn't mean the agent can't do it; one success doesn't
mean it reliably can. Producing correct code once is not the same as having
a reliable workflow for that class of task — that gap is exactly what evals
exist to close when it matters enough to measure.

## Evals: no framework required

An eval is not a product. The minimum viable eval is:

```
Task
  ↓
fresh/controlled starting state
  ↓
agent attempts the task
  ↓
objective verification
  ↓
PASS / FAIL
```

That's it. A single script, a fixture directory, and a check is a complete
eval. Do not reach for an eval harness, a dashboard, or a framework until you
have enough individual evals that *running them by hand* has become the
actual bottleneck — not before. Building the harness before you have the
evals is building infrastructure on spec.

## Trust progression

Autonomy is earned, not assumed. Do not treat "run without supervision" as
the default goal.

```
agent
  ↓
human supervision (backseat driving)
  ↓
verification exists and is trusted
  ↓
repeated successful tasks under that verification
  ↓
increased trust
  ↓
less supervision needed
  ↓
multiple agents in parallel
  ↓
cloud agents (further from direct supervision)
  ↓
automation / auto-merge
```

Each step down requires the step above to have actually held up over time —
not "it worked once," but repeated, verified success. Skipping straight to
"let it auto-merge" without earned trust and strong verification is the
single riskiest overengineering move on this list, because it removes the
human at the exact moment verification quality matters most.

## Git history and PR shape as evidence

Two cheap, always-available sources of evidence, worth checking before
inventing new instrumentation:

- **Git history** tells you whether a "recurring" problem is really
  recurring, and how it's evolved — search past commits/PRs for the same
  class of mistake before assuming this is new.
- **Atomic changes / small PRs** are themselves a verification and
  observability aid: a large diff hides what actually happened; a small,
  reviewable diff makes both human review and rollback cheap. If agents keep
  producing hard-to-verify changes, "make PRs smaller and more atomic" is
  often a cheaper fix than adding tooling.

## Multiple agents / cloud agents / automation

Only consider these once:
- Verification for the relevant task is reliable (not aspirational), and
- Trust has been earned through repeated success under that verification.

They are a *consequence* of a mature verification + trust setup, not a
starting point. Don't introduce parallel or cloud agents to "go faster" if
the underlying verification is weak — that just parallelizes unverified
work.

## Anti-overengineering checklist

Run this before proposing any new mechanism. If any answer is "no" or "not
sure," don't build it yet.

- [ ] Has this actually recurred (not just happened once)?
- [ ] Have I checked git history to confirm this isn't already handled or
      already tried?
- [ ] Is there a smaller mechanism (rule < hard constraint < existing test)
      that solves this without new infrastructure?
- [ ] Am I proposing an eval because it's genuinely unclear whether the
      agent can do this class of task reliably — or because evals sound
      rigorous?
- [ ] Am I proposing an eval harness only because I already have enough
      individual evals that running them by hand is the real bottleneck?
- [ ] Am I proposing a feature map because navigation is an observed,
      repeated problem — or because "give the agent a map" sounds prudent?
- [ ] Am I proposing observability tooling because the failure genuinely
      can't be understood cheaply by just reading the transcript/diff — or
      because it feels like the professional thing to add?
- [ ] Am I about to add a dependency when existing tooling (linter, type
      system, CI) can already enforce this?
- [ ] Am I about to turn a single human correction into a permanent rule,
      instead of just accepting the correction once?
- [ ] Is there existing agent infrastructure (a rule, skill, eval, check)
      that no longer earns its keep and should be deleted instead of added
      to?

Stale infrastructure is a real failure mode: a skill nobody triggers, an
eval nobody runs, a rule that no longer reflects the codebase — these cost
context and trust just like missing infrastructure costs reliability.
Removing them is as legitimate an outcome of this framework as adding
something.

## How to use this skill when invoked

1. Get the concrete symptom and the actual evidence for it in one sentence.
   If it isn't repeated and doesn't meet a stated exception, stop —
   **recommend nothing**, just fix it. "No new mechanism" is a first-class,
   often-correct output of this skill, not a failure to find one.
2. Walk the promotion ladder top to bottom; stop at the first rung that
   genuinely fits.
3. Name the mechanism using the definitions table, and say explicitly which
   question it answers.
4. If it lands on "durable rule," hand off: "this is a job for
   `self-improve`" rather than drafting the rule yourself here.
5. State the smallest version of the mechanism (e.g., "this is a single
   script + fixture, not a harness"; "this is one lint rule, not a skill").
6. Say what you are *not* recommending and why — including "nothing, because
   existing tooling/a single instance/insufficient evidence" when that's the
   answer — so the anti-overengineering reasoning is visible, not just the
   conclusion.

### Worked shapes

- "Agents repeatedly break this workflow" → check recurrence → rule, skill,
  hard constraint, or verification gap, in that order of investigation.
- "I want to know if Claude Code can reliably implement this class of
  issue" → eval (single script + fixture + check first; harness only if
  many such evals pile up).
- "Agents keep getting lost in this huge repo" → feature map.
- "I don't understand why the agent keeps failing" → observability first;
  do not add more prose instructions until you can see what's actually
  happening.
- "Should this run without me watching it" → trust progression check:
  is verification reliable, has it succeeded repeatedly, only then loosen
  supervision.
