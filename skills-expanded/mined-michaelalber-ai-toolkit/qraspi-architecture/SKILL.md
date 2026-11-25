---
name: qraspi-architecture
audience: team
description: >
  QRASPI Architecture phase — locks the path-dependent decisions for a NEW system as MADR ADRs
  (with alternatives), draws the C4 Context + Container in Mermaid, and specifies required
  fitness functions. Use for '/qraspi-architecture <project>', 'write the ADRs for new X', 'what
  architecture for new X', 'lock the stack decisions for X'. Not for critiquing an EXISTING
  system (architecture-review), retrospective ADR journaling (architecture-journal), a feature
  in an existing codebase (qrspi-spec), or the deprecated RPI workflow.
---

# QRASPI Architecture

> "Architecture represents the significant decisions, where significance is measured by cost of change."
> -- Adapted from Grady Booch

## Core Philosophy

The Architecture phase is where greenfield finally **chooses**. Research mapped the landscape and
refused to pick; Architecture locks the path-dependent decisions -- the ones expensive to reverse
once code exists -- as **MADR ADRs with real alternatives**, then makes each decision *executable* by
specifying the fitness function that will gate it in CI. The failure mode this phase prevents is the
**fait-accompli ADR**: a record that rationalizes a decision already made instead of weighing options
the human can redirect. So every ADR carries >= 2 considered options, is written `proposed`,
presented, and set `accepted` only after the human aligns -- the greenfield analog of `qrspi-spec`'s
"brain surgery" gate. An ADR that names a measurable quality attribute without a fitness function is
an intention with no teeth; this phase requires both. For high-domain-complexity systems an optional
pre-step builds a domain glossary in `CONTEXT.md` (use upstream mattpocock/skills domain-modeling if
installed; no 7th phase -- it folds in here).

**Non-Negotiable Constraints:**
1. RESEARCH-GATED -- never start without `research.md` (status: complete) on disk; never design from
   memory. The ADR alternatives come from research's "Options on the table".
2. ADRs WITH ALTERNATIVES -- every ADR is MADR format with >= 2 Considered Options; a fait-accompli
   ADR (< 2 real options) cannot reach WRITE
3. ALIGN BEFORE LOCK -- write ADRs `status: proposed`, STOP and present, loop on the human's
   redirection; set `status: accepted` only after approval (`adrs_aligned: true`)
4. FITNESS FUNCTIONS REQUIRED -- every accepted ADR naming a measurable quality attribute gets
   >= 1 specified fitness function; `fitness_functions_specified` MUST be > 0 (authoring delegates
   to the `fitness-functions` primitive, which lands them as CI gates in Skeleton)
5. CONTEXT BUDGET: keep utilization under 40%. At 60%, write `architecture.md` with progress and
   tell the user to start a fresh session.

## Workflow

```
PRE-FLIGHT
    [ ] Locate the project folder thoughts/shared/qraspi/YYYY-MM-DD-{slug}/
    [ ] Read research.md (status: complete). If absent -> STOP; route the user to /qraspi-research
    [ ] Read the answered questions.md for quality attributes + hard constraints
    [ ] OPTIONAL: high domain complexity? -> domain glossary pass -> CONTEXT.md the ADRs reference
    [ ] Determine adr_dir: default <target-repo>/docs/adr/ (overridable via --adr-dir / frontmatter)

DRAFT  (decisions as PROPOSED ADRs)
    For each path-dependent decision behind research's "Options on the table":
      write a MADR ADR (references/adr-template.md), NNNN-kebab-title.md, >= 2 Considered Options,
      status: proposed
    Draft architecture.md: summary + C4 Context & Container in Mermaid (references/c4-conventions.md)
      + a fitness-function spec index (references/fitness-spec.md)

ALIGN & LOOP  (the "brain surgery" gate -- mirrors qrspi-spec)
    Present the proposed ADR set + C4. STOP. The human redirects -> revise -> re-present.
    Loop until approved. Only THEN set each ADR status: accepted; adrs_aligned: true.

FITNESS SPEC  (required output)
    For every accepted ADR naming a measurable quality attribute, specify >= 1 fitness function in
    architecture.md (references/fitness-spec.md): attribute, threshold, candidate tool, ADR id.
    Authoring/wiring is the fitness-functions primitive's job in Skeleton; this writes the contract.
    fitness_functions_specified > 0.

WRITE
    <target>/docs/adr/NNNN-*.md   (accepted ADRs -- live in the target repo, QRSPI reads them later)
    thoughts/shared/qraspi/YYYY-MM-DD-{slug}/architecture.md   (status: complete; INDEXES the ADRs)

REPORT
    architecture.md path · accepted ADR list · C4 levels drawn · fitness functions specified ·
    "Review, then start a NEW session and run /qraspi-skeleton"
```

**Exit criteria:** every ADR is MADR format with >= 2 alternatives and `status: accepted`;
`adrs_aligned: true`; C4 Context + Container drawn in Mermaid; `architecture.md` written and indexes
the accepted ADRs; `fitness_functions_specified > 0`; user told to review before `/qraspi-skeleton`.

## State Block

```
<qraspi-architecture-state>
phase: PRE-FLIGHT | DRAFT | ALIGN-LOOP | FITNESS-SPEC | WRITE | REPORT | COMPLETE
project_folder: thoughts/shared/qraspi/YYYY-MM-DD-{slug}/
adr_dir: [target]/docs/adr/
research_present: true | false          # MUST be true to proceed
domain_model_invoked: true | false      # optional -- high domain complexity only
adrs_drafted: [count]
adrs_min_alternatives_met: true | false # every ADR has >= 2 Considered Options
adrs_aligned: true | false              # MUST be true before any ADR is set accepted
c4_levels: [Context, Container]
fitness_functions_specified: [count]    # MUST be > 0 to COMPLETE
alignment_revisions: [count]
context_budget: under-40 | approaching-60 | checkpoint-now
status: in_progress | complete
</qraspi-architecture-state>
```

## Output Template

See `references/adr-template.md` for the MADR ADR structure (Considered Options required),
`references/c4-conventions.md` for the Mermaid `C4Context`/`C4Container` conventions and the
`architecture.md` summary shape, and `references/fitness-spec.md` for the fitness-function spec table
that hands off to the `fitness-functions` primitive.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `qraspi-research` | Prior phase. Its `research.md` "Options on the table" are the alternatives input for the ADRs. |
| `qraspi-skeleton` | Next phase. Consumes `architecture.md` + the accepted ADRs; lands the specified fitness functions as CI gates. |
| `fitness-functions` | Authors the fitness functions this phase specifies (it owns the per-stack tooling); Skeleton wires them as CI gates. |
| `architecture-journal` | Reusable ADR + retrospective skill; this phase uses a MADR variant (`references/adr-template.md`) for the greenfield decision lock. |
| `qrspi-spec` | Brownfield sibling's design gate. Architecture is the greenfield analog -- ADRs-with-alternatives instead of a design brain-dump. |
