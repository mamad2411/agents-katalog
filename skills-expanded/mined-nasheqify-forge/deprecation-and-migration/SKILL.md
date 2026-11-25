---
name: deprecation-and-migration
description: >
  Deprecation and migration discipline (code-as-liability; strangler / adapter /
  feature-flag patterns; churn + zombie-code handling). Use when removing an old
  system / API / feature, migrating users to a new implementation, or deciding
  maintain vs sunset.
status: active
invocation:
  primary: user-facing
  secondary: [workflow-step]
  trigger_patterns:
    - "deprecate"
    - "sunset"
    - "remove old system"
    - "migration plan"
    - "zombie code"
    - "altlasten"
    - "entfernen"
disable-model-invocation: false
---

Read and follow `framework/work-principle.md` before taking up work.
Resolve this reference against the framework root; retain the consumer CWD.


# Skill: deprecation-and-migration

## Purpose

Code is liability, not asset. Every line of code carries
maintenance cost — fixing bugs, updating dependencies,
applying security patches, onboarding new engineers.
Deprecation is the discipline of removing code that no longer
earns its effort. Migration is the process of moving users
safely from old to new.

Most engineering organizations are good at building. Few are
good at removing. This skill closes the gap.

Formalizes the existing STALE-CLEANUP invariant (`framework/invariants.md`
§5) at the skill level — when / how to deprecate is a
methodology question, not just a cleanup sweep.

## Source

agent-skills at `eb07f19` (MIT License, © 2025 Addy Osmani); Forge's register of adopted methods.

## Standalone

Distinct from:
- `skills/_protocols/skill-guardrails.md` —
  skill-specific anti-patterns, not the deprecation
  lifecycle.
- `framework/skill-anatomy.md` §Consolidation mechanic —
  describes the skill-as-mode-absorbed mechanism.
  deprecation-and-migration is broader (also code, APIs,
  modules, whole systems — not just skills).
- STALE-CLEANUP invariant (`framework/invariants.md` §5) — the same-commit
  ref-cleanup discipline Buddy applies on removal. This
  skill is the **decision discipline** (when / how) behind
  that cleanup.

What only this skill delivers:
- Deprecation-decision framework (5 questions before
  deprecation start).
- Compulsory-vs-advisory classification with trigger
  conditions.
- Migration process (build replacement first → announce →
  incremental → remove).
- 3 migration patterns (strangler / adapter / feature flag).
- The churn rule (owner responsibility for migration).
- Zombie-code diagnosis + treatment.

## When to call

- Replace an old system / API / library with a new one.
- Sunsetting a feature that is no longer needed.
- Consolidating duplicate implementations.
- Removing dead code that no one owns but everyone depends
  on (zombie code).
- Lifecycle planning for a new system (deprecation planning
  starts at design time).
- Decision: maintain a legacy system or invest in
  migration?

### Migration-needed check (MUST before any "no migration needed")

Run whenever a change touches the shape of persisted data (a stored
payload, event, row, document or file format) — including a spec or
design decision that concludes "no migration needed". Judge the **read
path**, not only the DDL:

1. **Name the decode path.** Where is stored data read back, and is it
   re-validated strictly (`extra=forbid`, closed literal / enum types,
   required fields)? A JSON/JSONB column with no CHECK or index on the
   field can still break every read through a strict decoder.
2. **Classify the change.** Field removal, rename, literal / enum
   narrowing or a newly required field against a strict decoder =
   pre-change rows fail to decode.
3. **Pick exactly one and write it into the decision:** a
   `schema_version` bump with a decoder for the old version; an
   upcast on read; or a stated **empty-store precondition** naming
   the trigger that ends it (e.g. "first real append in production")
   and the task or gate that must migrate before that trigger.

"No migration: no column reads the field" without step 1 is not a
valid conclusion. A real doubt here is an L2 trigger for the code
board (`skills/code_review_board/SKILL.md` §1.1).

### Do not call for

- Pure skill-as-mode consolidation (e.g. ux_review →
  spec_board mode=ux) →
  `framework/skill-anatomy.md` §Consolidation mechanic.
- Mechanical STALE-CLEANUP after a rename → the
  stale-cleanup sweep (invariant 5).

## Process

### Phases 1, 2 and 5: deciding whether and how to deprecate

Before starting a deprecation, when deciding whether to maintain a system or sunset it, and when code shows zombie
signs: read and follow `skills/deprecation_and_migration/decision.md` (phase 1: the five mandatory decision questions;
phase 2: compulsory vs advisory; phase 5: zombie-code signs and the binary response).

### Phases 3–4: migrating and removing the old system

