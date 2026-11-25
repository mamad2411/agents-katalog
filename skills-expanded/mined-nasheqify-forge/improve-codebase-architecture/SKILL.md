---
name: improve-codebase-architecture
description: >
  Codebase-wide architecture improvement via the deep-modules pattern
  (Ousterhout / Feathers) — find tightly-coupled modules worth consolidating and
  deepening. Use when looking for refactor opportunities or to make the codebase
  more testable + AI-navigable; run periodically (every few days), not diff-centric.
status: active
invocation:
  primary: user-facing
  secondary: [workflow-step]
  trigger_patterns:
    - "improve architecture"
    - "find refactoring opportunities"
    - "deepening opportunities"
    - "consolidate modules"
    - "make testable"
    - "codebase walk"
disable-model-invocation: false
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: improve-codebase-architecture

## Purpose

Surface architectural friction and propose **deepening
opportunities** — refactors that turn shallow modules into
deep modules. The goal is testability + AI-navigability.

Complementary to existing review skills:
- `code_review_board` (L1/L2) is **diff-centric** — review of
  recent changes.
- `architecture_coherence_review` is **cross-spec** — interface
  contracts between specs.
- `improve_codebase_architecture` is **codebase-wide +
  periodic** — an every-few-days friction walk, not
  diff-centric.

Distinct: not "what's wrong with this PR?", but "where does
friction accumulate across the whole codebase, and where would
deepening concentrate complexity?".

## Source

Matt Pocock's skills at `b843cb5` (MIT License, © 2026 Matt Pocock); Forge's register of adopted methods.

## Standalone

Distinct from:
- `code_review_board` (L1/L2) — diff-centric, post-MCA
  return. This skill is codebase-wide + periodic; no diff
  required.
- `architecture_coherence_review` — cross-spec interface
  contracts (≥2 specs). This skill is codebase-wide within a
  single repo, not cross-spec.
- `code-architecture` persona (absorbed into code-review) —
  diff-review architecture axis. This skill finds refactor
  candidates, not review-of-existing-code.
- `frame` — problem-analysis discipline. This skill is the
  codebase-walk discipline (anchored on concrete files +
  modules).

What only this skill delivers:
- **Strict glossary** (module / interface / implementation /
  depth / seam / adapter / leverage / locality) —
  disciplinary vocabulary, not "component / service / API /
  boundary".
- **Deletion test** as an identification tool for shallow
  modules.
- **One-adapter-hypothetical / two-adapters-real rule** as
  anti-YAGNI for abstractions.
- 3-phase loop (explore organic → present numbered candidates
  → grilling loop with the user).
- Inline side effects: update CONTEXT.md / offer an ADR on
  rejection.

## When to call

- The user wants to improve architecture, find refactor
  opportunities, or make the codebase AI-navigable +
  testable.
- Periodic (Pocock recommendation: every-few-days continuous
  refactor).
- After larger feature additions when "it feels messy".
- Before onboarding a new maintainer / agent — friction map
  as an entry tool.
- When tests test implementation instead of behaviour —
  symptom that modules are shallow.

### Do not call for

- PR diff review → `code_review_board` L1 / L2.
- Cross-spec interface check → `architecture_coherence_review`.
- Single-module refactor with a clear plan → direct MCA
  delegation.
- Performance optimization (hot path) → `code-review`
  performance axis.

## Glossary (strict)

Before exploring (Phase 1) and before writing any candidate, proposal or finding in deep-module vocabulary: read and
follow `skills/improve_codebase_architecture/glossary.md` (terms module, interface, implementation, depth, seam,
adapter, leverage, locality; principles including the deletion test and the one-adapter / two-adapters rule;
relationships; rejected framings).

## Process

When starting the codebase walk: read and follow `skills/improve_codebase_architecture/process.md` (Phase 1 organic
exploration with the deletion test; Phase 2 numbered candidates with files, problem, solution, benefits and ADR
conflicts, then the user's pick; Phase 3 grilling loop with inline CONTEXT.md updates and the ADR offer on
rejection).

## Red flags

