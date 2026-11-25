---
name: e2e
description: Run this repo's end-to-end browser scenarios (e2e/scenarios/*.md) or author a new one from a prose description, against an isolated local fake-mind world with an ephemeral data dir. Drives the UI with Playwright (the Playwright MCP tools when present, otherwise a small driver script) and writes a proof bundle to .e2e/runs/<ts>/ with screenshots, accessibility snapshots, console logs and a machine-readable summary. Use when claiming a UI change is done, when verifying a user journey, when reproducing a reported bug, or when asked to add or run a test for a journey.
---

# e2e — scenario runner and author for Souls

The repo's contract is [docs/testing/e2e.md](../../../docs/testing/e2e.md); read it first, it overrides this skill. The pieces:

| Path | What |
|---|---|
| `docs/testing/e2e.md` | Boundaries: isolated browsers only, reserved ports, attempt cap, what a run must save |
| `e2e/config.mjs` | Paths (`e2e/scenarios`, `.e2e/runs`), reserved ports, iteration cap |
| `e2e/scenarios/*.md` | Scenarios: front matter + numbered steps with `expect*` and `screenshot` lines |
| `e2e/local-smoke.mjs` | The local smoke (`e2e/scenarios/local-smoke.md`): boots its own instance on a free port, world list → one world → a person drawn, then tears down |
| `v2/tools/dev/run.sh` | Starts one local world of the new engine on loopback (world, gateway, directory with the dev sign-in, origin, page) in its own folder; no model runs |
| `.e2e/` | Gitignored working state: runs, browsers, scratch drivers |

Scenarios marked with a remote or hardware fixture (for example `client-fixture-arrival`, which needs owned loopback
fixtures, prebuilt bundles and a hardware-GPU browser) are **out of scope for cloud sessions**: say so and stop
rather than approximating them.

## Modes

| Ask | Do |
|---|---|
| `run <scenario-id>` | Run one scenario end to end |
| `run smoke` | Run every scenario with `tier: smoke` that is runnable here, one after another |
| `author <description>` | Explore the journey in a browser, then write `e2e/scenarios/<id>.md` |
| `local smoke` | `node e2e/local-smoke.mjs [--port N] [--clip]`: the quick "does the app work" check; read its `summary.json` |

## Pre-flight

1. Read `docs/testing/e2e.md` and `e2e/config.mjs`. Note reserved ports; never use them for your own world.
   A scenario with a `runner` in its front matter (`local-smoke`) is run by that command, not driven by hand.
2. The world's programs and page: `v2/tools/dev/run.sh` builds what is missing and builds the page from this
   checkout at each start (its head lists what it needs, and how to name prebuilt ones).
3. Browser: Playwright MCP tools (`mcp__playwright__*`) if listed; otherwise a driver script under `.e2e/` that
   loads Playwright the way the harness does (`tools/playtest/lib/platform.mjs` → `resolvePlaywright`, or
   `createRequire('mars/viewer/package.json')('@playwright/test')`, as `e2e/local-smoke.mjs` does). Browsers come from
   `PLAYWRIGHT_BROWSERS_PATH`, `/opt/pw-browsers` when present, or an explicit `.e2e/browsers` cache:
   `PLAYWRIGHT_BROWSERS_PATH="$PWD/.e2e/browsers" pnpm --filter mars-campus-viewer exec playwright install chromium`.
   Never use a signed-in personal browser profile.
4. Read the target scenario in full: front matter (`id`, `tier`, `fixture`, `critical_path`) and every step.

## Running one scenario

