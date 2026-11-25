---
name: spec-authoring
description: >
  Interview-based authoring of a NEW spec or spec section — solution-space
  exploration + intent_chain / intent alignment. Triggers when a NEW spec is
  needed (the code does not exist yet); NOT for syncing a spec to code (use
  retroactive_spec_update) or reviewing one (use spec_board).
status: active
relevant_for: ["main-code-agent"]
invocation:
  primary: workflow-step
  secondary: [user-facing]
disable-model-invocation: false
uses: [frame, spec_board, spec_update]
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: spec-authoring

## Guiding principle

**The spec defines the product. Incidents are fixed in the spec,
not in the code.**

Authoring = product decision act, not documentation. What is in the
spec gets built. When something surfaces during implementation that
the spec doesn't cover: **back to the spec**, don't improvise in
code. Theory (5 primitives, conventions):
`framework/spec-engineering.md`. Detail mechanics (grilling mode,
mediator audit, lessons-table, extended anti-patterns):
`REFERENCE.md`.

## When to call

- **Write a NEW spec** (greenfield).
- **NEW section in existing spec** when the section describes a
  feature that doesn't exist yet (interview for user intent required).
- User intent exists, no structured spec yet.
- Scoping mode (high-level intent → L0-L3) identified the need.
- Specify phase in build workflow.

**Feature additions to existing specs** = `spec_authoring`, not
`retroactive_spec_update`. The feature does not yet exist in code, so
no code evidence; user intent must be clarified via interview. When
unsure: code already exists? Yes → retroactive, no → authoring.

## Do not call for

- **Bring existing spec to as-is code state** → `retroactive_spec_update`.
- **Only review** → `spec_board`.
- **Cross-spec verify after amendment** → `spec_amendment_verification`.

## Phase 1 — Interview

Buddy interviews the user:

- Probe technical and difficult details; question edge cases.
- Surface concerns and trade-offs.
- No obvious questions — ask the hard ones.
- Don't stop until the spec is self-contained.
- **For NEW L1+ specs — bug-class elicitation:** for each draft AC,
  ask "what defect class does this AC guard against? at which test
  level?". Capture noun-phrase answers as `bug_class` rows in the
  §Test-Strategy catalog (Phase 2 checklist item 6). Dedup at
  elicitation; small variations within a bug class do not warrant a
  new row (per `testing/SKILL.md` proportionality rules). When in
  doubt, drop.

Goal: **uncover gaps together that neither saw before**, not "query
the user".

In a build, before the interview settles scope: read and follow
`workflows/runbooks/build/lifecycle.md` (which conditional stages, UX
and architecture, the change needs, and their observable triggers).

**Grilling mode** (one question at a time, recommended-answer-per-
question, walk-the-tree systematic): for foundation / high-stakes /
high-uncertainty / conflict-risk specs. Detail: REFERENCE.md.

### Solution-space exploration (REQUIRED)

Mechanic: `skills/frame/SKILL.md` (SoT). 8 sub-steps run inside the
interview. Especially: reformulate problem, first-principles drill
(`bedrock_drill` on foundation specs), ≥3 fundamentally different
approaches (null option allowed), happy/edge/effort/reversibility
evaluation. Bedrock map (when drilled) flows in as constraint source
— physics/logic axioms = hard constraints, YOUR-CHOICE = soft with
rationale. If a council fires after exploration: council gets frame
approaches as input (no fresh start).

## Phase 2 — Write the spec

When the interview moves to writing the spec, before drafting a new spec or section, and before locking a
recommendation or a named external or internal surface in it: read and follow `skills/spec_authoring/writing.md`
(artifact checklist, REQUIRED on every new spec, items 1–8; verify-before-recommend; integration-surface grounding,
REQUIRED; mediator pass-through audit; the 5 primitives).

## Phase 3 — intent_chain + alignment validation

`intent_chain` format / variants / inheritance rules:
`framework/intent-tree.md` (SoT). Required on delegation (`framework/invariants.md`
invariant 3); optional in direct conversation.

**Intent alignment validation** (MUST — receiving agents): before planning and at a substantive
implementation choice, cite the applicable project intent and the original local
outcome in the existing plan or deviation. Explain how the choice serves both and stop the dependent action
on missing or conflicting intent. Escalate to the commissioning Buddy or the owner of a direct request
(owner: framework/invariants.md §Intent-driven). A direct request can supply its local objective without an
`intent_chain`; use project sources for project work and supplied intent for standalone work.