- A proposal that uses "service" / "component" / "boundary"
  vocabulary instead of the strict glossary (drift).
- A candidate without a files list (too abstract to decide
  on).
- Solution description without locality + leverage
  argumentation.
- A proposal that increases test coverage without changing
  the module (that's symptom treatment, not deep-module).
- Proposing a new seam with only one adapter ("diamond" risk
  — hypothetical seam).
- A proposal that violates its own CONTEXT.md vocabulary
  (domain drift).
- A refactor plan without checking whether tests still test
  the right thing.

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "It's just a small refactor" | Several small refactors without glossary discipline accumulate as vocabulary drift. |
| "Component / service / API is standard language" | Standard isn't precise enough for deep-modules discipline. The strict glossary prevents drift. |
| "We extract that into a util module" | Util is a pattern break. A deep module has behaviour + locality. Util is pass-through. |
| "Several small modules are more testable" | Test against implementation, not behaviour. A deep module with a small interface is easier to test (the interface is the test surface). |
| "We add the adapter prophylactically" | One adapter = hypothetical seam. Two adapters = real seam. Adapter only when something actually varies across it. |
| "Pure function = automatically good" | A pure function without locality (bug hides in HOW it's called) is shallow + leaky. |
| "We use DDD's bounded context" | "Boundary" is overloaded. Say **seam** + **interface** in this skill's vocabulary. |

## Contract

### INPUT
- **Required:** codebase access (repo locally or via Read
  tool).
- **Required:** clear trigger (user request for an
  architecture improvement, or a periodic
  every-few-days run).
- **Optional:** CONTEXT.md with a domain glossary (the skill
  uses it when present, lazy-creates when absent).
- **Optional:** docs/decisions/ or docs/adr/ with ADRs.
- **Context:** this skill (with the strict glossary),
  `skills/_protocols/skill-guardrails.md`,
  `skills/documentation_and_adrs/SKILL.md`.

### OUTPUT
**DELIVERS:**
- Phase 1 friction map (organic, qualitative — where does the
  reviewer experience friction?).
- Phase 2 numbered candidate list (files / problem / solution
  / benefits) with strict-glossary vocabulary.
- Phase 3 grilling conversation per picked candidate with a
  design-tree walk.
- Inline side effects: CONTEXT.md updates / ADRs on rejection
  / cross-ref to api_and_interface_design when interface
  design is needed.

**DOES NOT DELIVER:**
- No implementation of the refactors — only decision
  material.
- No diff review — `code_review_board` is a different
  domain.
- No cross-spec review — `architecture_coherence_review` is
  a different domain.

**ENABLES:**
- A codebase-wide refactor roadmap.
- Vocabulary discipline (anti-drift).
- Clear decisions about seams / adapters / module shapes.
- Testability improvement via the deep-module pattern.

### DONE
- Friction map documented (phase 1 output).
- ≥3 numbered candidates presented in the complete format.
- The user has picked which candidates to explore (phase 2
  gate).
- Grilling loop for picked candidates done with the
  design-tree walk (phase 3).
- CONTEXT.md updates / ADRs / cross-refs done inline.
- Strict glossary used consistently (no "service" /
  "component" / "boundary" drift).

### FAIL
- **Retry:** vocabulary drift detected → rewrite candidates
  with the strict glossary.
- **Escalate:** ≥2 candidates contradict an existing ADR →
  user decision whether to revisit the ADRs.
- **Abort:** no friction found → the codebase is already
  deep + clean. The skill is not needed now; defer to the
  next run.

## See also

- `skills/_protocols/skill-guardrails.md` — anti-patterns.
- `skills/api_and_interface_design/authoring.md` — phase 3
  grilling loop invokes contract-first when interface design
  is needed.
- `skills/documentation_and_adrs/SKILL.md` — ADR format on
  rejection.
- `skills/code_review_board/SKILL.md` — diff counterpart.
- `skills/architecture_coherence_review/SKILL.md` —
  cross-spec counterpart.
- `skills/deprecation_and_migration/SKILL.md` — when a
  refactor retires an old system.