### 1. Boot an isolated world
```bash
RUN=.e2e/runs/$(date -u +%Y%m%dT%H%M%SZ)-<id>; mkdir -p $RUN/snapshots $RUN/shots
v2/tools/dev/run.sh --port 4720 --dir $RUN/data > $RUN/world.log 2>&1 &
# wait for `ready http://127.0.0.1:4720` in $RUN/world.log
# → http://127.0.0.1:4720/w/dev/ ; signed in as the test person Ada, the world's creator: …/w/dev/?as=Ada
```
The world is N2's test world (`fixture: testworld`). A scenario on the old page (apps/web, what soul.game shows), or
one naming a genesis template, boots with
`node tools/playtest/arena/new-engine/old-page.mjs --template worlds/templates/<name>.json --dir $RUN/data` instead:
it prints `ready <url>` with the old page on a new-engine world of that template (the proof skill's section 1 says
what it starts and needs). The dev sign-in works on loopback only. Record the URL, pid, port and
commit (`git rev-parse HEAD`, dirty or not) in `$RUN/ready.json`. Boot errors (port taken, missing build) are
relayed verbatim.

### 2. Drive each step
1. **Snapshot first.** Save the accessibility tree to `$RUN/snapshots/step-<n>.yml` and grep it for the role and
   name you need (`grep -nE 'button "Sit"' ...`) instead of reading it whole. Never guess selectors.
2. **Act with real input**: clicks, typing, key presses, pointer drags, touch on the phone viewport. The 3D world is
   a canvas: aim pointer input at visible geometry, and wait for the arrival card to complete first.
3. **Check the step's assertions**:
   - `expect-url` → compare `location.pathname` (and search) against the regex.
   - `expect-api` → `curl -s` the route on the world origin and check status and shape.
   - `expect-console` → collect console errors since the named step; apply any "except matching" regex.
   - `expect` (free-form) → judge from the snapshot or a screenshot. The only judged assertion; keep it narrow.
4. **Screenshots** named in the step go to `$RUN/shots/<name>`.
5. **Waits**: wait for the specific text, element or world state; default timeout 30 s. No fixed sleeps as asserts.

### 3. Repair loop (cap 3 attempts, from `e2e/config.mjs`)
On a failed step:
1. Capture the failure: screenshot, snapshot, console errors, tail of the world log.
2. Write `$RUN/attempt-<n>.md`: one paragraph on what you think broke and what you will change.
3. Fix the code if it is a product bug. If the scenario itself is wrong, edit it and say so in the run notes;
   **never weaken an assertion silently**.
4. Before retrying, re-read `git diff` and every `attempt-*.md` so you do not repeat yourself. Same assertion failing
   twice with no new diff: stop.
5. Fresh boot for every attempt (`kill <pid>`, new run dir); restart from step 1.
6. Before attempt 3, spawn a fresh subagent with only the evidence (attempt notes, scenario path, last screenshot and
   snapshot) and ask for one new root-cause hypothesis different from attempts 1 and 2, with a file:line change, or
   `ESCALATE`. On `ESCALATE`, skip attempt 3 and write the handoff.

### 4. Teardown (always)
`kill <pid>` of the world you started, and only that pid. Never kill a process just because it holds a port.
Remove `$RUN/data` unless the failure needs it.

### 5. Proof bundle
- `$RUN/summary.json`: `{ id, status, commit, dirty, url, steps: [{ n, asserts: [{ kind, ok, detail }] }], screenshots }`.
- `$RUN/run.md`: walk-through, assertion table, evidence list. Readable in two minutes.
- If the change is tier T2 or higher (`node tools/proof/tier.mjs`), also record the journey with the `proof` skill;
  screenshots alone do not satisfy T2.

### 6. Terminal states — stop at the first one reached
| State | When |
|---|---|
| **PASS** | Every step's assertions green on a single boot |
| **PARTIAL** | Critical-path steps green, a non-critical assertion red (say which) |
| **FAIL** | Still red after 3 attempts: write the handoff below |
| **ABORT** | Boot cannot work here (missing build, out-of-scope fixture): relay the error, tear down |

Never re-run a passing scenario for reassurance. In `run smoke`, move to the next scenario after each terminal
state and stop after the last one.

## Authoring a scenario
1. Boot a world as above with the template that contains the journey.
2. Explore the journey in the browser; snapshot before every action; note URLs, accessible names, console state.
3. Decide the tier: a critical user path is `smoke`; edge cases and polish are `regression`.
4. Write `e2e/scenarios/<id>.md` from `.claude/skills/e2e/scenario-template.md`. `id` matches the file name.
5. Run it once as a new scenario. Iterate on wording if the first run shows fragility, not on the assertions.
6. Report the file and the run result.

## Long runs in cloud sessions
Foreground commands are capped at 10 minutes. Start anything longer detached and poll:
`nohup setsid node <driver> > $RUN/driver.log 2>&1 &` then check the log with short `tail`/`grep` calls.

## Handoff (3 attempts used)
```markdown
## HANDOFF — e2e <id> (<run dir>)
Status: FAIL after 3 attempts.
| # | Hypothesis | Change | Result |
|---|---|---|---|
Suspected cause: <one paragraph>
Evidence: <screenshot, snapshot, world log tail paths>
Questions for the maintainer: <1–3>
```

## Rules
- Never claim pass without every deterministic check green.
- No model runs: the engine has no mind, and `run.sh` starts none. Nothing here may spend model credits.
- Ephemeral data only; never point a run at a real data dir or a production world.
- Never commit `.e2e/` contents, screenshots or video.
