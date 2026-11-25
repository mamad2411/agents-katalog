---
name: qrspi-questions
audience: team
description: >
  QRSPI Questions phase -- surface what the agent does not know before any research or design
  begins. Use for "/qrspi-questions <feature>", "what don't we know about X", "surface unknowns
  for X", "open technical questions for X". Do NOT use to answer a question or for general Q&A --
  this phase ASKS questions, it does not answer them. Do NOT use for the deprecated RPI workflow.
---

# QRSPI Questions

> "Judge a person by their questions rather than their answers."
> -- Adapted from Voltaire

## Core Philosophy

The Questions phase is the first alignment gate of QRSPI. Before any codebase research or design,
the agent surfaces every unknown as a targeted technical question and STOPS for the human to
answer. A skipped question becomes a wrong assumption; a wrong assumption cascades into wrong
code. This phase makes the unknowns explicit and cheap to correct -- one edit in `questions.md`,
not a rewrite later.

**Non-Negotiable Constraints:**
1. ASK, never answer -- this phase produces questions, not solutions, designs, or research
2. Cover ALL relevant areas -- data model, API contract, UI, integration, auth, testing, edge cases
3. STOP after writing `questions.md` -- the human answers inline before Research begins
4. One feature folder per feature -- every QRSPI artifact co-locates there
5. CONTEXT BUDGET: keep utilization under 40%. At 60%, write `questions.md` with progress and
   tell the user to start a fresh session.

## Workflow

```
PRE-FLIGHT
    [ ] Determine the feature slug (kebab-case) and today's date
    [ ] Feature folder = thoughts/shared/qrspi/YYYY-MM-DD-{slug}/   (create if absent)
    [ ] If an ANSWERED questions.md already exists here, this phase is DONE -> route to /qrspi-research

SURFACE
    Enumerate unknowns across every area the feature could touch:
      data model · API contract · UI/UX · integration points · auth · testing · edge cases · migration
    For each unknown, write a specific, answerable question -- never a vague prompt
    Group questions by area; mark any that BLOCK design as [BLOCKING]

WRITE
    Create thoughts/shared/qrspi/YYYY-MM-DD-{slug}/questions.md
    Use references/questions-template.md
    Set status: awaiting-answers

STOP
    Tell the user: answer the questions inline in questions.md, then start a NEW session
    and run /qrspi-research. Do NOT proceed to Research yourself.
```

**Exit criteria:** `questions.md` written with status `awaiting-answers`; questions cover all
relevant areas with blocking items flagged; user told to answer inline and start a fresh Research
session.

## State Block

```
<qrspi-questions-state>
phase: PRE-FLIGHT | SURFACE | WRITE | STOP | COMPLETE
feature_slug: [kebab-slug]
feature_folder: thoughts/shared/qrspi/YYYY-MM-DD-{slug}/
areas_covered: [data | api | ui | integration | auth | testing | edge-cases | migration]
question_count: [count]
blocking_count: [count]
context_budget: under-40 | approaching-60 | checkpoint-now
status: awaiting-answers | complete
</qrspi-questions-state>
```

## Output Template

See `references/questions-template.md` for the full `questions.md` structure and frontmatter.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `qrspi-research` | Next phase. Consumes the ANSWERED `questions.md` as its neutral topic source. |
| `qrspi-spec` | Downstream. Design decisions trace back to the answers captured here. |
| `spec-coach` | Use instead when you want an interactive design conversation, not a one-shot question dump. |
