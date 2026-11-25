---
name: amber-release-gate
description: Run the Pinto Notes release gate (performance, security, storage and network) on a candidate commit and read its report. Use before any App Store submission, TestFlight build for users, Mac release, or production server deploy, when asked whether a build is fast or safe enough to ship, or to compare a branch's performance with the last release.
---

# Pinto Notes release gate

No App Store submission, TestFlight build for users, Mac release or production server deploy goes out
without a passing gate report for that commit in `docs/Evidence/release-gate/` (a short summary; the
full report and raw numbers are in `~/content-tools/projects/amber-proto/release-gate/`). What it measures, the
budgets and why they are what they are: `docs/Technical/release-gate.md`.

## Run it

```sh
scripts/release-gate.sh origin/dev --baseline mac-v1.1.2
```

- The candidate is any ref. `--baseline` is the last release; the newest report for that commit is
  used, and without one the gate runs the baseline first (twice the time).
- About 40 minutes for a full run: two Release builds on this Mac (niced), then 3 accounts × (sign-in
  + 3 measured launches) on fleet-air. Run it in the background and keep working.
- `--only security` (or `perf`, `storage`, `network`, comma-separated), `--sizes 1,2000`, `--runs 1`
  for a quick look. A quick look is not a gate report: say so if you share one.
- It exits 0 on pass, 1 on fail, and prints the report's path.
- What the Mac measured is kept in `build/release-gate/out/<sha>/perf-*.json`. If a later step
  failed, `--reuse-perf` writes the report from it without measuring again. `--rescore <full report .json>`
  scores an existing report against the current budgets.

## Before the first run on a machine

- `Config/Backend.staging.local.xcconfig` (`scripts/staging.sh app-config`), `.secrets/staging.env`,
  and `supabase login` (the advisors and the read-only SQL go through the Management API).
- Xcode signed in with the team's Apple ID (the build is team-signed, like `scripts/release-mac.sh`).
- `ssh fleet-air` works and the Air is awake and unlocked: the app draws on its screen. Nobody may be
  using Amber Notes Beta there; the gate signs it in and out of the bench accounts.
- `gitleaks`, `pnpm`, `deno` on PATH.

## Reading the report

- **FAIL** lines first: over budget, or more than 15% worse than the baseline (past the metric's noise
  floor). Each says what was measured and where.
- Hangs list the step they happened in, and `Hangs, sampled` has the main thread's stack from
  `sample`, symbolicated from the archive's dSYM. Start there.
- "views laid out" counts layout passes per step; idle must stay at 0. A view class that shows up in
  idle, or thousands of passes on a sidebar toggle, is a re-render loop or an over-broad update.
- Server numbers come from staging, which runs whatever was deployed there, not the candidate's
  functions. Deploy the candidate to staging first when its server code changed.

## Rules

- Never launch the app or a test host on this Mac (Emil's screen): measurements run only on fleet-air
  or CI. Building here is fine. Ask before using the Air; Emil uses it too. Processes are stopped by
  exact PID only.
- Staging only. The scripts refuse production's project ref; never point them anywhere else.
- No paid API calls.
- When a budget is wrong (a deliberate trade, a better machine), change `scripts/release-gate/budgets.json`
  in its own commit and say why in `docs/Technical/release-gate.md`. Never loosen a budget to pass a run.
- A new host in the code fails the hosts line until it's added to `scripts/release-gate/hosts.txt`
  with what it is.
