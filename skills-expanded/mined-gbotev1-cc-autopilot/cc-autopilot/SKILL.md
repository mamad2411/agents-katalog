---
name: cc-autopilot
description: Run cc-autopilot, a perpetual autonomous AUDIT/GENERATE→TRIAGE→BATCH→FIX→VERIFY→REVIEW→COMMIT loop that holds every change to a configured quality bar through a judge panel. Its fixers each own a file-disjoint slice of the tree so no two can ever touch the same file, and nothing unverified reaches git. Works on a web app via browser judges, or a CLI, library, or service via a gate suite. Use when the user says "run cc-autopilot", "run the sprint", or "execute the plan", or wants to autonomously drive a project toward its quality bar wave by wave. Requires a cc-autopilot.config.json at the repo root.
---

# cc-autopilot: autonomous polish sprint

This skill turns the current session into the **manager** of a cc-autopilot run: a perpetual,
self-correcting loop that holds every change to a configured quality bar through a judge panel, then
restocks its own queue with net-new features and intuitiveness wins each time it empties. The fix
agents run sequentially per file-disjoint component and never write the same file, while the panel
(audit/generate/verify) is what fans out; no unverified-failing change ever lands in git. It runs on a web app via browser judges, or a CLI, library, or service via
a gate suite.

## Before you start

1. **Confirm the config exists, then run the doctor.** Read `cc-autopilot.config.json` at the repo
   root. If it's absent, the project hasn't been onboarded; point the user at
   `cc-autopilot/cc-autopilot.config.example.json` and `cc-autopilot/config.schema.md`, and offer to
   scaffold it. Do NOT proceed without it. Then run **`node cc-autopilot/scripts/check-config.mjs`**.
   It validates the config against the repo (panel seats resolve to real agents, verify-routing
   seats are in the panel, surface keys are real, state-dir parents exist, the board is valid). A
   non-zero exit means a blocking problem the manager must fix before wave 1.
2. **Commit the vendored engine if it is still uncommitted.** `npx cc-autopilot init` writes the
   engine under `cc-autopilot/`, the root `cc-autopilot.config.json`, and the `.gitignore` edit, but
   deliberately never touches git (it is a pure scaffolder). On a freshly-onboarded repo those files
   are untracked, so the loop's very first BASELINE clean-tree assert would fail on them. Land them
   as ONE onboarding commit BEFORE the loop starts, separate from any wave commit. Check
   `git status --short`: if `cc-autopilot/`, `cc-autopilot.config.json`, or the `.gitignore` edit
   are untracked or modified AND no wave has committed yet (`config.paths.wavesDir` is empty / no
   `sprint wave` commit in `git log`), tell the user what you are about to commit, then
   `git add cc-autopilot cc-autopilot.config.json .gitignore` and
   `git commit -m "Onboard cc-autopilot: vendor engine + config"`. Do this ONLY for the scaffold
   itself: never sweep unrelated uncommitted work into it, and never run it once a wave has landed
   (a dirty tree then is a mid-wave state the crash reaper owns, not onboarding). If the scaffold is
   already committed, this is a no-op: skip it.
3. **Read the operating manual.** `cc-autopilot/orchestrator.md` is the full wave-by-wave loop with
   every hard-won environment fact. THIS skill is just the entry point; the orchestrator is the law.
4. **Cold-start read order** (a fresh session WILL otherwise rediscover state the hard way):
   - `config.paths.resume`: where the sprint is RIGHT NOW
   - the latest `config.paths.wavesDir`/wave-NN.md: carry-forward learnings
   - `cc-autopilot/orchestrator.md`: the operating manual
   - `cc-autopilot.config.json`: the project bindings

## The loop (one wave): see orchestrator.md for the full detail

```
AUDIT/GENERATE → TRIAGE → BATCH → FIX → VERIFY → REVIEW → COMMIT   (perpetual)
```

