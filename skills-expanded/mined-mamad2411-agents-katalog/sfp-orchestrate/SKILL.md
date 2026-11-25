---
name: sfp-orchestrate
description: >
  Run the full Spec-First Protocol pipeline in a single session.
  Orchestrates discover, audit, and refine skills without context
  clearing between phases.
---

# Spec Orchestrate

## Purpose

You are running the **complete Spec-First Protocol pipeline** in a single,
continuous conversation. Instead of invoking each skill separately with
context clearing between phases, this skill orchestrates the full
Discover → Audit → Refine → Lock cycle without interruption.

You will execute each phase by reading and following the instructions in
the corresponding skill file. This orchestrator defines **when** to
transition between phases; the individual skills define **how** each
phase operates.

## When to Use This Skill

Use this orchestrator when:

- The specification scope is moderate (not expected to produce an
  exceptionally long interview or audit trail).
- The context window of the active model is large enough to hold the
  full conversation across all phases.

If context window pressure is a concern, or the specification is very
large, use the individual skills separately instead:
**Spec Discover** → **Spec Audit** → **Spec Refine**, clearing context
between each invocation.

## Pipeline Overview

The protocol follows a structured loop across sequential phases:

0. **Phase 0: Request Triage** – Assess the complexity of the request to
   determine if a full specification is warranted before beginning discovery.
1. **Phase 1: Discovery** – Conduct a structured interview to extract
requirements and compile the initial specification draft.
2. **Phase 2: Audit** – Perform an adversarial review of the specification
draft. If findings/issues exist, transition to Phase 3. If the audit is clean
and the owner approves, transition to Phase 4.
3. **Phase 3: Refinement** – Resolve findings incrementally with the owner,
update discovery notes, and recompile the specification. Once recompiled,
cycle back to Phase 2 (Audit) for verification.
4. **Phase 4: Lock** – Finalize and lock the specification, removing the draft
suffix and cleaning up the working directory.

## Execution Instructions

### Phase 0: Request Triage

Read and follow the Request Triage instructions defined in the
[Spec Discover skill](../sfp-discover/SKILL.md) by cross-reference. Assess the
user's request against the triage criteria:

- **Low complexity + owner accepts → Pipeline complete.** The request was
  answered directly. Do not proceed to discovery.
- **Low complexity + owner overrides → Proceed to Phase 1.** The owner wants a
  full specification.
- **High complexity → Proceed to Phase 1.** Normal protocol flow begins.

---

### Phase 1: Discovery

Read and follow the instructions in the
[Spec Discover skill](../sfp-discover/SKILL.md).

Execute the full discovery process. Note that **Resume Detection** is handled
natively by the discover skill's initialization phase; no additional
orchestrator logic is needed. Follow initialization, structured interview,
Discovery Notes, compilation gate, and specification compilation.

**Phase exit condition:** The project owner has approved compilation and
the draft specification file (`YYYY-MM-DD_<SLUG>_SPEC_DRAFT.md`) has
been written to the spec-specific subdirectory `.sfp/YYYY-MM-DD_<SLUG>/`.

**Transition:** Announce to the project owner that the discovery phase is
complete and the protocol is moving to the audit phase. Then proceed
directly to Phase 2.

---

### Phase 2: Audit

Read and follow the instructions in the
[Spec Audit skill](../sfp-audit/SKILL.md).

Execute the full audit process: load the specification and Discovery
Notes, perform the adversarial review, classify findings, and produce the
Audit Report. Update `.sfp/YYYY-MM-DD_<SLUG>/status.md` with `phase: audit`
and the current timestamp. Increment the `iteration` counter if this is not
the first audit pass.

**Phase exit conditions:**

- **Clean audit (zero blockers) + owner approves →** Proceed to Phase 4
  (Lock). The audit skill handles finalization, immutability, and
  cleanup.
- **Findings exist →** Check the convergence contract (below) before
  proceeding to Phase 3.

### Convergence Contract

The orchestrator enforces iteration-bounded loop control to prevent
unproductive cycling. Read `iteration` and `max_iterations` from
`.sfp/YYYY-MM-DD_<SLUG>/status.md` (default `max_iterations` is **5** if
not set).

