# AGENTS.md

Use this file with [CLAUDE.md](./CLAUDE.md) before making changes in this directory.

This file provides agent-specific guidance for crate `shipper-core`.

## Role

`shipper-core` is the execution engine used by both `shipper` and `shipper-cli`.

- Plan generation and state transitions
- Runtime command execution and environment wiring
- Retry, output contracts, and pre/post-run orchestration logic
- Registry/authentication integration points

## Guidance

- CLI surface decisions belong to `shipper-cli`.
- Public API stability for consumed crate exports should be preserved when possible.
- Prefer editing internal behavior in this crate and keep `shipper` as a thin API facade.
- Keep tests, logging, and state transitions intentionally deterministic when changing execution paths.
