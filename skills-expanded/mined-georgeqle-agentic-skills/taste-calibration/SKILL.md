---
name: taste-calibration
description: One-question-at-a-time questioning to calibrate operator-agent alignment on intent, taste, and boundaries
type: planning
version: v0.0
argument-hint: "[rough idea, problem, or partial spec]"
---

# Taste Calibration

Invoke as `$taste-calibration`.

Relentless one-question-at-a-time questioning to build shared understanding before any code or docs.

## Process

1. **Gather context silently.** Read `.agents/project.json`, `README.md`, `AGENTS.md`, `CLAUDE.md`, and any existing `research/` or `specs/` files relevant to the topic when present.
2. **Explore the codebase without mutation.** Gather grounding facts (stack, structure, relevant patterns) using permitted non-mutating exploration tools. If subagents are available and permitted in the active Codex environment, they may be used for independent read-only exploration; otherwise inspect directly. Do not surface exploration results to the user unless they become relevant to a question.
3. **Begin calibration.** Use `$ARGUMENTS` as the seed topic.

### Calibration Rules

- **One question per turn. Always.**
- **Include a recommended answer on every question** ("I'd guess: ...").
- Style: Socratic, taste-seeking, occasionally provocative.
- Example questions:
  - "Would you rather this feel like X or Y?"
  - "What would make this wrong even if it passes tests?"
  - "If I shipped this and you hated it, what would I have gotten wrong?"
  - "What kind of solution would annoy you?"

### Axes to Cover

Before considering termination, cover all three:

- **Intent** -- what are we doing and why
- **Taste** -- how should it feel, what's the quality bar, what's elegant vs hacky
- **Boundaries** -- what's out of scope, what would be wrong

### Termination

Stop calibration when any one condition is met:

- User says done / enough / move on
- Last 2-3 answers were pure confirmations with no corrections or new info
- All three axes covered and alignment is clear

When ready to stop:

1. Announce termination intent and ask for confirmation
2. Summarize shared understanding inline (3-8 bullets covering intent, taste notes, boundaries, and open questions)

## Output

No files. Summary lives in conversation context.

## Constraints

- One question per turn
- Always include recommended answer
- Do not write files
- Do not mutate the repo during context gathering
- No assumptions manifest, no coverage checkpoint, no canonical sections

## Next-Step Routing

After the summary: "Run `$destination-doc` to serialize this alignment."

## Default Shipping Contract

Follow the shared shipping contract convention in CLAUDE.md.