```text
WHILE latest audit has blockers AND iteration < max_iterations:
  run Phase 3 (refine) → run Phase 2 (audit) → increment iteration
IF iteration >= max_iterations:
  pause, inform owner that cycling may be unproductive,
  suggest options: continue, halt, or re-discover problematic areas
IF zero blockers:
  request explicit owner approval → proceed to Phase 4 (lock)
```

After each audit-refine cycle, write the updated `iteration` count and
`last_updated` timestamp back to `status.md`. Ensure you preserve the `persona` field
in `status.md` if it exists. This ensures the iteration state and persona context
survive context clears.

If the owner chooses to continue past `max_iterations`, reset the counter
or increase `max_iterations` in `status.md` per the owner's preference.

---

### Phase 3: Refinement

Read and follow the instructions in the
[Spec Refine skill](../sfp-refine/SKILL.md).

Execute the full refinement process: prioritize findings, walk through
each one with the project owner, record decisions, handle scope
expansion, and recompile the specification. Update `status.md` with
`phase: refine` and the current timestamp.

**Phase exit condition:** The updated specification has been recompiled
and written.

**Transition:** Announce to the project owner that refinement is complete
and the protocol is cycling back to audit. Then return to Phase 2.

---

### Phase 4: Lock (Finalization)

This phase is handled entirely by the audit skill's **Finalization Gate**
(executed during Phase 2 when the audit is clean). No separate action is
needed from this orchestrator.

When the audit skill completes finalization:

1. The specification file is renamed and moved (via `mv`) from the spec-specific subdirectory to the `specs/`
   directory (removing `_DRAFT`). Ensure the original file is removed from the `.sfp/...` working directory.
2. The status in `.sfp/YYYY-MM-DD_<SLUG>/status.md` is updated to `phase: locked`.
3. The project owner chooses to **archive** or **delete** the `.sfp/YYYY-MM-DD_<SLUG>/` working directory.
4. If a Persona with `## 7. Downstream Guidance` is active, a **Downstream
   Execution Prompt** is appended to the locked specification.
5. The protocol is complete.

Announce to the project owner that the Spec-First Protocol pipeline is
finished and the locked specification is ready for downstream execution.

## Override Directive

When executing each phase above, **ignore the "Suggested Next Skill"
section** at the end of each individual skill's instructions. Do not
suggest clearing context or starting a fresh session. Phase transitions
are managed by this orchestrator, not by the individual skills.

All other instructions, guardrails, and behavioral rules defined in each
skill must be followed exactly as written.

## Orchestration Guardrails

- **No phase skipping.** Every specification must pass through Discovery
  before Audit, and through Audit before Lock. Do not skip phases even
  if the project owner requests it.
- **Announce transitions.** When moving between phases, explicitly tell the project owner which phase is ending and
  which is beginning. Keep transition announcements brief and visually distinct (e.g.,
  inside a blockquote or separated by blank lines).
- **Preserve all skill guardrails.** The individual skills define
  guardrails (No Solutions, Contradiction Blocker, Scope Creep
  Containment, Zero Solution Design, No Silent Passes, etc.). All of
  these remain in full effect during orchestrated execution.
- **Context monitoring.** If the conversation becomes very long and the
  model's responses begin to degrade in quality (repetition, missed
  details, or inconsistencies), recommend to the project owner that they
  continue with the individual skills in separate sessions, using the
  `.sfp/` working files as the handoff mechanism.
- **Downstream Execution Boundary.** Once the specification is final and
  locked, the pipeline is complete. You must NOT automatically begin planning,
  task creation, or code modifications. You must announce completion and offer
  the project owner the choice of how to proceed. Execution only begins
  after an explicit user request.
- **Succinct Communication & Visual UX.** Ensure all orchestrator responses are direct, highly succinct, and free of
  conversational fluff. Use bullet points and lists to make options or steps easily skimmable.
- **Operational Mode Override.** This skill's workflow governs the session.
  Do not defer to external planning modes, implementation pipelines, or
  other agent operational behaviors that would bypass or substitute this
  skill's defined phases and orchestration structure.
