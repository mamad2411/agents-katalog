---
name: file-scope-rules
description: "Use when setting in_diff on a review finding, deciding whether a finding may block a change, or scoping a scan or review. The causation test for in_diff, why a pre-existing issue keeps its severity but never blocks, and which paths to skip."
license: MIT
---

# File scope rules

## The diff-scope rule

**A finding blocks only when this change introduced it or made it worse.** A pre-existing issue is
reported with `in_diff: false` and keeps the severity its impact earns. Scope is what stops it
blocking; its severity stays as it is.

Scope and severity are separate axes (see `code-review-standards`). Capping an out-of-diff finding at `NIT`
makes a latent SQL injection look like a whitespace complaint to every later reader: the
inline-comment selector, a severity-filtered fix-up pass, the next review of the same repo.
`in_diff: false` already says "does not block".

### The causation test

Ask: **is the problematic line added or modified by this change, or does the change break it?**
Answer from the diff under review. In the code-review pipeline that is `.code-review/DIFF.md`;
elsewhere, `git diff <target>...<source> -- <file>`.

| Where the root cause lives | `in_diff` | Severity | Blocks? |
| --- | --- | --- | --- |
| A line the diff added or modified | `true` | what impact earns | it can; `contract.py` decides |
| An unchanged line the diff breaks, e.g. a changed signature whose caller was not updated | `true`; anchor it on the changed line | what impact earns | it can, as above |
| Unchanged code the diff does not affect: latent, dead, "newly relevant", a global gate the change did not move | `false` | what impact earns, uncapped | no |

The test is causation, not proximity. "This file matters more now" does not make a latent bug in it
the change's fault, and neither does "the new path can reach this code" when the new path is itself
correct. Only "this change created or worsened it" sets `in_diff: true`.

### A critical pre-existing issue

An exploitable hole reachable in production, or data loss on a normal path, still gets
`in_diff: false` when this change did not cause it. Report it at `BLOCKER` and name it first in your
summary so a human acts on it separately. Blocking the change would not fix the issue, and the
pipeline's predicate never blocks on `in_diff: false`, so flipping scope to force a block is
anchor-shopping.

### Two ways reviewers break the rule

- **Anchor-shopping.** Attaching a finding to a new test file because the buggy source is not in the
  diff, then letting it block. Either the diff genuinely breaks the unchanged code (anchor on the
  in-diff line that breaks it) or it does not (`in_diff: false`, same severity).
- **Downgrading for uncertainty.** Certainty is `confidence`. A MAJOR you could only partly trace is
  a MAJOR at `MEDIUM` confidence. It stays a MAJOR, and it stays in the report.

## Paths a scan or review skips

Review changed source, tests, infrastructure-as-code, CI definitions, container and build files.
Skip these, because nobody hand-writes them or they are not this repo's code:

| Pattern | Why |
| --- | --- |
| `node_modules/`, `vendor/`, `.venv/` | vendored dependencies |
| `dist/`, `build/`, `out/`, `.next/`, `target/` | build output |
| `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.terraform/`, `.terragrunt-cache/` | tool caches |
| `coverage/`, `.nyc_output/` | coverage reports |
| lockfiles (`package-lock.json`, `yarn.lock`, `pnpm-lock.yaml`, `poetry.lock`, `*.lock`) | generated; review the manifest change instead |
| `.worktrees/`, `.git/` | other copies of the repo, VCS internals |
| `.env`, `.env.*` | secrets; do not read or quote them |

When no scope is given, review the changed files (`git diff --name-only <base>...HEAD`, or the staged
set), then a directory the caller named, and the whole repo only when asked.

## Verify

Before filing, check each `in_diff: true` finding's `location` against the diff: the line is added
or modified there, or the finding names the changed line that breaks it. Every other finding is
`in_diff: false` at unchanged severity.

Without a checkout, apply the causation test to the diff the user pastes. When the paste does not
show whether the change caused a finding, say so and lower its `confidence`, not its severity.
