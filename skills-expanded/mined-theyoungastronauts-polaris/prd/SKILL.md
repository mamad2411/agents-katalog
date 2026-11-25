---
name: prd
description: "Generate a structured Product Requirements Document from a feature idea."
disable-model-invocation: true
---

# Skill: Product Requirements Document

> Adapted from external PRD and clarification skills

## Overview

Generate a structured, demo-grade PRD from a rough idea, then refine it through systematic questioning. Combines requirement generation with clarification into a single pass.

## When to Use

- After brainstorming, to formalize a design into structured requirements
- When starting from a rough MVP or demo idea that needs product clarity
- Before running `/ux-spec` for UI-heavy features
- When the feature needs explicit UX decisions, not just technical architecture

**Not for:** Backend-only features, pure technical tasks, or ideas that are already well-specified.

## Input

The user provides a rough description — possibly vague, incomplete, or "vibe-level." You must:
- Infer missing details, but clearly label assumptions
- Optimize for a believable demo, not production scale
- Ask one clarifying question max before proceeding, then state assumptions

## Process

### Phase 1: Generate the PRD

Write a PRD with these 7 sections. Use concise, builder-friendly language.

#### 1. One-Sentence Problem

> [User] struggles to [do X] because [reason], resulting in [impact].

Pick the single most demo-worthy problem if multiple exist.

#### 2. Demo Goal

- What must work for this demo to be considered successful
- What outcome the demo should clearly communicate
- Non-goals (what is intentionally out of scope)

#### 3. Target User

Define one primary user role:
- Role / context
- Skill level
- Key constraint (time, knowledge, access, etc.)

Avoid personas or demographics.

#### 4. Core Use Case (Happy Path)

The single most important end-to-end flow:
- Start condition
- Step-by-step flow (numbered)
- End condition

If this flow works, the demo works.

#### 5. Functional Decisions

Required capabilities only. Use this table:

| ID | Function | Notes |
|----|----------|-------|

Rules: phrase as capabilities, no nice-to-haves, keep the list tight.

#### 6. UX Decisions

Explicitly define so nothing is left implicit:
- **Entry point:** How the user starts, what they see first
- **Inputs:** What the user provides
- **Outputs:** What the user receives and in what form
- **Feedback & states:** How the system communicates loading, success, failure, partial results
- **Errors:** What happens on invalid input, system failure, user inaction

#### 7. Data & Logic

- **Inputs:** Where data comes from (user, API, static/mocked, generated)
- **Processing:** High-level logic only (input → transform → output)
- **Outputs:** Where results go (UI only, stored, logged)

### Phase 2: Clarify and Refine

After generating the PRD, ask the user for their preferred depth:

| Depth | Questions | Use When |
|-------|-----------|----------|
| Quick | 5 | Time-constrained, PRD is already solid |
| Medium | 10 | Balanced review of key areas |
| Long | 20 | Comprehensive exploration |
| Ultralong | 35 | Exhaustive deep-dive |

Then ask questions one at a time using AskUserQuestion, adapting after each answer.

**Prioritize questions by impact:**
1. Critical path items — requirements that block other features
2. High-ambiguity areas — vague language, missing acceptance criteria
3. Integration points — interfaces with external systems
4. Edge cases — error handling, boundary conditions
5. Non-functional requirements — performance, accessibility gaps
6. User journey gaps — missing steps, undefined states

**After each answer, reassess:**
- Did the answer reveal new ambiguities? Prioritize those.
- Did it clarify related areas? Skip now-redundant questions.
- Did it contradict earlier answers? Address the conflict.

**Question quality standards:**
- Specific — reference exact PRD sections
- Actionable — answer directly informs a requirement update
- Non-leading — don't suggest the "right" answer
- Singular — one question per turn

### Phase 3: Finalize

After all questions are complete:
1. Update the PRD with clarified requirements
2. List any remaining unresolved ambiguities
3. Suggest priority order for addressing open items

## Output

Write the PRD to `docs/plans/{topic}-prd.md`.

## Done When

A builder could read this PRD, build a demo without guessing, and explain the product clearly to someone else.

## After the PRD

> "PRD is saved. Next steps:
> - **UI-heavy feature:** Run `/ux-spec` to design the user experience before planning.
> - **Technical feature:** Start a new session with the planner agent to break this into implementation phases."

## Guidelines

- Optimize for speed + clarity
- Make reasonable assumptions explicit
- Do NOT include: architecture diagrams, tech stack decisions, pricing/GTM, long explanations

## Common Mistakes

**Overspecifying implementation:** The PRD defines WHAT, not HOW. No tech stack, no architecture.

**Skipping UX decisions (section 6):** The most commonly under-specified section. Entry points, feedback states, and error handling are product decisions, not implementation details.

**Too many functional requirements:** If the list is longer than 8-10 items, you're past MVP. Cut ruthlessly.

**Vague happy path:** "User logs in and does the thing" is not a use case. Number every step.
