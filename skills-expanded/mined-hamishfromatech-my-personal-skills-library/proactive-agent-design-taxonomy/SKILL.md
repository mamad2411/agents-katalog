---
name: proactive-agent-design-taxonomy
description: Design coding agents that are situation-aware and proactively surface the right insight at the right time, not merely execute on command. Covers the three-level proactivity taxonomy (Reactive, Scheduled, Situation-Aware), insight-policy design, interruption-cost reasoning, and the IDQ/CGS/LL evaluation framework. Use when building IDE agents, coding assistants, or autonomous developer tools where timing, relevance, and trust matter more than throughput. NOT for batch automation or simple reactive chatbots.
---

# Proactive Agent Design Taxonomy

## Overview

Coding agents have matured from inline completion to autonomous execution, but the next frontier is proactivity: agents that notice context shifts, infer what matters, and decide whether to notify, question, draft, or stay silent — before a human asks. The arXiv 2026 research "Agentic Coding Needs Proactivity, Not Just Autonomy" establishes that no deployed coding agent currently documents meaningful interruption-cost reasoning or explicit silence as a learned action. This skill closes that gap with a three-level taxonomy, an insight-policy framework, and measurable evaluation metrics.

## When to Use

- Designing IDE agents or coding assistants with ambient intelligence
- Moving from Level 2 (scheduled/triggered) to Level 3 (situation-aware) agent behavior
- Building trust through calibrated interruption rather than constant availability
- Evaluating vendor coding agents against timing quality, not just task success
- NOT for simple reactive chatbots, batch CI jobs, or always-on interruptive assistants

## Core Insight: Three Levels of Proactivity

| Level | Name | Initiation | Learns From Feedback? | Silences as Explicit Action? | Example |
|-------|------|-----------|----------------------|---------------------------|---------|
| 1 | Reactive | Developer prompt only | No | No | Copilot-style inline suggestion |
| 2 | Scheduled | Schedule, webhook, or predefined event | Weak / partial | Rarely | Claude Code Routines, Cursor Automations |
| 3 | Situation-Aware | Continuous event stream monitoring | Yes — per-developer policy | Yes — deliberate silence | Hypothetical ambient agent with learned Cost_int |

**The gap:** Most 2026 products cluster at Level 2. They run autonomously but do not learn a cross-context interruption policy. The critical missing piece is judgment: when to interrupt, what to show, and when to remain silent.

## The Insight as Unit of Behavior

A proactive agent does not emit tasks — it emits insights. An insight is a context-grounded, time-sensitive hypothesis about what matters next, paired with one of four actions:

1. **Notify** — Surface a state change or risk for awareness.
2. **Question** — Ask for missing intent when ambiguity is high.
3. **Draft** — Produce a low-ambiguity artifact (patch, comment, review thread).
4. **Stay Silent** — Deliberately withhold an insight when interruption cost exceeds expected benefit.

An insight policy selects the action, chooses evidence, frames any message, and updates future decisions from feedback.

## Interruption-Cost Reasoning

A Level 3 agent evaluates:

```
action* = argmax [ E[utility(outcome)] - Cost_interruption(state, action) ]
```

Where `Cost_interruption` is not constant. It depends on:
- IDE focus state (typing, debugging, idle)
- Edit cadence and test activity
- Calendar status and sprint deadlines
- Recent dismiss/defer signals from this developer
- Recovery cost for the current task type (bug fix vs. architecture)

**Practical proxy signals:** idle time, active file, error state, commit cadence, recent agent dismissals. All telemetry must be locally scoped and privacy-preserving.

## Four Acceptance Criteria for Insights

Before shipping a proactive agent, every candidate insight must satisfy:

1. **Relevant now** — Expected benefit exceeds interruption cost; silence is chosen when the same fact can safely wait.
2. **Grounded** — A reviewer can recover the files, diffs, tickets, logs, or signals that support the claim.
3. **Action-matched** — Notify for awareness, question for missing intent, draft for low-ambiguity work, silence for low-value or poorly timed items.
4. **Learnable** — Acceptance, dismissal, deferral, and edits change future timing or framing for this developer.