Once the deprecation decision stands, before building the replacement and announcing it, while migrating consumers,
when choosing a migration pattern, and before removing the old system: read and follow
`skills/deprecation_and_migration/migration.md` (phase 3 steps 1–4: build the replacement, announce + document with
the deprecation-notice template, migrate incrementally under the churn rule, remove the old system with the
STALE-CLEANUP inventory-flip; phase 4: strangler, adapter and feature-flag migration patterns).

## Red flags

- A deprecated system without an available replacement.
- A deprecation announcement without migration tooling or
  documentation.
- "Soft" deprecation that has been advisory for years
  without progress.
- Zombie code without an owner but with active consumers.
- New features added to a deprecated system (instead of
  investment in the replacement).
- Deprecation without measuring current usage.
- Removing code without verifying zero active consumers.
- Violating the STALE-CLEANUP invariant (refs in active
  files survive after removal).

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "It still works, why remove it?" | Working code that nobody maintains accumulates security debt + complexity. Maintenance cost grows silently. |
| "Maybe we'll need it again" | If we need it again, it can be rebuilt. "Just in case" costs more than rebuild. |
| "Migration is too expensive" | Compare migration cost vs ongoing maintenance cost over 2-3 years. Migration is usually cheaper long-term. |
| "We'll deprecate after the new thing is finished" | Deprecation planning starts at design time. When the new thing is finished you'll have other priorities. **Plan now.** |
| "Users will migrate themselves" | They won't. Provide tooling + documentation + incentives — or do the migration yourself (churn rule). |
| "We can maintain both indefinitely" | Two systems doing the same thing = double the maintenance + testing + documentation + onboarding cost. |
| "A stub file with a pointer is enough" | Pattern break against the user mantra "no altlasten" — on clear consolidation, delete, don't archive. A stub only when there's historic value + non-trivial lookup need. |

## Contract

### INPUT
- **Required:** clearly identified subject (system / API /
  module / feature) to be deprecated.
- **Required:** answers to the 5 decision questions (phase
  1) — all 5 deprecation-pro.
- **Required:** a replacement exists or is clearly planned.
- **Optional:** consumer list (phase 3 step 1 — who uses
  it).
- **Optional:** migration-tooling idea (required on
  compulsory).
- **Context:** `framework/invariants.md` §stale-cleanup invariant 5,
  `framework/skill-anatomy.md` §consolidation mechanic
  (skill-specific),
  `skills/documentation_and_adrs/SKILL.md` (ADR for a
  substantial deprecation decision).

### OUTPUT
**DELIVERS:**
- Deprecation decision documented (5 answers).
- Compulsory-vs-advisory classification.
- Migration plan with the chosen pattern (strangler /
  adapter / feature flag).
- Deprecation notice (status / replacement / removal date /
  reason / migration guide).
- Removed code + tests + docs + config (at the end).
- STALE-CLEANUP complete (every active ref cleaned).
- ADR on a substantial deprecation decision.

**DOES NOT DELIVER:**
- No pure STALE-cleanup sweep — that's invariant 5.
- No skill-as-mode consolidation in detail — see
  `framework/skill-anatomy.md` §consolidation mechanic.

**ENABLES:**
- Clean framework without zombie code.
- Safe migration without data loss or user disruption.
- Reduced maintenance cost long-term.

### DONE
- Replacement production-proven, every critical use case
  covered.
- Migration guide exists with concrete steps + examples.
- All active consumers migrated (verified by metrics /
  logs / grep).
- Old code + tests + docs + config completely removed.
- No references to the deprecated system in the codebase —
  completeness proven by inventory-flip (claim of mechanism vs
  closed real inventory), not name-grep alone (`migration.md` §Phase 3 Step 4).
- Deprecation notices themselves removed (they served
  their purpose).
- STALE-CLEANUP complete in the removal commit.
- ADR written if applicable.

### FAIL
- **Retry:** migration of a consumer fails → don't advance
  the strangler phase further; fix, then continue.
- **Escalate:** the 5 decision questions don't clearly
  yield deprecation-pro → user discussion whether the
  system should really go. Solution expert / council on a
  substantial question.
- **Abort:** the replacement isn't production-proven →
  repeat phase 1, harden the replacement first.

## See also

- `framework/invariants.md` invariant §5 STALE-CLEANUP — the same-commit
  ref-cleanup discipline.
- `skills/shipping_and_launch/rollout.md` phase 2
  feature-flag strategy — same mechanism, pre-migration use
  case.
- `framework/skill-anatomy.md` §Consolidation mechanics —
  skill-specific sub-variant.
- `skills/documentation_and_adrs/SKILL.md` — writing an ADR
  for substantial deprecation decisions.
- `skills/_protocols/skill-guardrails.md` — anti-patterns.