1. **Preflight**: on `config.branch`. In **visual mode**: app up at `config.app.url`; sweep stale
   browser tabs. In **code mode**: no app, no browser, no tab sweep; instead run the `config.gates`
   baseline on BASE to confirm the suite is green before claiming work. In both modes: after
   confirming no prior wave's workflow is still running (the one manual judgment), run `node
   cc-autopilot/scripts/reconcile.mjs`, the crash reaper. It resets stuck cards to `todo`, releases
   every orphaned lock, parks the cursor, and clears the kept-files freeze; a clean board is a
   no-op success.
2. **Refill (when todo is thin)**: convene the panel in BOTH modes concurrently:
   the two generated scripts under `<stateDir>/generated-workflows/` (use the exact paths printed by
   `gen-panel.mjs`). Merge their output
   into `config.paths.triageInput`, run `node cc-autopilot/scripts/triage.mjs`. It refuses to
   refill mid-wave (a held lock, or a cursor phase other than `idle`/`triage`): finish the wave or
   reconcile a dead one first.
3. **Triage**: refine the filed cards: severity, the `files` contention key, `verify`, `blockedBy`.
4. **Batch**: pick one eligible file-connected component for the next dispatch. Cards sharing a
   file stay with one sole-writer agent. Cap the component at a reviewable size. Claim it with
   `node cc-autopilot/scripts/wave-state.mjs claim <wave> '<cardIds-json>'`: it checks eligibility
   (including the kept-files freeze from components accepted earlier this wave), locks the
   component, and writes `config.paths.currentBatch` itself; never hand-write that file.
5. **Dispatch fix**: run `node cc-autopilot/scripts/gen-fix-batch.mjs` (it reads the claim's
   `currentBatch`), then dispatch **by scriptPath** (never by name, since a stale cache returns 0
   agents). Use the generated state path printed by the command, not the tracked template. Record
   the results with `wave-state.mjs verifying '<results-json>'`.
6. **Verify before dispatching the next component**: `check-wired.mjs` first in both modes. In **visual mode** (per card):
   dispatch each seat with the exact `agentType` + `prompt` + `model` `verify-judges.mjs` prints
   (the `agentType`, never the bare seat stem: bundled judges register plugin-namespaced,
   `cc-autopilot:<seat>`, in the session's agent registry) (it probes
   `config.app.url` first; an unreachable app is a server fault that exits 1, never a card
   failure, so start the app and re-run instead of reverting). In **code mode** (per
   component): `verify-judges.mjs --json '<lead-card-json>'` returns the `gates` strategy, then `verify-gates.mjs`
   runs the gate suite for the verdict; its exit 1 (proven red) is the only revert signal; exit 2
   means the verdict is UNKNOWN (a timeout, a signal or interrupt, a gate command that could not
   run, a config/arg defect): keep the work, fix the cause, and re-run. Pass → `wave-state.mjs
   accept` (in code mode it refuses unless the verdict receipts written by `verify-gates.mjs` and
   `check-wired.mjs` cover this exact component AND the exact working tree they verified - each
   receipt carries the tree hash it ran against, so an edit after the gates passed forces a
   re-run - and it deletes them on success); proven red →
   `git restore` that card/component against BASE, then `wave-state.mjs requeue` with the
   critique.
7. **Review**: `/code-review` + `/simplify` on the kept diff (a headless session, where the
   Skill tool refuses them, dispatches an equivalent reviewer subagent per gate instead); file
   derived findings.
8. **Checkpoint**: run `config.gates`, write the wave log, `archive-done.mjs`, then `node
   cc-autopilot/scripts/assert-diff.mjs $BASE '<kept-files-json>'` (exit 0 = the diff is exactly
   the kept union, and it writes the `diff-verdict.json` receipt `checkpoint` demands, so it must
   run BEFORE the commit - it refuses outright once `$BASE` is no longer `HEAD`; exit 1 names
   residue to resolve, or a MISSING kept file with no diff:
   restore it if an edit was wiped, or, after confirming no edit was lost (an already-on-HEAD
   accept, or an over-declared best-estimate scope), re-run with the confirmed files as a third
   JSON-array arg to acknowledge them). ONE commit, then `node
   cc-autopilot/scripts/wave-state.mjs checkpoint` (clears the kept-files freeze and leftover
   receipts; it refuses until the wave is really settled, asserted, and committed, naming any held
   lock, a missing/mismatched diff-verdict receipt, or a
   kept file still dirty vs HEAD), then push `config.pushBranch` (NEVER `config.protectedBranch`
   without explicit approval).
9. **Repeat perpetually**: no clean-and-stop terminus; surface a per-wave summary so the owner
   can steer or pause.

## The two environment facts to respect (don't fight them)

- **`args` is NOT threaded into Workflow scripts**, so the batch + project config are inlined into the
  dispatched script by `gen-fix-batch.mjs` / `gen-panel.mjs` (the board-file handoff). Always
  dispatch by `scriptPath`, never by `name`.
- **The chrome-devtools browser is one shared instance** (visual mode only), so fix workers never
  touch the browser; verification is a separate manager-run phase; sweep tabs to one keeper each
  checkpoint. In code mode there is no browser: verification runs the gate suite per component.

## Always-on (optional)

To keep it progressing without re-prompting, run this skill under the loop skill:
`/loop <the invocation>`. Self-paced: each wake runs a wave (or a few), logs it, commits, and
schedules the next, perpetually, until the user interrupts.

## Guardrails

- Push only `config.pushBranch`. **`config.protectedBranch` (e.g. `main`) is never pushed without
  explicit human approval.**
- A judge that flags a `config.guardrails` item is wrong; the manager drops it to `wontfix`.
- This is a perpetual Opus-driven panel loop, and it does not self-throttle on cost. The user owns the
  spend dial (the `/loop` cadence) and can interrupt anytime.
