---
name: rules-shipping
description: Binding personal rules for finishing a change — load after code changes and before calling work done, writing/choosing tests, opening/updating a PR, releasing, merging, post-merge/deploy checks, or sending any Slack/DM message.
---

# rules-shipping

These rules are binding (moved verbatim from ~/.claude/CLAUDE.md). Each heading names its full-text file in `~/.claude/rulebook/`: **Read that file before acting in its area** — the one-liners are the trigger, not the whole rule.

## Post-Code Impact Check — `13-post-code-impact-check.md`
- After any change, before done/PR: callers & dependents; behaviour deltas; referenced targets exist; before removing a backfill/cron/"one-off" verify the write path populates the data; backward compat with prod client; state what's unverified. Run gates, fix regressions first.
- **Server gate needing a new client input is half a change**: enumerate every caller (incl. deployed bundles), open client PRs in the same session, write enable order (clients → server requires → secret/flag last) into both PR bodies.

## Release Safety — `19-release-safety-rules.md`
- Follow the release-safety skill; a backend release is valid only if the current prod app keeps working.

## Testing — `28-testing-rules.md`
- New endpoint → e2e happy path; critical flows (auth, payments, money/contract) → happy + error e2e; config-mismatch bugs → a test that would have caught it.
- Test only what matters: no junk (glue, constants, library behaviour, mock-only, permutation matrices); **no bystander tests** for code the diff didn't touch; smallest set proving the contract; prefer existing route-harness files.
- HTTP-layer only (supertest / route harness; outermost boundary for non-HTTP). Unreachable through HTTP → no test, prove by running the real thing. Never add cases to an existing forbidden-class (unit/helper) test file.

## Release Readiness & Pre-PR — `29-release-readiness.md`, `30-pre-pr-checklist.md`
- Env vars declared + validated; migrations run on clean DB; no NODE_ENV branching; smoke/e2e for primary flow; local migrations applied before schema testing.
- No env var without `.env.example` + schema; no schema change without migration; no edits to committed migrations; integrations config-driven.

## Post-PR / Post-Merge — `31-post-pr-post-merge-follow-up.md`
- Own the change until verified in the target env. Monitor checks; fix CI on the same branch.
- **Slack**: never post unprompted. A channel send needs (1) the send instruction + (2) the target → then send without re-confirming wording. **DMs always get confirmed first** (draft + recipient + wait for yes). Iterating on a draft is not a send order.
- **Slack style** (first time): English, **<300 chars hard**, line breaks always (one item per line, link at line end — every PR/issue a full URL, never a bare `#123`; URLs may push the cap), `Hello <Name>,` … `Thank you.` for reports to a person (not for PR-review pings), first person with explicit "I", scannable bullets, sparse bold on the ask, one line on what was verified, a line for what you deliberately didn't do + why, approval requests name the irreversible bit, link don't re-explain.
- After merge, confirm the deploy run went GREEN (`gh run list --branch <rc|master>`); a red shared pipeline is yours to surface + fix even if it predates you. Verify behaviour in RC/prod; blocked by access → ask for the specific account/record; never store prod secrets; report env checked + evidence + limits.
