---
name: code-modernization
description: "Behavioral parity guides legacy-code assessment, version upgrades, incremental rewrites, and architecture rebuilds. Use when planning or executing a code modernization, or checking migration evidence."
disable-model-invocation: true
---

# Code Modernization

Modernize one bounded slice while preserving its observable behavior. Start with a pilot and expand only after its evidence passes.

Use the host's file, shell, question, and review tools. Run sequentially by default. Delegation requires explicit authorization and available host capabilities. The workflow needs no Claude Code plugin, hook, slash command, or model version.

## 1. Establish intent and resume state

Read repository instructions, existing plans, and working-tree changes. Infer the requested mode: **assess**, **execute**, **resume**, or **verify**. A request to understand or plan authorizes analysis; an implementation request authorizes the stated migration scope.

Read [ARTIFACTS.md](ARTIFACTS.md) before creating or resuming a run. Reuse its artifacts and recorded answers. Ask only for missing decisions that affect correctness or scope: source and target, observable contracts, permitted changes, or external consumers. Continue independent analysis while waiting.

Resolve the actual source root and revision. Keep the baseline immutable; use an isolated checkout or repository-approved workspace for changes. Record the source of any included uncommitted work. If source is unavailable, produce a proposal labelled unverified and identify the access needed. Analysis cannot establish implementation facts without code.

## 2. Preflight and map

Inspect manifests, CI, build wrappers, generators, private dependency feeds, and test configuration. Measure the existing build and tests on this code. Record tool versions, commands, results, and baseline failures. Inspect test destinations before running code that writes data or calls external services.

Map entry points, dependencies, cycles, state changes, storage, authorization, and externally consumed contracts. Follow imports across the slice boundary. Classify each finding as observed, inferred, or unknown, with source locations at the recorded revision. Count generated and vendored code separately.

For a large estate, process bounded modules and keep a coverage ledger. Every module in the declared scope must be accounted for. Record unread files and unresolved dependencies as gaps.

## 3. Define the behavior contract and choose a pilot

Extract rules for calculations, validation, permissions, state transitions, and side effects. Give each rule an ID, Given/When/Then cases, and source citations. Re-read the cited implementation and callers. Comments alone do not establish behavior. Separate existing quirks from intended behavior and record any unresolved conflict.

Select one small unit with observable inputs and outputs. Record its explicit file scope, dependencies, protected verification configuration, required checks, and rollback method. Prefer dependency leaves; resolve cycles and shared contracts explicitly.

Choose **uplift**, **transform**, or **reimagine** using [MIGRATION.md](MIGRATION.md). Finish assessment with a phased plan and evidence gaps. Execute only the work already authorized. A new target architecture, changed product behavior, or wider scope needs the missing decision; routine in-scope repairs proceed.

## 4. Establish verification, then migrate

Read [VERIFICATION.md](VERIFICATION.md) before changing production code. Build characterization tests from legacy execution or identified recorded evidence. Establish a measured baseline and show that a meaningful mutation is detected.

Implement the selected branch in bounded batches. Use deterministic transforms for repeated mechanical changes and agents for unresolved semantic work. Run focused checks during repairs and all required checks at the batch boundary. Preserve test expectations and protected checks; changing the oracle is a separate recorded decision.

Record each failed attempt and its new evidence. After three repair attempts without a new diagnosis, reduce the slice or resolve the missing contract instead of repeating the same edits. This is a replanning point, not a pass.

## 5. Verify and deliver

Perform a separate verification pass from the recorded contract and current diff. Follow the verdict criteria in [VERIFICATION.md](VERIFICATION.md). If no independent reviewer is available, label the pass as self-review.

Update state after each batch and before handoff. Deliver the diff, behavior-to-test mapping, executed checks, deliberate differences, rollback instructions, and remaining gaps. Report only the declared slice as complete. Claim estate completion only when every scoped unit meets its exit criteria.

For **resume**, revalidate source and target revisions before using old evidence. For **verify**, leave implementation and oracle unchanged; report findings for a repair pass. Merge and deployment follow the user's existing authorization and repository rules.

Read [SOURCES.md](SOURCES.md) when inspecting provenance or comparing this adaptation with the upstream plugin.