## Brief authoring (separate skill)

Brief-time MCA delegation artifact lives in `agents/brief-architect.md`,
not here. spec_authoring produces the spec; brief-architect produces
the per-task brief that translates spec → MCA-ready instructions.

## Amendments to existing specs

This skill covers **greenfield specs** and **new sections that need
an interview**. It does NOT cover mechanism-shift / class-rename /
contract-retraction amendments to locked specs — those go through
`brief-architect mode=spec_amendment` when the substantial-amendment
threshold fires.

**Amendment discipline** (pre-edit gate, dispatch threshold, dispatch
shape, greenfield-direct rationale): `_protocols/spec-amendment-discipline.md`.

## Why orchestrator-direct (no fresh-context architect)

Greenfield authoring is run by Buddy (interview + draft), not handed to
a fresh-context architect — deliberately, not as a gap. A fresh-context
architect (`brief-architect`) earns its keep where its value applies:
reading existing code + the spec corpus end-to-end and grounding claims
against them — its `brief`, `spec_amendment`, and `retro_spec_update`
modes each ground against an **existing** artifact. Greenfield authoring
has **no existing artifact to ground against** — the spec is being born —
so that value is moot. And the front-half is an irreducibly interactive
interview (multi-turn, user-in-the-loop); a one-shot context-isolated
agent cannot run it. Author-anchoring — the one real risk of Buddy
drafting what Buddy just interviewed — is caught by the independent
`spec_board` review, not by a redundant drafting handoff. Substantial
amendments to *locked* specs DO get the architect (`brief-architect
mode=spec_amendment`): there the existing spec + code are exactly what
must be ground against. So the "no architect at authoring" asymmetry is
principled — architect = grounding against an existing artifact;
greenfield has none.

## Contract

**INPUT:** user intent, no existing spec file for this scope,
access to `framework/spec-engineering.md` + `docs/specs/Spec header.md`.
Optional: scoping output, frame report.

**OUTPUT:** new spec under `docs/specs/`, SPEC-MAP entry, README
entry, failure-modes section, implementation-surface estimate.

**DOES NOT:** board review (→ `spec_board`), code, implementation,
brief authoring (→ `agents/brief-architect.md`).

**DONE:** spec file with header + content + failure modes +
implementation surface; SPEC-MAP bidirectional; README entry; 5
primitives applied.

**FAIL handling:** interview gaps → more rounds. User cannot answer
fundamental intent questions → ESCALATE back to scoping or intent.md
sharpening.

## Boundary

- No update of existing specs → `spec_update`.
- No board review → `spec_board`.
- No cross-spec verify → `spec_amendment_verification`.

## Anti-patterns

- **NOT** write spec without solution-space exploration. INSTEAD
  `frame` sub-steps 1-8 as required interview part.
- **NOT** treat failure modes as "I'll add later". INSTEAD required
  Phase 2 output.
- **NOT** treat `intent_chain` as checkbox. INSTEAD actively derive
  vision → operational → action.
- **NOT** author multiple new specs in parallel. INSTEAD sequential,
  full interview per spec.
- **NOT** ask "does the spec look complete?" as meta-question.
  INSTEAD identify specific uncertainties; ask sharp questions with
  agent's own recommendation attached.
- **NOT** lock structural-refactor on visible-edge analysis only.
  INSTEAD trace transitive import graph per
  `_protocols/mca-brief-template-verification.md` §Structural-refactor pre-lock
  checklist BEFORE brief locks the decision.
- **NOT** generate two-option questions from handoff/spec disagreement
  without code-grounding first.
- **NOT** assume mediator pass-through; verify it (3-question audit).
- **NOT** name an existing framework surface (enum / contract / gate /
  skill) without grounding it against the live SoT and citing `file:line`;
  a source task's claim about a third surface may be stale and propagates
  verbatim into the new spec.
- **NOT** write a state-bearing mechanism as one bullet per side (entry
  recipe, exit recipe, undo paragraph) spread over several specs.
  INSTEAD one `§Mechanism-Lifecycle` matrix in the owning spec, every
  cell filled, other specs pointing at it
  (`_protocols/mechanism-model.md`). Because: per-side prose is reviewed
  per side; the defects live in the cells nobody wrote.

Extended anti-patterns + Lessons-table (full failure-shape +
discipline-rule rows): REFERENCE.md.
