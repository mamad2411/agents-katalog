---
name: codex-delegate
description: |
  Build a versioned codex delegation envelope and route it through the guarded codex wrapper.
when_to_use: |
  Use when the operator calls /codex:delegate or when codex-coder / codex-reviewer need to
  delegate a bounded coding or review task to codex.
---

# Codex Delegate

This skill is the routing contract for the `codex` plugin. It prepares one
`codex.delegation.v1` envelope and invokes the shared wrapper:

```bash
python3 plugins/codex/scripts/codex_delegate.py
```

The wrapper is the only supported execution path. Do not call raw `codex` directly, do not run a
background or detached path, and do not solve the delegated task locally as a fallback.
Direct Read/Edit/Write solving is a contract breach.

## Required Inputs

- `role`: `coder` or `reviewer`.
- `mode`: `read-only` or `task`.
- `task`: bounded task text or a task file path.
- `evidence`: `minimal`, `summary`, or `full`.
- `write_set`: explicit paths, required when `mode=task`.
- `model` / `effort`: optional for direct `/codex:delegate` use; omit them to let codex fall back
  to its own configured default (KTD3). Saga registry dispatch supplies both explicitly and fails
  closed if either is absent.

Registry-backed Codex identity is the canonical `<model>-<effort>` pair, for example
`gpt-5.6-sol-high`. The separate `model` and `effort` fields are preserved in the envelope so the
Codex argv, bridge receipt, and Saga evidence can be compared without parsing prose.

## Shared Envelope Gate

- Coder delegations default to `mode=task`, which is write-capable but scoped to a disposable
  clone only — a run always preserves its patch in the evidence bundle and never applies to the
  live tree in v1 (KTD5).
- Reviewer delegations default to `role=reviewer`, `mode=read-only`, and
  `review_lens=adversarial`.
- Supported reviewer lenses are `adversarial`, `quality`, `scope-gap`, and `security-ops`; route
  lens variants through the envelope instead of creating more agents.
- The wrapper owns evidence capture, provenance classification, and changed-path checks once the
  supervised runner lands (U2/U3).

## Delegation Flow

1. Normalize the requested role, mode, lens, write-set, evidence level, and timeout into the
   `codex.delegation.v1` contract.
2. Write the task to a temporary task file when needed.
3. Invoke exactly one wrapper run through `plugins/codex/scripts/codex_delegate.py`.
4. Report only the wrapper output and evidence bundle path.

Each follow-up delegation is a fresh wrapper invocation.