## Evaluation Metrics: IDQ, CGS, LL

Unlike SWE-Bench (which scores task completion), proactive agents must be scored on insight quality.

### Insight Decision Quality (IDQ)
Did the agent choose the right action at the right time?
- Full credit for the reference action
- Partial credit for reasonable alternatives
- Penalties for false interruptions, missed opportunities, wrong action types, bad timing
- Scores both shown insights **and** deliberate silence

### Context Grounding Score (CGS)
Is the shown insight supported by the right evidence?
- F1 harmonic mean of evidence precision and recall against reference support facts
- Fact-check: claims in the message must be faithful to the evidence
- Not applicable when no insights are shown (silence is the correct action)

### Learning Lift (LL)
Does feedback improve later decisions?
- Compare adapted policy (learns from feedback) vs. frozen policy (does not)
- Evaluated on the same later decision points
- Positive LL means feedback improved timing or action choice

**Valid ranges:** Report all three together. High IDQ + low CGS = good timing, weak justification. High CGS + low IDQ = grounded but poorly surfaced.

## A-Tech Application: A-Coder Ambient Mode

### Current Gap
A-Coder operates mostly at Level 2 (user-triggered or spec-driven execution). The missing layer is ambient monitoring that surfaces migration risks, dependency drift, or security alerts only when the developer is already in the relevant context.

### Level 3 Implementation Targets
1. **Event stream ingestion:** Repository diffs, CI logs, dependency advisories, issue updates, calendar events — merged into one timestamped ledger.
2. **Insight engine:** Runs in shadow mode, scoring candidate insights by IDQ before surfacing any.
3. **Silence logging:** Records candidate insights that were withheld so the policy can be audited post hoc.
4. **Feedback loop:** Each surfaced insight captures accept/edit/dismiss/defer, updating the per-developer model.
5. **Privacy boundary:** Raw telemetry (focus state, edit cadence) stays local; only project-level evidence (affected files, CI status) enters shared channels.

### Checkpoint Workflow
Instead of autonomous end-to-end execution, proactive A-Coder operates as an accountable decision surface:
- Inbox view of shown and deferred insights
- Developer accepts, edits, defers, or dismisses each insight
- Each response feeds back into the policy model
- Autonomous execution happens only after human checkpoint within trusted scopes

## Anti-Patterns

- **Show every detected issue** — Ignores interruption cost entirely; floods the developer.
- **Always-silent fallback** — Defeats the purpose; no insight stream means no value.
- **One-size-fits-all timing** — Ignores that a 3 PM alert and a 3 AM alert have wildly different costs.
- **Task-completion as sole metric** — SWE-Bench tells you nothing about whether the agent annoyed the developer along the way.
- **Surveillance telemetry** — Sending raw IDE state to cloud undermines the trust required for sustained partnership.

## Cross-References
- `developer-experience-and-flow/agentic-interface-consolidation` — Single-tool consolidation for flow preservation
- `developer-experience-and-flow/flow-state-engineering-for-coding-tools` — Neuroscience of developer flow and interruption recovery
- `developer-experience-and-flow/ai-assisted-engineering-discipline-2026` — Spec-before-code planning that proactive agents monitor
- `developer-experience-and-flow/proof-first-ux-accountability` — Transparency in agent actions and reasoning traces
- `cognitive-science-and-ux/context-switching-taxonomy-ai-assisted-work` — Measuring the cost of context switches that proactive agents must respect

## References
- See [references/proactive-coding-arxiv-deep-dive.md](references/proactive-coding-arxiv-deep-dive.md) for the full arXiv paper summary, agent comparison table, and active-user-simulation protocol.
- See [references/interruption-cost-literature.md](references/interruption-cost-literature.md) for Meyer et al. 2024, Mehrotra et al. 2016, and Okoshi et al. 2015 recovery-time data.

## Date Researched
2026-06-19 | A-Tech Research Division
