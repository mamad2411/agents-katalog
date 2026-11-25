---
name: qraspi-questions
audience: team
description: >
  QRASPI Questions phase -- surface what is unknown about a NEW system before any research,
  architecture, or skeleton begins. Use for "/qraspi-questions <project>", "new project from
  scratch", "greenfield X", "questions for a brand-new system". Do NOT use for QRSPI (an EXISTING
  codebase / adding a feature) -- that routes to qrspi-questions. Do NOT use for the deprecated RPI
  workflow.
---

# QRASPI Questions

> "If you do not know how to ask the right question, you discover nothing."
> -- W. Edwards Deming

## Core Philosophy

The Questions phase is the first alignment gate of QRASPI's greenfield (V0/V1) path. Before any
domain research, architecture, or skeleton, the agent surfaces every unknown about the new system
as a targeted question and STOPS for the human to answer. Greenfield has no codebase to constrain
the answers, so the danger is a *narrow* question set that silently commits the design to one
shape. This phase defends against that with a **fixed six-category checklist**: it enumerates a
question for every greenfield concern whether or not the user named it. A skipped category becomes
an unexamined assumption that cascades into the ADRs; surfacing it here costs one edit in
`questions.md`, not an architecture rewrite later.

**Non-Negotiable Constraints:**
1. ASK, never answer -- this phase produces questions, not solutions, research, or architecture
2. Cover ALL SIX greenfield categories -- functional scope · quality attributes (the -ilities) ·
   integration / external systems · compliance / regulatory · deployment / runtime target ·
   data & domain model -- enumerate a question for every category, named by the user or not
3. STOP after writing `questions.md` -- the human answers inline before Research begins
4. One project folder per project -- every QRASPI artifact co-locates there
5. CONTEXT BUDGET: keep utilization under 40%. At 60%, write `questions.md` with progress and
   tell the user to start a fresh session.

## Workflow

```
PRE-FLIGHT
    [ ] Determine the project slug (kebab-case) and today's date
    [ ] Project folder = thoughts/shared/qraspi/YYYY-MM-DD-{slug}/   (create if absent)
    [ ] If an ANSWERED questions.md already exists here, this phase is DONE -> route to /qraspi-research

SURFACE
    Walk the SIX greenfield categories in order; for EACH, write at least one specific,
    answerable question -- never a vague prompt, never skip a category:
      functional scope · quality attributes (-ilities) · integration / external systems ·
      compliance / regulatory · deployment / runtime target · data & domain model
    Mark any question that BLOCKS architecture as [BLOCKING]

WRITE
    Create thoughts/shared/qraspi/YYYY-MM-DD-{slug}/questions.md
    Use references/questions-template.md
    Set status: awaiting-answers

STOP
    Tell the user: answer the questions inline in questions.md, then start a NEW session
    and run /qraspi-research. Do NOT proceed to Research yourself.
```

**Exit criteria:** `questions.md` written with status `awaiting-answers`; all six greenfield
categories carry at least one question with blocking items flagged; user told to answer inline and
start a fresh Research session.

## State Block

```
<qraspi-questions-state>
phase: PRE-FLIGHT | SURFACE | WRITE | STOP | COMPLETE
project_slug: [kebab-slug]
project_folder: thoughts/shared/qraspi/YYYY-MM-DD-{slug}/
areas_covered: [functional | quality-attributes | integration | compliance | deployment | domain]
                # all six MUST be present before WRITE
question_count: [count]
blocking_count: [count]
context_budget: under-40 | approaching-60 | checkpoint-now
status: awaiting-answers | complete
</qraspi-questions-state>
```

## Output Template

See `references/questions-template.md` for the full `questions.md` structure and frontmatter.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `qraspi-research` | Next phase. Consumes the ANSWERED `questions.md` to scope the landscape map. |
| `qraspi-architecture` | Downstream. Every ADR's decision traces back to an answer captured here. |
| `qrspi-questions` | Brownfield sibling. Use it instead when the system already EXISTS and you are adding a feature. |
| `spec-coach` | Use instead when you want an interactive design conversation, not a one-shot question dump. |
