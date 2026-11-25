---
name: repolish
description: Review and clean an entire repository for readability and maintainability, standardize language formatting, refactor while preserving behavior, and remove proven-unused code using coordinated subagents and resumable file accounting. Use for repository-wide cleanup or organization requests; a small feature or isolated formatting fix does not require a whole-repository pass.
---

# Repolish

Turn a repository into code people can comfortably read and maintain. Account for every file in the agreed scope; rewrite a file only when the change improves it. Preserve features, observable behavior, public contracts, and user work.

Read [references/workflow.md](references/workflow.md) before starting. It defines discovery, formatter selection, worker assignments, deletion evidence, verification, and the inventory helper commands.

## Defaults

- Perform full behavior-preserving cleanup: formatting, naming, control flow, function responsibilities, module organization, duplication, and dependency boundaries.
- Standardize each language with a conventional formatter, even where existing styles conflict. Add minimal pinned development tooling if needed; preserve runtime dependencies, compiler semantics, and language targets.
- Remove files or code only when evidence supports non-use. Leave uncertain candidates in place and explain them.
- Continue past pre-existing failures, record them, and fix cleanup regressions. Missing checks and unverified behavior remain explicit gaps.
- Work locally. Cleanup does not authorize automatic commits, publication, deployment, runtime dependency upgrades, or public API changes.

Honor narrower user scope and repository instructions. Do not turn a small request into a repository overhaul. When cleanup is requested, carry out justified local changes without repeated confirmation; a request only to plan or review does not authorize implementation.

## Execute in passes

1. **Map and baseline.** Read applicable instructions, inspect working changes, discover workspaces, languages, entrypoints, generators, public consumers, and existing checks. Create the external file ledger and capture baseline results.
2. **Format centrally.** Choose one primary formatter per language or compatible file domain. Normalize indentation, wrapping, and logical spacing with syntax-aware tools. Keep mechanical changes distinguishable from structural edits; check the formatted baseline before parallel work.
3. **Review in parallel.** Partition by cohesive subsystem with exclusive file ownership. Each worker reads its files and relevant callers, makes justified improvements, and runs focused checks. Formatting alone is not code review.
4. **Integrate.** The lead resolves shared-file requests, cross-boundary moves, imports, configuration, and deletions. Run relevant combined checks and inspect the final diff for behavior changes and unrelated edits.
5. **Reconcile and finish.** Refresh inventory and receipts against final contents. Account for additions and removals. Finish only when there are no pending files or unexplained regressions; label blocked coverage or verification limits as incomplete.

## Readability and fundamentals

Use descriptive names, focused functions, straightforward control flow, and blank lines between logical steps. Prefer useful intent comments over narration of obvious operations. Preserve nuanced validation, error handling, ordering, state transitions, resource cleanup, and async behavior.

Apply SOLID where responsibilities, substitutability, interfaces, or dependency direction cause concrete maintenance problems. Use DRY for shared knowledge, KISS for simpler solutions, and YAGNI to avoid speculative extension points. Cohesive functions or modules often suffice; do not manufacture classes, interfaces, wrappers, or a new architecture to satisfy a checklist.

Do not split semicolons, braces, strings, or comments using text replacement to simulate formatting. Do not force tabs where the language requires spaces, or expand intentionally compact data and generated output merely to look handwritten.

## Parallel ownership

The lead owns the ledger, shared configuration, package manifests, lockfiles, common exports, cross-subsystem changes, integration, and completion claims. Workers own disjoint file sets, never spawn additional workers, and return proposals for edits outside their ownership. Serialize shared writers and checks that mutate the same outputs.

Use available subagent capacity only where work can be separated; otherwise run serially and disclose that limitation. A worker returning successfully is not evidence that the integrated repository works.

## File accounting

Use `scripts/inventory.py` to initialize, reconcile, record dispositions, and report coverage. It writes only an external ledger and cannot rewrite or delete source. Only the lead writes the ledger; workers return receipts.

Record `reviewed`, `changed`, `removed`, `excluded`, or `blocked` with specific evidence. `reviewed` means the relevant content was actually inspected; `changed` includes final-content review, not just a formatter run. Generated, vendored, binary, ignored, linked, and nested-repository material needs an explicit exclusion reason. Read and review human-authored configuration, documentation, and generator sources where they affect the codebase.

The helper checks inventory freshness, not semantic correctness or test success. Refresh receipts after content changes. Preserve uncertain removal candidates and never report exclusions as refactored code.

## Deliver

Report substantive improvements, files removed and why, coverage counts, checks with actual outcomes, baseline failures, retained candidates, and remaining gaps. Link the external ledger/report location. Distinguish final integration verification from worker checks and formatting. Describe unverified areas without claiming behavioral equivalence that the evidence cannot establish.
