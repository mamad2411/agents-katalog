---
name: verify
description: Prove a change works end to end through acceptance criteria, focused project gates, real user or caller flows, edge cases, and reliability checks. Use before a PR, when the user asks whether a change actually works, or as the first stage of $ship even when automated tests are green.
---

# Verify

Read every applicable `AGENTS.md` before choosing commands or environments.

1. **Acceptance criteria** — Re-read the request or ticket and write down the observable behaviors required. If they cannot be stated without a material product decision, ask for that decision.
2. **Existing gates** — Discover the repository's commands. Start with the smallest relevant tests, typecheck, lint, diagnostics, and build checks for the changed code. Expand to broader suites when repository convention, change risk, or the user's request requires them. A relevant regression blocks verification; label unrelated pre-existing failures separately.
3. **Drive it end to end** — Exercise the public interface as a user or caller would:
   - UI: use `$agent-browser` for the real flow and screenshots unless project instructions mandate another runner. Load its current core workflow before browser commands.
   - API: send real requests to a local or designated test environment, cover success and error paths, and inspect responses and test-state persistence.
   - CLI: run the command through its public entry point with valid and invalid input.
   - Library: consume the public API from a focused scratch or existing integration test.
   Use repository verification scripts, seed data, and QA documentation when available.
4. **Sweep edge cases** — For each touched input or state, consider empty, null, zero, boundaries, duplicates, double-submit or retry, dependency failure, and wrong permissions. Establish the expected outcome and add tests for credible regression risks.
5. **Check reliability** — Determine what happens if work is interrupted, whether production errors are diagnosable, whether new external calls have bounded timeouts and retries, and whether migrations have a documented recovery path. Inspect these properties; do not perform destructive recovery tests without explicit authorization.

Do not send mutating requests to production or another external system unless the user explicitly authorized that exact target and action. If credentials or the environment prevent a check, state precisely what remains unverified instead of reducing the claim to "tests pass."

Report broken behavior first, then acceptance-criteria pass or fail with evidence, edge-case outcomes, relevant command results, screenshots, and remaining risk.
