---
name: confidence-gate
description: When you're about to claim success ("fixed", "done", "works", "passing tests") at the end of a turn, verify the claim is backed by actual evidence in this session. presence's Stop hook will flag a success claim that has no recent test/build pass behind it. Be aware of this gate and either run the verification, or hedge the claim explicitly.
---

# Confidence gate: claim what you can verify

`presence`'s Stop hook parses your final assistant message for unhedged success language. If it finds words like "fixed", "done", "works", "passing tests", and there's been an edit but no passing test/build event since that edit, it logs the discrepancy. In strict presets it also re-prompts you to verify before stopping.

## How to avoid the warning

Three options, in order of preference:

### 1. Actually verify

Run the test suite, build, lint, or whatever the project uses for verification, **before** declaring success. The presence event log captures `npm test`, `pytest`, `cargo test`, `tsc`, `next build`, and ~15 other common commands automatically. Running any of them creates a `test_pass` / `build_pass` event that satisfies the gate.

### 2. Hedge explicitly

If you can't run the verification (no tests in the project, network-isolated environment, user wants quick scaffold without running CI), hedge the claim:

- "I think this fixes the issue, but I haven't run the tests."
- "This should work; needs verification."
- "Untested: ..."

These hedges are recognized by the gate and disable the warning.

### 3. Don't claim what you didn't do

The cheapest fix: don't say "fixed" if you only edited the file. Say "made the change to X; please run the tests to confirm."

## Why this matters

The single most common mode of agent failure is asserting completion when the work isn't actually verified. The user trusts the assertion, ships the change, and discovers the regression later when it's expensive to roll back. The gate exists to make this failure mode visible *before* the session ends.

## Settings

The gate intensity is set by the active preset (see `/presence-preset`):

| Preset | Commit gate (PreToolUse) | Stop gate |
|---|---|---|
| `solo-dev` (default) | off | silent (logged to confidence.jsonl, surfaced via /presence-doctor) |
| `team-oss` | warn (advisory message into context, no interruption) | silent |
| `enterprise-strict` | block (refuses commit until verified) | block (re-prompts on unverified success) |
| `zerotrust` | block | block |

The Stop-hook detection always runs as long as `confidence.enabled` is true (default). Only the *response* to a detection (silent log vs hard block) varies by preset.
