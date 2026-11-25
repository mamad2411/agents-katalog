---
name: twining-verify
description: Runs pre-completion verification — checks unresolved warnings, decision hygiene, and drift. Recommended for complex tasks; for simple tasks a status post via twining_post is sufficient.
auto-invocable: true
---

# Twining Verify — Pre-Completion Verification

For complex tasks (multi-file changes, architectural decisions, long sessions), verify your work against Twining's coordination state. For simple tasks, posting a `status` entry via `twining_post` is sufficient.

> **Note:** `twining_verify` requires `tools.full_surface: true` in config. If not available, post a `status` entry via `twining_post` summarizing what you did.

## When to Invoke

- Complex multi-file changes with architectural decisions
- Before handing off work to another agent on a large task
- Before creating a pull request with significant changes
- When you want to check for decision drift or unresolved warnings

## Workflow

### 1. Run Verification

Call `twining_verify` with:
- `scope`: The area you worked on (e.g., `"src/auth/"`)
- `checks`: Array of checks to run. Include all relevant ones:
  - `"test_coverage"` — Are decisions backed by `tested_by` relations?
  - `"warnings"` — Are all warnings acknowledged or resolved?
  - `"assembly"` — Were decisions made after assembling context (not "blind")?
  - `"drift"` — Has code drifted from decision intent?
  - `"constraints"` — Do checkable constraints still pass?

### 2. Interpret Results

Each check returns a status:

**`pass`** — No issues found. Proceed.

**`warn`** — Issues exist but aren't blocking:
- Uncovered decisions (no `tested_by` relation) — consider adding test links
- Blind decisions (made without `twining_assemble`) — acknowledge or re-verify
- Minor drift detected — review if decisions are still accurate

**`fail`** — Issues that should be addressed:
- Silently ignored warnings — read and acknowledge each one
- Failed constraint checks — fix the violation or update the constraint
- High drift count — decisions may be stale

### 3. Address Issues

For each issue found:

**Uncovered decisions** — If you wrote tests that cover a decision and the knowledge graph is enabled (`graph.auto_populate: true`), link them:
```
twining_add_relation(
  source="<affected_file>",
  target="<test_file>",
  type="tested_by",
  properties={ covers: "<what it tests>" }
)
```
If the graph is not enabled, this check can be safely ignored.

**Blind decisions** — If you skipped `twining_assemble` before deciding, acknowledge it. The decision may still be valid, but note that shared context wasn't consulted.

**Ignored warnings** — Read each warning. Either resolve the underlying issue or acknowledge it with a `twining_post` status entry explaining why it's acceptable.

**Stale decisions** — If code has changed significantly since a decision was made, use `twining_reconsider` to flag it for review.

### 4. Review What Changed

Call `twining_what_changed` with `since` set to your session start time. This shows:
- New decisions you or others made
- New blackboard entries
- Overridden or reconsidered decisions

Verify that all significant choices from your session are captured as decisions.

### 5. Link Commits

For each decision you made that's been committed, call `twining_link_commit` with the decision ID and commit hash.

### 6. Post Status Summary

Call `twining_post` with:
- `entry_type: "status"`
- `summary`: What you accomplished (one line)
- `detail`: Key changes, decisions made, any remaining work
- `scope`: The area you worked on

## After Verification

If all checks pass (or warnings are acknowledged), you can confidently tell the user the task is done. If issues remain, address them or explicitly communicate what's outstanding.
