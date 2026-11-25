---
name: pbs-exploration-brainstorming
description: "Use when starting a new project from scratch, before any technical decisions, to explore the idea through structured sessions and produce a brainstorming synthesis"
---

# Exploration Brainstorming

## Overview

Guide structured brainstorming sessions for an ENTIRE PROJECT to define the problem, solution, scope, risks, and open questions. The output is a synthesis document — not the conversation itself.

**Core principle:** The value is NOT the conversation — it's the synthesis document produced at the end. Conversations are long and messy. The synthesis extracts only what survived.

**Announce at start:** "I'm using the pbs-exploration-brainstorming skill to explore this project idea."

## When to Use

- Starting a new project from scratch — the idea is vague and needs structure
- Exploring a project concept before making ANY technical decisions
- NOT for features in existing codebases — use codebase-familiarization + feature-planning instead

## When NOT to Use

- You already have a clear Project Brief → skip to generating-definitions
- You're adding a feature to an existing codebase → use codebase-familiarization first, then this skill's Lightweight Mode if the feature needs conceptual exploration
- You're making technical decisions (stack, APIs) → that's exploration-discovery, not this

## Input

- **Required:** A project idea or concept (can be vague or well-formed)
- **Optional:** Feature request or ticket (if using Lightweight Mode for an existing codebase)

No documents required — this is the entry point of the framework.

## The Process

### Step 1: Understand the Starting Point

Ask the human to describe their idea. Then assess:
- How clear is the problem? (vague / somewhat clear / well-defined)
- How clear is the solution? (no idea / rough direction / specific vision)
- Is the scope bounded? (open-ended / loosely bounded / well-scoped)

This determines how deep to go in each block.

**Framework language:** If `AGENTS.md` does not already have a `framework_language` field, ask the human:
> "In what language should the framework documents (.pbs-framework/) be written? (e.g., English, Spanish)"

This applies ONLY to `.pbs-framework/` documents (syntheses, specs, roadmaps, closure reports). It does NOT apply to code, READMEs, or project documentation — those follow whatever conventions the project uses.

Record the answer to include in the synthesis so that `pbs-generating-definitions` can set it in AGENTS.md.

### Step 2: Explore the 5 Blocks

Guide the human through 5 thematic blocks. Ask questions **one at a time** — never dump all questions at once. Propose 2-3 approaches when relevant to help the human decide.

For the detailed questionnaire per block, see questionnaire-reference.md.

**Block 1: The Problem**
- What concrete problem are you solving? (2-3 sentences)
- Who has this problem? (specific person, not "everyone")
- How do they solve it today? What's frustrating about current solutions?
- Why does this problem matter?

**Block 2: Proposed Solution**
- What's your solution in one sentence?
- What's the simplest happy path? (minimum viable flow)
- What makes this different from what exists?
- What assumptions must be true for this to work?

**Block 3: Scope and Limits**
- Is this a POC (technical feasibility) or MVP (user validation)?
- What's IN the first cut? What's explicitly OUT?
- What's the simplest proof of success?
- How much time are you willing to invest?

**Block 4: Users and Context**
- Who is the primary user? (role, technical level, motivation)
- In what context do they use this? (desktop, mobile, CLI, automated)
- How often? What output do they expect?

**Block 5: Risks and Open Questions**
- What could go wrong? (technically, conceptually, dependencies)
- What don't you know yet that you NEED to know?
- Are there critical external dependencies?
- What's the plan B if the core idea doesn't work?

### Prompting Techniques

Use these during the conversation to push beyond surface-level thinking:

- **Constraint-based prompting:** Add limits to force creativity. "5 ideas that a solo dev can build in 2 weeks, no backend, offline-first"
- **Unexpected keyword injection:** Introduce concepts from other domains. "What if we applied the concept of 'medical triage' to prioritizing these alerts?"
- **Perspective multiplication:** "How would a Netflix engineer solve this? A 3-person startup? A student?"
- **"What if" framework:** "What if this had to work without internet? What if users could only use it 5 minutes a day?"
- **Devil's advocate:** "Play devil's advocate — what would make this idea fail completely?"

