---
name: agy-delegate
description: |
  Build a versioned Antigravity teammate delegation envelope and route it through the guarded
  agy wrapper.
when_to_use: |
  Use when the operator calls /agy:delegate or when agy-coder / agy-reviewer need to delegate a
  bounded coding or review task to Antigravity.
---

# Agy Delegate

This skill is the routing contract for the dormant `agy` plugin scaffold. It prepares one
`agy.delegation.v1` envelope and invokes the shared wrapper:

```bash
python3 plugins/agy/scripts/agy_delegate.py
```

The wrapper is the only supported execution path. Do not call raw `agy` directly, do not run a
background or detached path, and do not solve the delegated task locally as a fallback.
Direct Read/Edit/Write solving is a contract breach.

## Required Inputs

- `role`: `coder` or `reviewer`.
- `mode`: `no-write` or `patch-only`.
- `task`: bounded task text or a task file path.
- `evidence`: `minimal`, `summary`, or `full`.
- `write_set`: explicit paths bounding what the delegate may change in the clone.
- `verification`: orchestrator-supplied commands when checks are required.

## Shared Envelope Gate

- A delegation never writes the live tree. Every mode runs in a disposable clone and returns a
  patch for the caller to apply; `apply_policy` is always `preserve-patch`. Concurrent writes are
  prevented by assigning work units that do not cross files, not by a runtime fence.
- Coder delegations default to `mode=patch-only`.
- Reviewer delegations default to `role=reviewer`, `mode=no-write`, and
  `review_lens=adversarial`.
- Supported reviewer lenses are `adversarial`, `quality`, `scope-gap`, and `security-ops`; route
  lens variants through the envelope instead of creating more agents.
- Verification commands are supplied by the orchestrator or operator. The delegated teammate must
  not invent the gate it will be judged by.
- Verification runs inside the disposable clone for `patch-only`, after the delegate's changes and
  before the patch is reported. `verification.required` decides whether a failure is terminal: a
  required command that fails yields `checks_failed`, while an unrequired one is recorded in
  `checks.json` and leaves the run `patch_ready`. `no-write` runs skip verification — the clone is
  unchanged, so there is nothing to verify.
- The wrapper owns evidence capture, provenance classification, and changed-path checks.

## Delegation Flow

1. Read `agy/skills/agy-delegate/references/delegation-contract.md`.
2. Normalize the requested role, mode, lens, write-set, evidence level, timeout, and verification
   policy into the `agy.delegation.v1` contract.
3. Write the task to a temporary task file when needed.
4. Invoke exactly one wrapper run through `plugins/agy/scripts/agy_delegate.py`.
5. Report only the wrapper projection and evidence bundle path.

Each follow-up delegation is a fresh wrapper invocation unless a later wrapper version explicitly
adds stateful conversation support.
