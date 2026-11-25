---
name: qrspi-spec
audience: team
description: >
  QRSPI Spec phase -- a Design Brain-Dump the human redirects ("brain surgery"), followed by a
  vertically-sliced Structure Outline. Use for "/qrspi-spec <feature>", "design discussion for X",
  "structure outline for X", "spec out X from the research". Do NOT use for an open-ended design
  chat (use spec-coach); this phase consumes research.md and produces an approved spec.md.
---

# QRSPI Spec

> "Plans are worthless, but planning is everything."
> -- Adapted from Dwight D. Eisenhower

## Core Philosophy

The Spec phase turns objective research into an agreed design BEFORE any plan or code exists. It
runs two movements: a **Design Brain-Dump** the human performs "brain surgery" on, then a
**Structure Outline** of signatures and vertical slices. The hard human gate between them is the
point -- catching a wrong approach here costs minutes; catching it in code costs hours. Spec maps
the source workflow's stages 3 (Design Discussion) and 4 (Structure Outline); see
`references/stage-mapping.md`.

**Non-Negotiable Constraints:**
1. RESEARCH-GATED -- never start without an objective `research.md` on disk; never design from memory
2. BRAIN-DUMP FIRST, STOP -- present the Design Brain-Dump and WAIT; do not write the Structure
   Outline until the human approves (`design_approved: true`)
3. VERTICAL SLICES -- the Structure Outline slices work mock-API -> front-end -> database with a
   checkpoint per slice; never organize by horizontal layer
4. SIGNATURES, NOT IMPLEMENTATIONS -- the outline is a "C header file": types and signatures, no bodies
5. CONTEXT BUDGET: keep utilization under 40%. At 60%, write `spec.md` with progress and tell the
   user to start a fresh session.

## Workflow

```
PRE-FLIGHT
    [ ] Locate the feature folder thoughts/shared/qrspi/YYYY-MM-DD-{slug}/
    [ ] Read research.md (status: complete). If absent -> STOP; route the user to /qrspi-research
    [ ] Read the answered questions.md for design intent

BRAIN-DUMP  (source stage 3 -- Design Discussion)
    Write ~200 lines: current state (from research) · desired end state · design decisions & tradeoffs
    Write spec.md with the Brain-Dump only, status: draft, design_approved: false

STOP & LOOP  (the "brain surgery" gate)
    Present the Brain-Dump. WAIT. The human redirects architecture -> revise the Brain-Dump ->
    re-present. Repeat until the human approves. Do NOT write the Structure Outline before approval.

STRUCTURE OUTLINE  (source stage 4 -- only after design_approved: true)
    Add: new/changed type signatures, public function signatures, and high-level phases sliced
    VERTICALLY (mock-API -> front-end -> database), each with a verification checkpoint. No bodies.
    Set status: ready-for-review

REPORT
    Artifact path · slice list · "Review, then start a NEW session and run /qrspi-plan"
```

**Exit criteria:** `spec.md` holds an approved Brain-Dump plus a vertically-sliced Structure
Outline; `status: ready-for-review`; `design_approved: true`; user told to review before `/qrspi-plan`.

## State Block

```
<qrspi-spec-state>
phase: PRE-FLIGHT | BRAIN-DUMP | STOP-LOOP | STRUCTURE-OUTLINE | REPORT | COMPLETE
feature_folder: thoughts/shared/qrspi/YYYY-MM-DD-{slug}/
research_present: true | false      # MUST be true to proceed
design_approved: true | false       # MUST be true before the Structure Outline
brain_dump_revisions: [count]
slices_outlined: [count]
context_budget: under-40 | approaching-60 | checkpoint-now
status: draft | ready-for-review | approved
</qrspi-spec-state>
```

## Output Template

See `references/spec-template.md` for the full `spec.md` structure and frontmatter, and
`references/stage-mapping.md` for the 8-stage source -> 5-phase QRSPI mapping.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `qrspi-research` | Prior phase. Its objective `research.md` is the factual ground for the Brain-Dump. |
| `qrspi-plan` | Next phase. Consumes the approved `spec.md`; refuses to plan without it. |
| `dotnet-vertical-slice` / `python-feature-slice` / `rust-feature-slice` | Stack scaffolders for the vertical slices the Structure Outline defines. |
| `spec-coach` | Use instead for an open-ended interactive design chat; `qrspi-spec` is a gated brain-dump -> outline. |
