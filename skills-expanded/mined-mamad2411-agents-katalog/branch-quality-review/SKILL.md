---
name: branch-quality-review
description: Deep quality review of branch or diff changes -- correctness, architecture, test value, decision clarity. Use for any on-demand review of a branch, diff, or PR's code. Flags -- --read-only (findings only, no edits), --strict (harsh maintainability bar).
---

# Branch Quality Review

The core on-demand review skill. Reviews branch changes across four passes. Other review skills call this one -- keep it self-contained.

Default: fix what's clearly wrong inline, flag what needs judgment. `--read-only` flips this to findings-only (use when reviewing someone else's code).

## Arguments

Parse `$ARGUMENTS`:

- `--read-only`: make NO edits. Note findings only. The author decides what to act on.
- `--strict`: apply the strict maintainability bar (see below) on top of the normal passes.
- Anything else is a base ref override (default: `main`).

## Setup

1. `git log <base>..HEAD --format="%h %s%n%b%n---"`, `git diff <base>...HEAD --stat` to scope the change.
2. Read every changed file. Use an Explore agent for large diffs (>10 files).
3. **Repo-specific patterns.** Derive the repo key:
   ```bash
   basename "$(git remote get-url origin 2>/dev/null | sed 's/\.git$//')"
   ```
   If `~/.claude/review-patterns/<key>/` exists, read every `.md` file in it and fold those checks into the passes below. If the directory does not exist, skip this step silently -- do not mention it.

## Pass 1: Correctness & safety

- **Logic**: off-by-one, wrong conditionals, race conditions, bad state transitions, unreachable branches.
- **Types**: `any`, unsafe assertions (`as unknown as X`), missing narrowing, hand-maintained unions a library already types.
- **Null/undefined**: optional values accessed without a guard where `?.`/`??` would prevent a runtime error.
- **Errors**: silently swallowed errors, missing try/catch around async, `.then()` where `.finally()` is needed for cleanup, unhandled rejections.
- **Resource cleanup**: subscriptions, observers, or disposables not registered for teardown; leaks.

Read enough surrounding context to avoid false positives (a guard may exist upstream). Surface suspicious-but-unsure patterns as questions, not just confirmed bugs.

## Pass 2: Architecture

Vocabulary: module, depth, seam, locality, leverage.

- **Deletion test**: would removing an abstraction concentrate or scatter complexity?
- Shallow modules (interface ~= implementation)? Inline them.
- Speculative seams (one adapter)? Remove.
- Pass-throughs adding interface without depth? Inline.
- **Interface too wide?** A parameter that every caller derives from context, an injected service, or another value the callee could reach itself is caller-side plumbing -- pull it inside and shrink the signature (deep module = small interface). Counterweight: keep the param if it is a real injection seam that varied callers or tests exercise with different values.

## Pass 3: Test value

- Tests must target the **interface**, not internals.
- Each test must catch a real failure mode, not mirror the implementation.
- Delete tests that only buy coverage percentage. Add tests for actual risk paths.

## Pass 4: Decision clarity

- Every non-obvious "why this way?" must be answerable from naming, structure, or a one-line comment.
- Flag decisions that rely on oral tradition. Suggest CONTEXT.md/ADR entries for load-bearing choices.

## Strict tier (`--strict` only)

Be ambitious about structural simplification. Hunt for "code judo": restructurings that preserve behavior while deleting whole branches, modes, or layers. Prefer deleting complexity over rearranging it.

Treat these as presumptive blockers unless the author justifies them:

- A plausible code-judo move that would delete incidental complexity is left on the table.
- The PR pushes a file from under 1000 lines to over 1000 without a strong reason.
- Ad-hoc branching or one-off special cases bolted into an existing flow that make it more tangled.
- Feature-specific logic scattered across shared/general-purpose paths.
- An unnecessary wrapper, cast, or `any`/`unknown`/optional churn that obscures the real contract.
- A bespoke helper duplicating an existing canonical one, or logic placed in the wrong layer.

Prefer a few high-conviction structural findings over a long list of nits.

## Finishing

- **Default mode**: fix clear issues inline, then run tests. Summarize as **Fixed** (`file:line` cited) and **Flagged** (issue + suggested resolution).
- **Read-only mode**: make no edits. Summarize as **Findings** (`file:line`, grouped by pass) and a one-line **Verdict**.
- Cite `file:line` for every finding.
- If the branch is solid, say so and stop. Don't pad.

After presenting findings (not in read-only mode), suggest `grill-my-pr` if the user wants to pressure-test that they can defend every decision before submitting.
