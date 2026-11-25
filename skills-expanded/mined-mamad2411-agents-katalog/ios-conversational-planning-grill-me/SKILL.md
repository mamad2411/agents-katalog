---
name: ios-conversational-planning-grill-me
description: Produce an implementation-ready plan for iOS projects through repository discovery, iOS architecture analysis, and a conversational decision interview. Use before coding when UIKit, SwiftUI, Rune, navigation, lifecycle, concurrency, or ubiquitous-language and business-logic constraints matter. Do not use for non-iOS repositories; use `$conversational-planning-grill-me` there.
disable-model-invocation: true
---

# iOS Conversational Planning + Grill Me

## Outcome

An approved, implementation-ready iOS plan. This skill owns only the iOS-specific evidence and constraints; `$conversational-planning-grill-me` owns the planning model, the `$grill-me` interview, the decision ledger, conflict handling, the `$unslop` pass, the final approval gate, and the implementation handoff. Do not duplicate or weaken the shared engine's decision protocol.

## Inputs and preconditions

An iOS repository (UIKit, SwiftUI, or hybrid) and a change request. If the repository turns out not to be an iOS project, switch to `$conversational-planning-grill-me` directly.

## Workflow

### 1. iOS preflight

Before invoking the shared engine, read, in order when present:

1. Applicable `AGENTS.md` files and explicit user constraints.
2. `docs/UBIQUITOUS_LANGUAGE*` and `docs/UBIQUITOUS_BUSINESS_LOGIC*`.
3. `CONTEXT.md`, `CONTEXT-MAP.md`, ADRs, architecture docs, and feature notes.
4. Relevant models and contracts, then services, DI, navigation, state owners, and UI.
5. Tests, fixtures, previews, analytics, flags, migrations, and recent history that clarify intended behavior.
6. Nearby implementation exemplars and formatter or linter configuration.

Use `rg` and targeted reads. Avoid broad repository dumps. Follow imports and call sites only until each planning branch has enough evidence.

### 2. Apply the iOS planning lenses

Read [references/plan-readiness.md](references/plan-readiness.md) once a repository-backed plan is confirmed, and apply only the lenses relevant to the task. That reference is the single home of the iOS-specific lenses (architecture parity, Rune-first composition, domain-document usage, concurrency isolation, and verification limits); do not restate them here or in the plan from memory.

### 3. Hand off to the shared engine

Invoke `$conversational-planning-grill-me` with the iOS evidence, terminology, constraints, and open decisions. Carry the iOS-specific findings into its final plan.

### 4. Post-approval routing

For approved SwiftUI work, preserve the shared handoff rules and invoke `$project-rune-implementation-protocol` when the work is a Rune-first feature in a project that follows that protocol. Invoke `$swift-sako-semantic-linter` after in-scope Rune Swift or SwiftUI edits, and `$swift-6-concurrency` when the approved work materially changes isolation, `Sendable`, tasks, actors, or async control flow.

## Constraints

- Treat domain docs as domain authority, not infallible snapshots. When docs and executable behavior differ, report both with source anchors and make reconciliation an explicit decision.
- Never bypass the shared engine's approval gate, even for changes that look mechanical.

## Composition

<interface>
| Invokes | When | Carries in | Expects back | If unavailable |
| --- | --- | --- | --- | --- |
| `$conversational-planning-grill-me` | Step 3, after the iOS preflight | iOS evidence, canonical terminology, constraints, open decisions | The approved final plan and decision ledger | Run the interview with `$grill-me` directly, replicate the approval gate, and note the missing engine |
| `$project-rune-implementation-protocol` | Post-approval, for Rune-first SwiftUI feature work in protocol-following projects | The approved plan, decision ledger, and verification limits | The implemented vertical slice and integration report | Implement directly against local patterns and report the limitation |
| `$swift-sako-semantic-linter` | After in-scope Rune Swift or SwiftUI edits | The list of touched Swift files | The semantic scan report with fixes applied | Preserve local patterns and state that semantic compliance is unverified |
| `$swift-6-concurrency` | When approved work materially changes isolation, `Sendable`, tasks, actors, or async control flow | The concurrency-relevant diff and project settings | Isolation-correct guidance or fixes | Flag the concurrency risk for manual review |
</interface>

The shared engine owns the single `$unslop` pass on the outermost final planning artifact. The canonical hygiene rule applies only when this skill produces a separate iOS-specific report outside that engine:

Invoke `$unslop` once on the complete user-facing artifact after its technical content is final, unless a parent workflow owns the final artifact, in which case the outermost workflow makes the single pass. `$unslop` may improve prose but must not change technical meaning: preserve code, paths, symbols, commands, measurements, quoted decisions, evidence anchors, classification labels, and document structure. If `$unslop` is unavailable, deliver the artifact unchanged and note the skipped pass. In this skill, the pass must also never run twice on the same artifact.

## Failure handling

- Domain docs are missing: proceed on code evidence alone and record that terminology and invariants are unconfirmed by documentation.
- Domain docs contradict code: present both with source anchors as an explicit reconciliation decision; do not pick a side silently.
- A post-approval callee is unavailable: follow its `If unavailable` fallback above and record the limitation in the handoff.

## Output contract

The shared engine's output contract applies. iOS findings appear inside that plan as evidence anchors, lens results, and constraints, not as a separate parallel document, unless the user asks for a standalone iOS report.
