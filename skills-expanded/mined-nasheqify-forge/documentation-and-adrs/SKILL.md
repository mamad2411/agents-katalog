---
name: documentation-and-adrs
description: >
  Capture decisions + documentation for people with the why, alternatives, and
  trade-offs — ADRs, README / changelog, API docs. Triggers when an
  architecture/API decision needs capturing (after the decision, or before
  save); NOT for inline code comments, and NOT for text an agent follows
  (CLAUDE.md, AGENTS.md, a skill, a role): use instruction_authoring.
status: active
invocation:
  primary: workflow-step
  secondary: [user-facing]
disable-model-invocation: false
uses: []
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: documentation-and-adrs

## Source

agent-skills at `eb07f19` (MIT License, © 2025 Addy Osmani) and Matt Pocock's skills at `b843cb5` (MIT License, © 2026 Matt Pocock); Forge's register of adopted methods.

## Purpose

Document **decisions**, not just code. The valuable part is
the *why* context: constraints, rejected alternatives,
trade-offs. Code shows *what* was built; docs explain *why
this way* and *what was not chosen*. That's what later humans
and agents need.

## Framework paths (consumer repo)

| Artifact | Canonical location (framework consumer) |
|----------|---------------------------------------------------|
| ADR / architecture decision | `docs/decisions/` (see also the `knowledge_capture` skill, knowledge type **Decision**) |
| Solve / large research | `docs/solve/`, `docs/research/` |
| Architecture notes | `docs/architecture/` |

### ADR path override (project-local adaptation)

Before writing an ADR: read and follow `skills/documentation_and_adrs/adr-writing.md` (ADR path lookup order:
`.adr-config.yaml`, then `docs/STRUCTURE.md`, then the default `docs/decisions/`; it applies to every ADR write, and
a missing override path is created).

## When to use

