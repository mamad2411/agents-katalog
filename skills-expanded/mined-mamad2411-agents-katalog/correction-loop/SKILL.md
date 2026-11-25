---
name: correction-loop
description: Authoritative workflow for handling — or answering questions about — a correction or rework inside the AgentBoard architecture pipeline (research → classification audit → compose → design review). It is the single source of truth that the /architecture orchestration and the compose stages defer to, covering how to source-trace a correction to its real origin in real time, carry it as a declared auditable input into a correction-mode re-run of the right stage, treat the retry cap as a signal to trace outward rather than a hard stop, hand off to the external investigator at the cap, and involve the owner only when the trace lands on the spec. Use this skill — don't improvise — whenever something in an architecture run is wrong, needs reworking, or won't pass, and even when the user only asks how such a situation should be handled: a design-review or audit finding to resolve; a card or plan that keeps failing review or "just won't pass"; choosing whether to hand-edit the architecture document or re-run a stage; an upstream or downstream failure that traces back to an architecture decision; research/audit facts (the verified bundle) that turned out wrong; a component or requirement missing because the spec drifted or never captured it; or questions about where a correction should be routed, how repeated failures and the retry cap should be handled, when to stop retrying and investigate the root cause, when to involve the owner, or whether the architecture flow may edit the spec. Reach for it even when phrased casually — "the reviewer flagged something", "where does the fix go", "do I rerun or patch", "how does this get corrected", "at what point does it stop retrying". Do NOT use it for normal pipeline operation (running /architecture, creating cards, orchestrating a board), for writing or rewriting a spec from scratch, for plain edits such as fixing a typo, or for general explanations of how a pipeline stage works when nothing is being corrected.
---

# Correction Loop

The architecture pipeline has to be able to rework its own output. A design review turns up a real defect, the owner asks for a different decomposition, or something downstream fails for a reason that traces back to a decision made here. This skill is the **single source of truth** for how that rework happens — how it's recognized, routed, carried, bounded, and escalated.

The `/architecture` orchestration and the level compose profiles touch corrections too, but they are **consumers** of this definition, not co-authors of it. If one of them describes the loop differently, this skill is what's correct and that surface is what's out of date. Keeping the definition in one place is deliberate: this loop has been reinvented in scattered copies before, and the copies drifted apart.

## The ideas this loop rests on

Everything below follows from four convictions. Hold them and most decisions make themselves.

**The owner owns the *what*; agents own the *how*.** The spec is the owner's. Every engineering decision beneath it belongs to the agents, who have the context to make it faster and more reliably than handing it back would. So the loop's instinct is always to fix the problem itself, and to spend the owner's attention on the one thing only the owner can settle — the spec.

**Judge in the moment; don't gate.** The same symptom has different root causes on different runs. A static "this kind of problem goes to that stage" table, or a hardcoded reflex like "failed twice, so rewrite the spec," will confidently route to the wrong place and bury the real cause. The loop decides where a problem originated from the evidence in front of it, every time.

**Reason about origin — this is not a reflex bounce-back.** Review and audit today send work back the instant they spot a defect, without asking where the defect came from. This loop is deliberately more thoughtful than that, because fixing a symptom at the wrong stage just reproduces the failure on the next pass. (If this proves out for architecture, the same rigor can later be offered to review and audit.)

**A stuck loop is information.** If three honest attempts on the same target don't resolve it, the problem probably isn't *in* that target. That's a signal to widen the search, not to grind harder or to stop and wait for rescue.

## When a correction happens

A correction is **substantive** rework: a reworked Design decision, a different decomposition, an added or removed Card Slice, a new alternative, or a re-derivation forced by a blocker/serious finding. (A typo, a missed traceability row, or a one-line reword is a plain edit — fix it in place, not through this loop.)

It can arrive from three directions, and it is *not* only "the owner said something is wrong":

1. **A validating stage caught a defect** — most often the design reviewer, which stands to the architecture document as review stands to a plan.
2. **The owner directed a change** — a concern that needs rework. This may or may not happen on a given run; neither forced nor forbidden.
3. **A failure elsewhere traced back here** — something later in the pipeline whose root cause is an architecture decision.

## The workflow

### 1. Source-trace to the real origin
Note which of the three directions raised the correction, then work out where the problem *actually* originates — from the finding, the failure trace, the owner's concern, and the current pipeline state. Resist the urge to map "this type of issue → that stage"; that shortcut is what sends fixes to the wrong place.

### 2. Carry the correction as a declared, auditable input
Hand the correction to the stage that must redo the work as a dedicated, explicit input — not as extra prose dropped into a prompt, and not as a quiet edit to a file or the spec. Undeclared context can't be reviewed later, and silent edits are exactly how the owner's intent has gone missing before. The stage's normal from-scratch inputs don't carry this and aren't a substitute for it.

