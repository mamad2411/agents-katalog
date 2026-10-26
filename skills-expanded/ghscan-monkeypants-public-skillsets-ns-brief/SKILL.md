---
name: ns-brief
description: >
  Scope a new consulting skillset. Reads existing practice infrastructure
  and organisation research, then negotiates a brief defining the problem
  domain, target users, value proposition, and success criteria for the
  new methodology. Use when creating a new consulting product line.
metadata:
  author: monkeypants
  version: "0.1"
  skillset: new-skillset
  stage: "1"
  freedom: high
---

# Skillset Brief

You are scoping a **new consulting skillset** — a reusable methodology
that will be implemented as a bounded context package in the
consultamatron practice infrastructure.

## Prerequisites

Check that the client workspace contains:
- `resources/index.md` (shared research gate)

If missing, tell the user to run `org-research` first. The research
provides context about what consulting products are needed.

## Step 1: Understand the landscape

Discover available skillset sources:

```bash
uv run practice source list
```

This shows commons (built-in) and any installed partnership sources.
The operator must decide early whether the new skillset belongs in
the commons or a partnership source, as this determines the
implementation path.

Read the existing practice infrastructure:

```bash
uv run practice skillset list
```

This shows all registered skillsets (implemented and prospectus). The
new skillset must not duplicate an existing one. Understand what gaps
exist.

Read `resources/index.md` and sub-reports to understand:
- What consulting needs the organisation has
- Where existing skillsets fall short
- What methodologies could address unmet needs

## Step 2: Agree on source placement

Ask the operator:

> "Where should this skillset live — **commons** (open, committed to
> the repo), **personal** (operator-private, always available), or a
> **partnership source** (proprietary, per-engagement access control)?"

All three produce a full BC package with SKILLSETS, PRESENTER_FACTORY,
conformance tests, and a presenter. The difference is visibility and
access control:

**Commons** means:
- Lives in `commons/{bc_package}/`
- Committed to the repo, available to all engagements
- Anyone with the repo can use it

**Personal** means:
- Lives in `personal/{bc_package}/`
- Operator-private (gitignored), always available like commons
- No `add-source` needed — personal is included by default

**Partnership** means:
- Lives in `partnerships/{source-slug}/{bc_package}/`
- Only appears in engagements where the source is allowed
- Requires `practice engagement add-source` to enable

Record the decision in the brief under a **Source** heading:
- Source: commons | personal | {partnership-slug}
- If partnership: which partnership repo, does it exist yet?

## Step 3: Propose the brief

Present a skillset brief to the operator:

```markdown
# Skillset Brief — {Skillset Name}

## Problem domain

{What class of problems does this methodology address?
Be specific — "strategic alignment" is too vague,
"mapping technology evolution against business needs" is concrete.}

## Target users

{Who commissions this work? Who consumes the deliverables?
These become the anchors in any eventual Wardley map of the
methodology itself.}

## Value proposition

{Why would a client pay for this? What decisions does it enable
that they cannot make today? One paragraph.}

## Deliverables

{What tangible artifacts does the methodology produce?
List each deliverable with a one-line description.}

## Pipeline sketch

{Initial thoughts on the stages:
1. What does the operator need to know before starting?
2. What is the first meaningful output?
3. What sequence of refinement produces the final deliverable?
Each stage should have a clear gate artifact.}

## Existing art

{What existing methodologies, frameworks, or academic literature
does this draw from? Be specific — cite names, papers, books.}

## Relationship to existing skillsets

{Does this complement, extend, or overlap with existing skillsets?
How would it compose with them in an engagement?}

## Success criteria

{How will we know the skillset is good? Define testable properties:
- What should conformance tests verify?
- What quality attributes matter?
- What would a bad version of this skillset look like?}

## Source

**Placement**: {commons / personal / partnerships/{slug}}
**Rationale**: {why this choice — IP sensitivity, reusability, etc.}

## Scope boundaries

- **Included**: {explicit list}
- **Excluded**: {explicit list}
- **Ambiguous**: {areas needing further research}
```

## Step 4: Negotiate and agree

This is a negotiation. The operator may:
- Narrow or expand the problem domain
- Redefine the value proposition
- Add or remove deliverables
- Restructure the pipeline sketch
- Question whether this needs to be a new skillset at all

Iterate until the operator confirms.

When the operator agrees:
1. If the project is not yet registered, register it:
   ```
   engage/scripts/register-project.sh --client {org} \
     --engagement {engagement} --slug {slug} \
     --skillset "new-skillset" --scope "{agreed scope}"
   ```
2. Write `brief.agreed.md` with the agreed content
3. Record the brief agreement:
   ```
   skillset_engineering/skills/ns-brief/scripts/record-brief-agreed.sh \
     --client {org} --engagement {engagement} --project {slug} \
     --field "Skillset name={proposed name}" \
     --field "Problem domain={domain}"
   ```

## Completion

When `brief.agreed.md` is written, tell the operator the next step is
`ns-research` to research the methodology domain in depth.