### Step 3: Check Readiness

The brainstorming is ready when:
- [ ] Can describe the problem in 2 sentences
- [ ] Can describe the solution in 2 sentences
- [ ] Clear list of in-scope / out-of-scope
- [ ] Know the success criterion
- [ ] Remaining questions are TECHNICAL (for discovery), not conceptual

If any of these fail → continue exploring the weak areas.

### Step 4: Generate Synthesis

When all readiness signals are met, generate the brainstorming synthesis document.

**Output location:** `.pbs-framework/exploration/brainstorming-synthesis.md`

For the full synthesis template, see questionnaire-reference.md section "Synthesis Template".

The synthesis MUST include:
1. The Problem — description, who has it, current solutions
2. Proposed Solution — one-sentence description, happy path, differentiator
3. Scope — POC/MVP, included/excluded, success criterion
4. Key Assumptions — what must be true, validation status
5. Identified Risks — with impact and mitigation
6. Open Questions for Discovery — technical questions only
7. Explored and Discarded Ideas — brief record to avoid re-exploring dead ends
8. Framework Language — the chosen language for `.pbs-framework/` documents

<HARD-GATE>
The human MUST approve the synthesis before proceeding to discovery.
If the human finds gaps or disagreements, iterate until the synthesis accurately
captures the idea as understood by the human — not as interpreted by the agent.
</HARD-GATE>

### Lightweight Mode (Existing Codebase Features)

When brainstorming a feature for an existing codebase (not a new project):
- Use only Blocks 1-3 (Problem, Solution, Scope)
- Output a `feature-brief.md` instead of a full synthesis
- Skip Blocks 4-5 (users and risks are already known from the codebase)
- Transition to feature-planning instead of exploration-discovery

## Session Structure (Suggested)

```
Session 1: Problem + Solution (Blocks 1-2)
  Duration: 1-2 hours
  Technique: Ask the AI to question YOU instead of you asking it

Session 2: Scope + Users (Blocks 3-4)
  Duration: 1-2 hours
  Technique: Perspective multiplication — explore from different user types

Session 3: Risks + Synthesis (Block 5 + document generation)
  Duration: 1-2 hours
  Technique: Devil's advocate — try to destroy the idea
```

Sessions can be combined or split further depending on complexity.

## Common Mistakes

- **Dumping all questions at once** — ask one at a time. Let the human think and respond before moving on.
- **Accepting the first answer without probing** — use devil's advocate and "what if" to push past surface-level thinking.
- **Jumping to technical decisions** — "What framework?" belongs in discovery. Here we define WHAT, not HOW.
- **Synthesis reads like a transcript** — extract conclusions only. The synthesis is a reference document, not a conversation log.

## Red Flags

- Jumping to technical decisions → "What framework should I use?" belongs in discovery, not here.
- Accepting the first idea without questioning it → If you end with the same idea you started with, you didn't brainstorm.
- All questions answered in one session → For a real project, this usually means the exploration was shallow.
- No open questions for discovery → Every project has technical unknowns. If you found none, you didn't look hard enough.
- Synthesis that reads like a conversation transcript → Extract conclusions only.

## Common Rationalizations

| Excuse | Reality |
|--------|---------|
| "The idea is already clear, skip brainstorming" | If it's clear, the synthesis will be quick. Still write it. |
| "I already know the stack" | Stack belongs in discovery. Here we define WHAT, not HOW. |
| "Risks are obvious, no need to list them" | Obvious risks are the ones that get ignored. List them. |
| "The scope is the whole app" | That's not a scope. Define what's IN and what's OUT. |
| "Let's just start coding and figure it out" | That's vibe coding. This framework exists to prevent it. |

## Integration

**Entry point:** This is the first skill in the framework — no prerequisites.

**Calls next:**
- pbs-exploration-discovery — after human approves the synthesis (standard flow)
- pbs-feature-planning — after lightweight brainstorming for existing codebases