**Triggered in the `close-bookkeeping` step** of the `build` and `solve`
workflows (`workflows/runbooks/{build,solve}/workflow.yaml`, sub-step (a)
ADR-discipline triple, fed by close-retro's §Stale-Decisions). Fix has no ADR
sub-step. The substantive check is the **ADR-discipline triple** below — the
workflow step triggers the skill; the skill verifies the triple.

**Substantive triggers (independent of the workflow step):**

- Significant architecture decision.
- A choice between competing approaches.
- Public API change or new introduction.
- Feature with user-visible behaviour.
- Onboarding / agent context (the same explanation comes up
  again and again).

**Not:** commenting on obvious code. No docs for throwaway
prototypes without a persistence decision. Not text an agent
follows (`CLAUDE.md`, `AGENTS.md`, a skill, a role or agent
file, a workflow's step text): write or change it with
`instruction_authoring`, which places each rule in the text its
actor has when it acts.

## Architecture Decision Records (ADRs)

### When to write an ADR

#### ADR-discipline triple (required threshold)

Offer / write an ADR **only when all three** conditions are
met:

1. **Hard-to-reverse** — the cost to change again is
   meaningful.
2. **Surprising-without-context** — a future reader (human or
   agent) would ask "why this way? why not X?".
3. **Result-of-real-trade-off** — there were genuine
   alternatives; you chose this one for concrete reasons.

If even **one** of the three is missing → no ADR. Skip is fine
on:
- Ephemeral reasons ("not the focus right now", "not worth the
  effort").
- Self-evident decisions ("obviously the standard way").
- Reversible choices ("can change next week if it's wrong").

Anti-pattern: ADR inflation. Every decision becoming an ADR is
documentation theatre.

An architecture spine's decision (`skills/_protocols/architecture-spine.md`) is a
rule, not a record of why. When its choice also passes the triple, the ADR holds
the why and the decision's `Settled:` line names the ADR.

#### Typical triggers (when the triple holds)

- Framework, library, heavy dependency.
- Data model / schema.
- Auth strategy.
- API form (REST vs events vs ...).
- Build hosting / infra with high switching cost.
- Any decision that is expensive to undo.

#### Close-phase: consume the close_retro retro (build / solve)

At a build or solve close where `close_retro` fired, run the triple over the
retro's **§Stale-Decisions** rows (each = a T0 decision + a T1 invalidator,
`docs/<workflow>/<slug>-retro.md`) instead of re-extracting from raw
artifacts: which of those met hard-to-reverse + surprising-without-context +
result-of-real-trade-off → write the ADR. No retro present, or no qualifying
row → one-line skip. (spec 374 §6.)

### ADR template and lifecycle

Once the triple holds and an ADR is written, and when an ADR is superseded or deprecated: read and follow
`skills/documentation_and_adrs/adr-writing.md` (ADR path lookup order, ADR template with status, date, context,
decision, alternatives considered and consequences; lifecycle PROPOSED → ACCEPTED → SUPERSEDED or DEPRECATED).

## Independent verify-pass (code-mechanics claims)

When an artifact you author names or cites code mechanics (a code symbol, a `file:line`, a hook / check /
engine-field / step name, or a sentence asserting what a subsystem does), before the artifact is treated as
authoritative, and before changing the trigger or the tiers: read and follow
`skills/documentation_and_adrs/verify-pass.md` (why the pass is a default, the observable-signal trigger and its
recorded skip exceptions, the two tiers floor and stakes-escalation per ADR-008, the reviewer contract and verdict
labels, the honest enforcement class).

## Inline documentation

Comment on **why**, not **what** (see upstream good / bad
examples in TS / JS — same logic in Python: magic numbers,
race windows, invariants before call X).

**Gotchas:** non-obvious constraints at the call site;
reference an ADR when the rationale is longer.

## API documentation

- Public APIs: types / docstrings (Python), OpenAPI where
  available.
- Document failure cases and throws — that's part of the
  contract.

## README / changelog

README: a one-paragraph purpose, quickstart, command table,
architecture pointer to ADRs.
Changelog: for releases with Added / Fixed / Changed —
consistent with the consumer-repo convention.

## Documentation for agents

- `CLAUDE.md` / `AGENTS.md` — project rules; written and changed
  with `instruction_authoring`.
- Specs — let them build what is specified.
- ADRs — prevent agents from re-negotiating old decisions.
- Inline gotchas — avoid known traps.

## Common rationalizations (upstream)

| Rationalization | Reality |
|---|---|
| "Code is self-explanatory" | Code shows what, not why or alternatives. |
| "Docs when the API is stable" | The API gets more stable when docs find the design flaw early. |
| "Nobody reads docs" | Agents and you in three months read them. |
| "ADRs are overhead" | A short ADR saves long reviews later. |

## Red flags

- Architecture without written rationale.
- Public API without docs / types.
- README without quickstart.
- Commented-out code instead of deletion.
- TODOs that linger for weeks.
- No ADRs despite heavy decisions.
- Docs that just repeat the code.

## Verification

After documentation work:

- [ ] ADRs for significant architecture decisions (or
  intentionally dropped with a short note).
- [ ] README: quickstart + commands + architecture reference.
- [ ] Public APIs documented with params / return / errors.
- [ ] Gotchas where they apply.
- [ ] No dead commented-out code.
- [ ] Rule files consistent with behaviour; a change to one is
  written with `instruction_authoring`.
- [ ] Code-mechanics claims: load-bearing positive claims carry an
  evidence pointer at write time (Inv 10); on the verify-pass trigger
  (`verify-pass.md` §Independent verify-pass — observable-signal fire, not self-assessed),
  a dispatched cold-start reviewer verified them (floor), escalated to
  multi-perspective when the claim is consequential, before the artifact
  was treated as authoritative.

## Contract

### INPUT

- **Required:** decision context (problem, options,
  constraints) or an existing ADR on update.
- **Optional:** link to a task ID / spec ref.
- **Context:** consumer `docs/STRUCTURE.md`,
  `knowledge_capture` for routing Decision → `docs/decisions/`.

### OUTPUT

**DELIVERS:** an ADR draft or a README / changelog section,
consistent paths.
**DOES NOT DELIVER:** changing production code (→ MCA); fixing
spec content (→ spec_authoring / spec workflow).
**ENABLES:** council / review traceable; agents use the
why context.

### DONE

- ADR has status, date, context, decision, alternatives,
  consequences (or a deliberately shortened variant with a
  reference).
- Paths fit the target repo.

### FAIL

- **Retry:** missing alternatives section on a real choice —
  pull it in.
- **Escalate:** opposite of an existing ADR without a
  supersede chain.
- **Abort:** no write access to the target path (frozen zone)
  — escalate to Buddy.

## Boundary

- No **spec_board** / spec-quality review — only the
  decision / docs artifact.
- No **knowledge_processor** fact stream — here structured
  decisions, not session facts.
- No **testing** — test plans stay with the tester / testing
  skill.

## Anti-patterns

- **NOT** the why in a 20-line comment instead of an ADR on
  hard-to-reverse choices. **INSTEAD** ADR + a one-line
  reference in the code.
- **NOT** an ADR without a rejected alternative. **INSTEAD**
  at least one real alternative with pros / cons.
- **NOT** a README duplicate of the spec. **INSTEAD** the
  README links specs and ADRs.
