---
name: verify-change
description: The required verification gate — prove a change works by running the software and observing real behaviour, then record it with scripts/verify.sh so a receipt exists. Tests passing is not verification. Use before every commit, push, PR and merge of a behavioural change. Trigger words — verify, verification, confirm it works, does it work, run the app, smoke test, manual test, validate, receipt, gate, before push.
---
# Verify change (run it, look at it, record it)

**Use when:** any change that can alter what the software does — before commit, push, PR or merge.
**Owners:** qa-test-engineer, and every agent that writes code.

Verification here is **executable**. `scripts/verify.sh` runs this project's contract from `vantry.yml`,
captures real exit codes, and writes the one artifact that counts:
`.vantry/receipts/<branch-slug>.verify.json`. **The receipt is the output of this skill. Prose is not.**
This page is the human-readable half — what to run, what to look at, how to judge it. The receipt carries a
`tree_digest` of every non-trivial changed file, so one more edit makes it stale and the gate blocks again.

> A change is not done until scripts/verify.sh has written a passing receipt matching the code as it stands
> now. A green test suite is not a verification. If you cannot run the software, write the single word
> UNVERIFIED and stop — do not describe the change as working, done, fixed, ready, or verified.

## Procedure
1. **State the expected user-visible behaviour** in one line: what a user can now see or do that they
   couldn't (or the bug that must no longer reproduce). No line, no verification — you have nothing to check.
2. **Confirm `vantry.yml` declares `run.smoke`.** If it is missing or empty, **STOP**: verification is
   **UNDEFINED** for this project. Say so, then help declare a real smoke command (table below) and
   `run.start` / `run.ready` / `run.logs` if the software is long-running. Never fall back to the test suite
   — that is the exact substitution this whole system exists to prevent. `verify.sh` exits **2** on an empty
   smoke.
3. **Run `scripts/verify.sh`** (`--smoke` for a fast re-check after a trivial retry). It executes test →
   build → start/ready → smoke and writes the receipt with each step's exit code and output tail.
4. **Drive the flow yourself and LOOK.** The receipt proves commands exited 0; only you can confirm the
   software did the *thing*. Web → the browser, Playwright or `curl` on the real route. Service → real
   requests, assert status codes and response bodies. CLI → the real invocation, check exit code and diff
   stdout against expected. Library → a script that imports the **built** artifact, not the source.
   Use the real data path, not a mock, wherever feasible.
5. **Check logs, console and network.** A green screen with a 500 in the log is **not** a pass.
   `verify.sh` scans `run.logs` for error lines and records them in `log_scan.errors` — read that field, and
   read the browser console and network tab yourself for anything it cannot see.
6. **Record it:** `scripts/verify.sh --observe "<expected>" "<what you actually saw>" [artifact ...]`.
   Quote real output, a real log line, a screenshot path. It fails if no receipt exists — you cannot narrate
   a run that did not happen — and refuses an observation under 20 characters.

## What "exercised" means, per project_type
| project_type | exercised means | a real `run.smoke` |
|---|---|---|
| web | a browser drives the actual route and asserts rendered state | `pnpm exec playwright test tests/smoke.spec.ts` |
| service | real HTTP/RPC calls against the running process, status codes asserted | `bash scripts/smoke.sh` |
| cli | the built binary is invoked with real args; exit code + stdout asserted | `bash scripts/smoke.sh` |
| library | a consumer script imports the **built** package and calls it | `node scripts/smoke.mjs` |
| mobile | the app launches on a simulator/device and the flow is driven | `pnpm exec maestro test .maestro/smoke.yaml` |
| game | the build boots and a scripted play session reaches a known state | `Unity -batchmode -runTests -testPlatform PlayMode` |
| embedded | the firmware is flashed (or run in a simulator) and the device answers | `pio test -e native` · `pio run -t upload && pio device monitor` |
| contract | the contract is deployed to a local chain and its behaviour asserted | `forge test` · `anchor test` |
| data | the pipeline runs on a fixture and the output rows/schema are asserted | `bash scripts/smoke.sh` |
| data | the pipeline runs on a real sample and the output is asserted | `bash scripts/smoke.sh` |

## Verdicts
Exactly three. There is **no fourth verdict meaning "probably fine"**.

- **VERIFIED** — the receipt says `verdict: pass`, its `tree_digest` matches the code as it stands now, and
  `observation.observed` holds a real quoted observation. Only now may you call the change done.
- **FAILED** (hand it to `debugger` via `debug-issue` — it reproduces before it fixes, and the failing
  output you captured is its input) — it ran and did not do the thing. Say so plainly, paste the failing output and the relevant
  `log_scan.errors`, and hand it to the agent that owns the code to debug. Do not soften it, do not retry
  blindly, do not report progress as success.
- **CANNOT_VERIFY** — you could not run it (no smoke declared, missing credentials, no device, sandbox
  denies the port). State the reason, write **UNVERIFIED**, and **stop**. Escalate; do not proceed to push.

## Guardrails
- Never report "works" from a passing test suite. The suite proves logic; `run.smoke` proves the software.
- Never write, edit or hand-craft a receipt. **Only `scripts/verify.sh` may write one** — the Bash guard
  denies anything else, and forging evidence is the one unrecoverable offence here.
- Never use `--override` to get past a red run. It is a **committed, reviewed decision** with a written
  reason, not a way to unblock yourself.
- Leave nothing behind: no stray dev server, no seeded test rows, no half-written fixture.
- If the gate blocks you **twice**, stop looping and escalate to the human with the receipt's failing step.

## Done when
- `.vantry/receipts/<branch-slug>.verify.json` exists for this branch, and
- its `verdict` is `pass`, and
- its `tree_digest` matches the current working tree (`scripts/verify.sh --status` prints `freshness : CURRENT`), and
- `observation.expected` and `observation.observed` are set, and `observed` quotes something you actually saw.
