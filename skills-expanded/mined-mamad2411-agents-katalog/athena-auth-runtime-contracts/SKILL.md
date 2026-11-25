---
name: athena-auth-runtime-contracts
description: Trace, debug, or explain Athena Auth runtime contracts. Use when Codex needs to follow the real request path through `AthenaAuth::handle_request`, Axum integration, session extraction, `/get-session`, `/api-key/verify`, API-key virtual sessions, session cache refresh, revoke-session behavior, or admin audit logging in the `athena-auth` repo. Also use when a consumer or SDK bug likely comes from Athena Auth route behavior rather than UI, generator, or email-template code.
---

# Athena Auth Runtime Contracts

Use this skill for three seams:

1. Core request dispatch and Axum mounting.
2. Session, API-key, and `/get-session` behavior.
3. Admin audit and runtime truth debugging.

If the task is mostly admin email or email-template behavior, use
`$athena-auth-emails` instead.

## Read in this order

1. Read [references/request-pipeline.md](references/request-pipeline.md) when the task is about routing, base path normalization, plugin precedence, Axum behavior, or "which handler actually runs?"
2. Read [references/session-api-key-audit.md](references/session-api-key-audit.md) when the task is about `/get-session`, `/api-key/verify`, virtual sessions, session cache refresh, revoke flows, or admin audit rows.
3. Inspect the active checkout after the reference file identifies the exact source files and tests.

If docs, architecture notes, and implementation disagree:

- trust current source and tests over older diagrams
- trust the actual request path over SDK assumptions
- patch the real runtime seam instead of working around it in a consumer repo

## Choose the seam first

### Request pipeline and route ownership

- Start at `AthenaAuth::handle_request`.
- Then inspect Axum route registration and request extraction.
- Confirm whether the path is already normalized, base-path mounted, or plugin-owned before changing route behavior.

### Session or API-key behavior

- Inspect the shared `/get-session` path first.
- Check whether the caller is on bearer session auth, cookie auth, or API-key virtual session emulation.
- Treat direct DB user refresh and session-user cache behavior as part of the contract.

### Admin audit behavior

- Inspect admin plugin request handling and audit writes together.
- Preserve exact `action`, `target_type`, `target_id`, success flag, and actor-user semantics.

## Keep these rules stable

- Follow the real runtime request path before changing docs or SDK wrappers.
- Preserve plugin precedence and base-path stripping behavior.
- Preserve the immediate-refresh contract for `/get-session` after direct user changes.
- Treat API-key `/get-session` emulation as a first-class runtime seam, not a test-only hack.
- Use WSL2 for Rust test runs on this machine.
- Validate with the narrowest matching test first, then broaden only if needed.

## Validate

- Request-pipeline or Axum changes: run the matching route-matrix or Axum integration test.
- API-key or `/get-session` changes: run targeted API-key and get-session tests first.
- Admin audit changes: run targeted admin plugin tests first.
- Broader runtime changes: escalate to wider workspace tests only after the narrow seam passes.
