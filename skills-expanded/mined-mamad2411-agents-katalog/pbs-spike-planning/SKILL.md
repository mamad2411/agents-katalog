---
name: pbs-spike-planning
description: "Use when a technical question needs a real experiment to answer, to generate a structured spike spec before executing it in a separate session"
---

# Spike Planning

## Overview

Generate a structured spike spec for a technical question that needs a real experiment to answer. The spec defines the question, success criteria, time box, and approach — ready to be executed by pbs-spike-execution in a dedicated session.

**Core principle:** A well-defined spike question is half the answer. Vague spikes waste time. This skill forces precision before execution.

**Announce at start:** "I'm using the pbs-spike-planning skill to define a spike for: [question summary]."

## When to Use

- Discovery identified uncertain technical questions that need real experiments (Block 7)
- Mid-construction: you hit an unknown that can't be answered by docs or web search alone
- Evaluating a technology, API, or pattern before committing to it
- Any moment where "I think this works" needs to become "I verified this works"

## When NOT to Use

- The answer is available in official docs or web search → just verify and document
- The question is conceptual, not technical → that's brainstorming, not a spike
- The experiment would take < 30 minutes → just do it inline, no spec needed

## Input

- **Required:** A technical question or uncertainty to resolve
- **Optional:** Context from discovery synthesis, phase spec, or current task

## The Process

### Step 1: Clarify the Question

Turn the vague uncertainty into a precise, answerable question:

```
BAD:  "Does this library work?"
GOOD: "Can Library X parse format Y with nested structures of depth > 5
       without losing data, in under 200ms for a 10MB file?"

BAD:  "Is the API fast enough?"
GOOD: "Does the Canton JSON API respond to party allocation requests
       in under 500ms when 10 concurrent requests are made?"
```

Ask the human to confirm the question is what they actually need answered.

### Step 2: Define Success/Failure Criteria

Make them **measurable**:
- VIABLE if: [specific, measurable condition]
- NOT VIABLE if: [specific, measurable condition]
- INCONCLUSIVE if: [what "we still don't know" looks like]

### Step 3: Set Constraints

- **Time box:** 1-4 hours (default: 2 hours). Complexity-based:
  - API call / library test → 1-2 hours
  - Integration with external service → 2-3 hours
  - Architecture pattern validation → 3-4 hours
- **Constraints:** specific versions, no paid services, must work offline, etc.
- **Context references:** link to the relevant sections of brainstorming/discovery/phase spec so the spike session has full context without needing the current conversation

### Step 4: Suggest Approach

Outline 2-4 concrete steps the spike executor should follow. Be specific enough that a fresh session can start without ambiguity.

### Step 5: Generate Spike Spec

Write the spec to `.pbs-framework/exploration/spikes/spike-XX-[name].md` using the `spike-spec.md.template`.

Naming convention:
- `spike-01-canton-api-latency.md`
- `spike-02-websocket-reconnection.md`
- Number sequentially within the project

**If called from discovery:** Generate all identified spike specs, then return control to discovery.

**If called mid-construction:** Generate the spike spec in `.pbs-framework/phases/phase-XX/spikes/` instead.

<HARD-GATE>
The human MUST review and approve the spike spec before execution.
If the question is unclear or success criteria are vague, iterate until precise.
Do NOT proceed to execution — that happens in a separate session with pbs-spike-execution.
</HARD-GATE>

## Common Mistakes

- **Question too broad** — "Does the API work?" is not a spike question. What specific behavior are you testing?
- **No measurable success criteria** — "It should be fast" is not a criterion. "Response < 500ms at P95" is.
- **Time box too generous** — 4 hours is the max. If you think it needs more, split into multiple spikes.
- **Missing context references** — the spike session won't have your current conversation. Link to the docs it needs.

## Red Flags

- "This spike needs a full environment setup" → The spike scope is too big. Split it.
- "I'll figure out what to test when I start" → That's not a spike, that's exploration. Define the question first.
- "The whole feature needs spiking" → Break it into specific, independent questions.
- "Let me just run the spike now" → Generate the spec. Execution happens in a separate session.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The question is obvious, no need for a formal spec" | If it's obvious, writing the spec takes 5 minutes. Do it anyway. |
| "I'll remember the context" | The spike session won't have this conversation. Write the context references. |
| "One big spike is easier than three small ones" | One big spike exceeds the time box and answers nothing well. Split. |
| "Success criteria are hard to define" | If you can't define success, you don't understand the question yet. |

## Integration

**Called by:**
- pbs-exploration-discovery — Block 7, for all spikes identified during technical investigation
- pbs-task-execution — when an unknown is hit mid-implementation
- Standalone — anytime a technical question needs a real experiment

**Generates specs for:**
- pbs-spike-execution — executed in separate sessions

**Language:** Write spike specs in the language defined in AGENTS.md `framework_language` field. If not set, match the language of existing `.pbs-framework/` documents.
