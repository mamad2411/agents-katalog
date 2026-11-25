---
name: coff0xc-software-engineering
description: "Use when the user requests dev/software engineering: build product, repo repair, failing tests/CI, bugfix, feature/refactor, full-stack/end-to-end implementation, REST API/frontend UI implementation, scripts, Python/JS/TS/Go/Rust/Java/C/C++/Shell, dashboard/admin/API, browser smoke, diff/lockfile hygiene, minimal fix, direct implementation, prove it works. Manual trigger: Use coff0xc-software-engineering."
---

# coff0xc-software-engineering

<!-- skill-id: cs-swe-1a4f8c03 -->

## Quick Rules (read this first for everyday tasks)
> **[Read the repo first]** Look first at AGENTS/README, package/lockfile, entry points, test scripts, and the current dirty worktree.
> **[Minimal fix]** Change only the requested scope; reproduce/locate first, then patch in small steps, with no unrelated refactoring or new-framework migration.
> **[Verification loop]** Run the target test/typecheck/lint/build first, then widen by risk; what has not been run must not be written as verified.
> **[Git boundary]** Do not roll back user changes; confirm first for push, PR, deletion, production, credentials, and CI/CD permissions.

Execute ordinary development tasks directly from this section; expand the full workflow only for large features, architecture/API/schema/auth, CI releases, or skill quality validation.

If a task escalates to multi-file, multi-stage, multi-skill, architecture/API/schema/auth, or multi-worker work, first have `coff0xc-skill-router` read `references/complex-workflow.md`. This skill owns implementation, repo repair, testing, and diff hygiene in that flow.

## Capability
Engineering-delivery capability for real repos. It turns vague requirements into runnable code, reproducible fixes, verifiable test results, and clear diff summaries.

## What It Can Deliver
- Code patches, scripts, or configuration changes
- Failure causes and root-cause chain explanations
- Unit/integration/build verification results
- Git diff summaries and residual risk

## What Input It Can Take
- Local repos, error logs, test output, issue descriptions
- Requirement drafts, interface notes, UI screenshots, or existing modules
- package/lockfile, README, AGENTS, CI scripts

## Safe-Use Boundaries
- Local, reversible, low-risk code and test changes can be made directly
- Deletion, remote push, production configuration, credentials, paid services, and CI/CD permission changes must be confirmed first
- Do not introduce a new framework or unnecessary dependency for a small problem
- By default only local, reversible, verifiable low-risk work; confirm first for anything involving production, credentials, payment, remote writes, deletion, publishing, or permission changes.

## Why You Can Trust It
- Reads project structure and existing style before changing anything
- Runs narrow verification first, then widens by risk
- Tests that have not been run are never written as passed

## Typical Usage
```text
Use coff0xc-software-engineering to fix this repo's failing tests and explain the verification results.
Use coff0xc-software-engineering to implement this multi-file development task directly, with minimal confirmations.
Use coff0xc-software-engineering to build this admin panel feature end to end with tests.
```

## Default Output
- Close with only done, verified, remaining, and next steps; give a path or location for any file/code/rule artifacts.
- Checks not actually run are marked unverified; security/architecture conclusions carry an evidence level.

## Expand on Demand
- Everyday tasks use only the quick rules, capability boundaries, and typical usage above; do not read the full gates by default.
- Read `references/full-workflow.md` only for deep architecture, complex multi-stage work, quality evaluation, release, formal delivery, or when the current task lacks evidence.
- After reading a reference, keep context to the minimum necessary; do not output long process write-ups or extra self-justifying material just because a reference exists.
