---
name: xcode-build-fixer
description: Implement approved Xcode build optimization changes following best practices, then re-benchmark to verify improvement. Use when the developer has reviewed an optimization plan and approved specific changes, or when there is a clear list of build-setting or source-level fixes to apply and verify.
---

# Xcode Build Fixer

Use this skill to apply approved build optimization changes and re-benchmark to verify improvements.

## Non-Negotiable Rules

- Only apply changes that have explicit developer approval.
- Apply one logical fix at a time so changes are reviewable and reversible.
- Verify compilation succeeds after each change.
- Re-benchmark after all changes using the same baseline parameters.
- Do not revert best-practice settings based on single benchmark runs.

## Fix Categories

### 1. Build Settings

Modify `project.pbxproj` values directly. Common examples:

- `DEBUG_INFORMATION_FORMAT = dwarf` (Debug)
- `COMPILATION_CACHING = YES`
- `EAGER_LINKING = YES`
- `ONLY_ACTIVE_ARCH = YES` (Debug)
- `SWIFT_COMPILATION_MODE = singlefile` (Debug)

### 2. Script Phases

- Add input/output file declarations to prevent unnecessary re-execution.
- Add configuration guards (`if [ "$CONFIGURATION" != "Debug" ]; then exit 0; fi`).
- Convert `alwaysOutOfDate` scripts to properly declared dependencies.

### 3. Source-Level Fixes

Code changes that reduce compiler overhead:

- Add explicit type annotations to complex expressions.
- Mark classes `final` when not subclassed.
- Narrow access control (`private`, `fileprivate`).
- Decompose large SwiftUI `body` properties into subviews.
- Break long method chains with typed intermediates.

### 4. SPM Restructuring

- Pin branch-tracked dependencies to version tags or revision hashes.
- Extract shared contracts to break circular dependencies.
- Separate interface from implementation modules.

## Execution Workflow

1. Read the approved items from `.build-benchmark/optimization-plan.md`.
2. For each approved item:
   a. Identify the exact file(s) and location(s) to change.
   b. Apply the change.
   c. Verify compilation: `xcodebuild build`.
   d. If compilation fails, revert and note the issue.
3. After all changes are applied and compiling, re-benchmark using the original baseline parameters.
4. Compare results and generate the execution report.

## Regression Evaluation

A change is only a clear regression if it makes the metrics that matter to the developer's daily workflow worse. Evaluate holistically:

- **COMPILATION_CACHING**: May make standard clean builds slightly slower (cache population overhead) while making cached clean builds significantly faster. This is a net positive for real developer workflows.
- **Best-practice settings** (`COMPILATION_CACHING`, `EAGER_LINKING`, `SWIFT_USE_INTEGRATED_DRIVER`, `DEBUG_INFORMATION_FORMAT = dwarf`): Retain regardless of immediate benchmark results -- they align with Apple's recommended configuration.
- **Speculative changes**: Revert only if they regress across all build types.

## Reporting Format

Use an execution report table:

```markdown
## Execution Report

| # | Change | Baseline | After | Delta | Status |
|---|--------|----------|-------|-------|--------|
| 1 | Set DEBUG_INFORMATION_FORMAT=dwarf | 86.2s | 82.1s | -4.1s (-4.8%) | Kept |
| 2 | Enable COMPILATION_CACHING | 86.2s | 87.0s (cold) / 78.5s (cached) | +0.8s cold / -7.7s cached | Kept (best practice) |
| 3 | Guard release-only script | 4.2s inc | 2.1s inc | -2.1s (-50%) | Kept |
```

Status values: `Kept`, `Reverted`, `Blocked` (compilation failed), `No improvement` (kept if best practice, reverted if speculative).

## Additional Resources

- For build settings best practices, see [references/build-settings-best-practices.md](references/build-settings-best-practices.md)
- For fix implementation patterns, see [references/fix-patterns.md](references/fix-patterns.md)
- For the shared recommendation structure, see [references/recommendation-format.md](references/recommendation-format.md)
