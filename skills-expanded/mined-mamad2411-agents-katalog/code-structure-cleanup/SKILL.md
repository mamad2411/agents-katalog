---
name: code-structure-cleanup
description: Use after behavior works to clean up structure, reduce duplication, extract repeated mechanics, prepare a focused PR, or make agent-written code maintainable without behavior changes.
---

# Code Structure Cleanup

Use this skill only after behavior is working or when the user explicitly asks for a cleanup, refactor, duplication reduction, or PR-readiness pass.

## Goals

- Reduce repeated mechanics: API calls, parsing, validation, serialization, adapters, IO, setup, error handling, and similar runtime plumbing.
- Preserve domain policy, public contracts, and user-facing behavior.
- Prefer existing local patterns over introducing a new architecture.
- Keep the diff scoped to files touched by the feature and directly related helpers.
- Improve future agent readability by making the shared mechanism obvious and named.

## Workflow

1. Inspect `git status --short` and relevant diffs before editing.
2. Identify concrete duplication by file, function, or call site.
3. Decide whether extraction is worth it; skip tiny, speculative, or one-off abstractions.
4. Choose the smallest repo-appropriate home for shared mechanics: existing service, adapter, utility, hook, parser, module-private helper, or test helper.
5. Ask before editing unless the user explicitly requested implementation.
6. Implement the minimal extraction and update callers.
7. Run the narrowest meaningful tests, typechecks, linters, or focused commands.
8. Summarize what got simpler, what behavior stayed unchanged, and any residual risk.

## Guardrails

- Do not redesign module boundaries or refactor unrelated areas.
- Do not rename broadly unless the current name is actively misleading.
- Do not move business decisions into generic services or low-level helpers.
- Do not mix cleanup with new product behavior.
- Do not create a "service layer" if the repo has a better established pattern.
- Do not hide meaningful differences behind a premature abstraction.

## Verification

Before finishing, check:

- User-facing behavior stayed the same.
- Repeated mechanics were actually reduced.
- Calling files became simpler or easier to scan.
- The diff stayed focused on the feature area.
- Relevant validation ran, or any skipped validation is explained.

## Final Response

Report:

- Duplication or structural friction found.
- Extraction or cleanup performed.
- Files changed.
- Validation run.
- Behavior-preservation risks or follow-ups.