For the record to be auditable, it needs to capture: which **round** this is, the **origin** (validating-stage / owner-directed / traced-upstream-failure), the **target** stage it's routed to, the **change** being asked for, and the **provenance** that justifies it (the finding id, the owner's instruction, or the failure trace). The exact field shape is defined where the consuming stage declares the input; what matters here is that it's declared and carries those things.

### 3. Route to that origin
There are three destinations. Which one is chosen comes from the source-trace in step 1, not from a rule:

- **The architecture document** — the reasoning, decomposition, traceability, slice boundaries, or a review resolution is wrong, but the upstream facts still hold. Re-enter the compose stage in correction mode (step 4).
- **The upstream facts** — the research/audit facts are wrong, or a failure traces back to them. Re-run the upstream stage for fresh facts before composing again.
- **The spec** — the trace lands on the spec itself: vague, underdefined, or quietly drifted from what the owner meant. The spec may be changed on that basis, but never in-flow and never through `/foundation` (which only *creates* specs). This routes out to the external spec-modification path, whose mechanics are out of scope here. This is the one destination that brings in the owner (step 7), because the spec is theirs.

The common thread: the architecture correction flow never edits the spec to make an architecture problem disappear. The spec and the architecture are separate authorities, and collapsing them is how a real spec problem gets papered over.

### 4. Work in correction mode, not from scratch
The receiving stage runs a correction-mode process that is genuinely distinct from its create-from-scratch flow — because revising existing output is a different task than generating it. In correction mode the stage treats the declared correction as the authoritative statement of what must change, reads the prior output, re-derives only what the correction touches, keeps the rest only where it's still correct, re-validates the whole result rather than just the edited part, and stops to report rather than guessing if the correction is underspecified.

### 5. Treat the retry cap as a signal
The loop runs at most **three attempts on the same card / target**. Reaching that cap is not a wall that ends the loop and dumps the problem on the owner — it's the signal that the cause lives somewhere other than the target you've been hammering. So the search widens and traces outward — to the plan, the architecture, the upstream facts, the spec, or elsewhere — decided in the moment. The agents do that tracing themselves; the system doesn't freeze and wait for the owner to diagnose what the agents are better placed to find.

### 6. Hand off to the investigator at the cap
When the cap is reached, the loop hands off automatically to the external investigator for root-cause analysis. Deeper root-cause work is a different job than review, and it's kept separate on purpose: if the reviewer owned the decision to stop retrying and start investigating, its corrections would sprawl past the stage it was reviewing. The investigator may draw on chat logs, card information, and whatever else is relevant; its internal behavior is defined elsewhere, not here.

> The external investigator is a separate surface and **may not exist yet**. This skill defines the handoff and the condition that triggers it — not the investigator itself.

### 7. Bring in the owner only for a spec-origin outcome
Escalate to the owner only when the trace — the investigation, or a direct read — concludes the origin is the **spec**. That's the one thing agents can't authoritatively settle, and it's where the owner's intent has been silently lost before. Every other origin — plan, architecture, upstream facts, process — the agents resolve at the source themselves.

### The pause is an option, not a gate
A pause is available at the `/architecture` orchestration layer and is **off by default**. The owner turns it on for a run when they want the *option* to look before a routed correction is applied. The loop never makes it mandatory — the whole point of the system is that the owner doesn't have to babysit every step. This pause is also separate from the AgentBoard blocking-gate feature: this skill neither changes nor depends on board settings, and "no app changes right now" must never quietly turn into removing a checkpoint that already exists.

## Out of scope
- The internal behavior of the external investigator agent.
- The mechanics of the external spec-modification path once the trace lands on the spec.
- The AgentBoard blocking-gate (app) feature.
- General agent operating discipline beyond this correction workflow.

## Where this comes from

This workflow is a faithful rendering of the owner's confirmed model, not a fresh invention. Each part traces to a recorded decision so it can be checked.

| Section | Decision records |
|---|---|
| Owner owns *what* / agents own *how*; separate authorities | CL-001, CL-004, CL-006 |
| Judge in the moment, no fixed gates | CL-009, CL-011 |
| Multi-origin corrections | CL-008 |
| 1 — source-trace to the real origin | CL-008, CL-009 |
| 2 — declared, auditable correction input | CL-023, CL-024, CL-028 |
| 3 — route to origin; never edit the spec in-flow | CL-012, CL-013, CL-014, CL-015 |
| 4 — correction mode distinct from create-from-scratch | CL-022, CL-025, CL-026, CL-027 |
| 5 — retry cap as a signal to trace outward | CL-011, CL-018 |
| 6 — automatic, separate investigator handoff | CL-016, CL-017, CL-019, CL-021 |
| 7 — owner escalation only on spec-origin | CL-020 |
| Opt-in, owner-controlled pause | CL-010 |

Sources: ledger records `CL-001..CL-029` in `docs/specs/spec-ledger.yaml`; derived prose `docs/specs/2026-05-16-correction-loop-option-a-design.md`; confirmed model `docs/ideation/2026-06-03-correction-loop-skill.md` and the owner USER EDITs in `docs/handoffs/2026-05-17-correction-loop-design-session-end.md`.
