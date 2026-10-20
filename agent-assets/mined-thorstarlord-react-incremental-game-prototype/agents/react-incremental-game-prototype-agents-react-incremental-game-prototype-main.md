# Agent Operating Policy — Campaign One / 1.0

**Status:** CURRENT AUTHORITY for coding-agent behavior  
**Applies to:** repository analysis, implementation, review, qualification, and handoff work

## Purpose

This file defines how coding agents should turn repository evidence into useful work without inventing scope or confusing evidence classes.

The governing distinction is:

> **Missing human evidence limits the claims this repository may make; it does not by itself prohibit useful repository-answerable work.**

Governance exists to improve the product and preserve justified scope. Governance is not itself the product objective. When a procedural rule blocks useful repository-answerable work without protecting a concrete product, safety, release, or evidence requirement, reconcile the rule instead of treating paralysis as success.

## Current objective

Campaign One is now **FEATURE_COMPLETE / HUMAN-UNVALIDATED** under `specification/Technical/FeatureCompleteResult.md`.

The active sequence is:

```text
FEATURE_COMPLETE
-> Beta convergence / human validation
-> bounded tuning / accessibility / presentation / reliability repairs
-> BETA_PASS
-> RC qualification
```

Historical Alpha, Content Alpha, GC, Candidate B, Candidate A, Candidate C, and deterministic Beta-readiness results remain valid evidence. Do not invent another feature-construction package by inertia. Human Beta is now the active maturity lane for actual player-experience claims and eventual `BETA_PASS`; deterministic, heuristic, synthetic, accessibility, reliability, presentation, pacing, balance, and persistence findings may still justify bounded repairs to the existing feature-complete game.

## Required reading order

For a new coding-agent session:

1. `AGENTS.md` — agent behavior and evidence-to-authority rules.
2. `STATUS.md` — current repository state, maturity, and active lanes.
3. `docs/CURRENT.md` — documentation classification and conflict resolution.
4. `HANDOFF.md` — current re-entry summary when present.
5. `specification/GameCompletionDefinition.md` — finished Campaign One / 1.0.
6. `specification/Features/FeatureScopeMatrix.md` — core, supporting, deferred, and cut scope.
7. `specification/Progression/GameProgressionArc.md` and `specification/Narrative/CampaignArchitecture.md`.
8. `specification/Technical/GameCompletionRoadmap.md`.
9. the relevant Alpha/Beta/Release contract.
10. `RUNBOOK.md` and the affected current domain contracts/results.

`CLAUDE.md` is a thin Claude adapter to this file. Do not maintain a second Claude-specific policy.

## Evidence classes

Keep evidence provenance explicit.

### DETERMINISTIC_FINDING

Examples: tests, static analysis, reproducible runtime behavior, browser automation, save/recovery checks, performance measurements.

May establish implementation behavior within the evidence actually exercised.

### HEURISTIC_FINDING

Examples: UX inspection, information hierarchy review, terminology inconsistency, pacing analysis, accessibility review, design contradiction, release-surface inspection.

May identify plausible defects or risks and may justify bounded repairs inside the already-authorized 1.0 scope.

### SYNTHETIC_FINDING

Examples: automated or model-assisted playthroughs, state-space exploration, scripted browser journeys, simulated product review.

May expose reproducible friction or risk and may justify bounded repairs. It does **not** become evidence about what real players actually understood, enjoyed, preferred, or retained.

### HUMAN_FINDING

Evidence from genuine external/fresh participants under the current Beta evidence procedure.

May support actual player-experience claims within the limits of the recorded sessions.

## Core evidence-to-authority rule

```text
missing human evidence
!= repository work forbidden

missing human evidence
= human-experience claims remain unproven
```

Evidence type controls the strength of the claim, not whether all useful work stops.

A bounded repair may therefore be justified by deterministic, heuristic, synthetic, accessibility, reliability, presentation, pacing, balance, or human evidence. Preserve the evidence class in the resulting record.

## Repository-answerable work agents may perform

Within the existing Campaign One / 1.0 scope, agents may proactively:

- perform end-to-end heuristic UX/product review;
- run synthetic/browser playthroughs;
- inspect navigation and discoverability;
- inspect state and causal legibility;
- analyze progression pacing, grind, economy pressure, and delegation timing;
- inspect balance contradictions using repository evidence;
- improve accessibility and input behavior;
- improve presentation, terminology, and visual hierarchy;
- improve performance and reliability;
- harden save/load/recovery/import-export behavior;
- remove prototype/debug residue from normal player surfaces;
- repair concrete architecture/integration defects that block the current product;
- inspect an alleged missing feature role only when a concrete finding may falsify the recorded `FEATURE_COMPLETE` contract;
- improve release qualification and deployment readiness;
- repair documentation/governance drift that can misroute future work.

Prefer the smallest **sufficient** intervention that resolves the evidenced Beta/release problem inside existing authorities. Do not reopen feature-depth search merely because broader implementation is possible. Add deterministic regression coverage where the repaired behavior is testable.

## Scope lock — not a repository freeze

Do not create work merely to keep an agent busy.

The following remain outside Campaign One / 1.0 unless current authority is explicitly revised:

- separate generic Skills/skill-tree;
- generic Crafting;
- general Inventory/Equipment economy;
- duplicate Saves authority;
- generalized ChapterEngine or narrative DSL;
- autonomous irreversible Copy planning;
- offline narrative/social/world decisions;
- Chapters 8+, interplanetary continuation, New Game+, or endless endgame;
- generalized simulation/live-service infrastructure.

Do not rewrite or invalidate closed M4–M26, GC-01–GC-12, or B/A/C evidence. Historical milestone closure remains evidence; `FEATURE_COMPLETE` is the current construction stop. A core feature may be reopened only when a concrete finding demonstrates that its required Campaign One role is actually absent or false, or when owner authority explicitly revises scope.

## Work-selection rule

Before a package, answer:

1. What named Beta/Release requirement or concrete finding justifies work now?
2. What evidence class supports the finding?
3. Which existing Campaign One authority owns the behavior?
4. What is the smallest intervention that resolves the finding without expanding feature scope?
5. What positive and rejection evidence will show the intervention works?
6. What persistence/browser/accessibility/recovery implications exist?
7. What claim will be stronger afterward, and what stronger claim remains unproven?
8. What is the stop condition?
9. Does this finding actually falsify `FEATURE_COMPLETE`? If not, do not reopen feature construction.

Technical possibility alone is not authorization. Evidence-backed **Beta convergence and release hardening inside the locked product boundary** is.

## Human Beta and release policy

The current human evidence floor remains:

- at least 5 accepted fresh-player first sessions;
- at least 3 accepted external beginning-to-ending fresh-save playthroughs;
- resolution or explicit acceptance of recurring severe findings;
- exact build/browser/session provenance.

Non-human evidence must never be relabeled as satisfying that floor.

Under current authority:

```text
CONTENT_ALPHA + TECHNICAL_BETA_READY
= retained historical integration/readiness evidence

FEATURE_COMPLETE
= recorded / HUMAN-UNVALIDATED

current frontier
= BETA_CONVERGENCE / HUMAN_VALIDATION

BETA_PASS
= not yet; still requires the human evidence contract

RC entry
= downstream; remains blocked until BETA_PASS under the current release contract
```

Changing those promotion requirements is an owner/product-policy decision. Improving the existing game while they remain open is not.

## Stop conditions

Stop repository work only when at least one is true:

- no bounded repository-answerable hardening or release-readiness improvement has material expected value;
- the next change would require unauthorized product-scope expansion;
- the next decision is genuinely owner-reserved;
- the next required evidence is genuinely external and there is no independent repository-answerable hardening work worth doing;
- an infrastructure/credential/external blocker cannot be resolved within current authority;
- the relevant requirement is already satisfied and additional work would be polishing beyond meaningful expected value.

**Absence of human evidence alone is not a universal stop condition.**

## External/tool blocker freshness

Treat an external, infrastructure, credential, or tool-capability blocker as an observation about a specific execution surface, not as a timeless repository fact.

Before stopping on such a blocker, when the check is safe and cheap:

1. re-verify the currently available capability rather than relying only on an older issue, handoff, or prior-session limitation;
2. record the observed surface and evidence precisely: actor/integration, operation attempted, result, and relevant date or candidate;
3. distinguish **resource state** from **observation authority** — for example, "rulesets list is empty" is evidence about rulesets, while a `403` on branch protection means protection state is **unknown to this integration**, not absent;
4. distinguish read capability from write capability; successful inspection does not imply mutation authority, and failed inspection does not prove the repository resource is unconfigured;
5. if the blocker is now resolvable within current authority, continue instead of preserving a stale stop boundary;
6. if it remains blocked, preserve the claim ceiling, record fresh evidence in the canonical issue/result when useful, and still check for independently warranted repository work.

```text
previously unavailable
!= currently unavailable

cannot observe
!= does not exist

can observe
!= can mutate

external blocker
= capability-scoped + evidence-dated
```

Do not repeatedly probe expensive or sensitive external surfaces when no capability or state has changed. Freshness checking exists to prevent stale blocker inheritance, not to create polling work.

## Maturity-transition closure protocol

When the repository crosses a named maturity or strategic-stage boundary such as:

```text
FEATURE_COMPLETION -> BETA_CONVERGENCE
BETA_PASS -> RC_QUALIFICATION
RC_QUALIFIED -> 1.0_PROMOTION
```

treat the transition as an **authority migration**, not as a label edit.

A transition is not complete merely because the new state appears somewhere. In the same bounded package:

1. update the positive current-state declarations;
2. remove or reclassify old active work-selection instructions that contradict the new state;
3. update re-entry questions, intake templates, stop conditions, and continuation rules;
4. reconcile `STATUS.md`, `docs/CURRENT.md`, `HANDOFF.md`, `README.md`, `RUNBOOK.md`, and any affected completion/maturity contracts;
5. preserve superseded reasoning as historical evidence rather than leaving it executable as current procedure;
6. add or update documentation-authority validation for both the **presence of the new state** and the **absence of known stale current-authority phrases**;
7. require exact-head Build Validation before merge;
8. close or supersede competing transition PRs so one canonical transition remains.

The governing invariant is:

```text
new maturity label
+ old active queue
= incomplete transition

new maturity label
+ reconciled work-selection logic
+ stale-authority rejection
= closed transition
```

Do not infer authority from the newest file or PR alone. The repository must have one coherent current re-entry path after the transition.

## Documentation discipline

Do not create another master context or governance truth file. Current truth remains distributed by responsibility:

- `STATUS.md` — current state;
- `docs/CURRENT.md` — document authority;
- `HANDOFF.md` — current re-entry summary;
- `GameCompletionDefinition.md` and maturity/domain contracts — requirements;
- `RUNBOOK.md` — procedure.

If an optional context file is ever introduced for a harness, it must be navigation-only and must not duplicate mutable state, milestone counts, SHAs, or independent policy.
