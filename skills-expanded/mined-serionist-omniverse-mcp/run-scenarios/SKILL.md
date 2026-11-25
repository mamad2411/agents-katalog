---
name: run-scenarios
description: >-
  Use when a maintainer asks to run the AI scenario suite ("run the scenarios", "run phase 15 on 8212", "the scenario
  run before the release", "run the outcomes", "how did the last scenario run go"). Checks the Kit app a run would
  drive, runs test_project/scenarios.md's phases, each in a headless Claude Code tester of its own, and
  test_project/outcomes.md's outcomes, each a request an agent gets alone and a read-only judge checks, compares the
  rows with earlier runs' and reports the regressions, each FAIL and WARN, and the skills and calls the agents chose.
---

# Run the AI scenario suite

The scenario suite checks what an AI client gets from the tools, their answers and the plugin's skills, where the
pytest live suites check the bridge. `tools/scenarios.py` does the work: each phase runs in a headless Claude Code
tester that has only this checkout's server and the plugin's skills, against a Kit app of its own, and the session
running this skill sees only the summary. Each outcome is a request in a user's words: an agent gets it alone and
chooses its own tools, then a judge with the read-only tools checks what it did. Why it works this way:
`docs/plans/2026-11-01-scenario-skill.md` and `docs/plans/2026-11-02-outcome-scenarios.md`.

## Steps

1. **Scope** from the request: the phases (`15`, `15-16`, `18-21,24`; every phase when none is named; `none` for
   outcomes alone), the outcomes (`--outcomes all`, `none` or `O1,O3`: every one in a run of every phase, none in a
   run of some unless named), the port (8212 unless the maintainer names one), and a budget in USD or a model when
   asked. `uv run tools/scenarios.py run --phases <phases> [--outcomes <outcomes>] --dry-run` shows the sessions,
   the setup scenarios a partial run adds from each phase's `Needs:` line, each prompt and each kind's command line,
   without Kit.
2. **Check the Kit app:** `uv run tools/scenarios.py check`, adding `--port <port>` only for a port the maintainer
   named.
   - No Kit answers: say what one needs (the command prints it), and ask the maintainer to start one or to approve
     their command for it.
   - A refusal (port 8211, a stage someone may care about, a bridge that differs from this checkout's, another run's
     lock file): report it; its override (`--allow-port-8211`, `--any-stage`, `--any-bridge`) only on the
     maintainer's word.
3. **Run:** `uv run tools/scenarios.py run --phases <phases>`, with `--outcomes` as scoped, the same `--port` and any
   override the maintainer gave `check`, and `--budget` or `--model` as asked. The phases take about 25 minutes and
   $9 with `claude-opus-5-5`, summed from two partial runs in the scenario-skill plan's step 9; the six outcomes about
   4 minutes and $1.40 to $1.70 more, from the outcome plan's step 8. Start it in the background where
   the client can, else give the maintainer the command for a terminal of their own. It prints each session as it
   ends, then the run's folder.
4. **Compare:** `uv run tools/scenarios.py compare` sets the newest run against the earlier ones; before a release,
   `--against <the last release's tag>` sets it against the run made on that release's tree, from a clean tree on
   its PR's final head, or `--against <its folder>`, which that release's PR names, when the tag's tree differs.
   While no release has a run, plain `compare`, which sets it against the earlier runs, and say so. A release PR
   names its run's folder. It exits 1 on a regression or a scenario not run.
5. **Report** to the maintainer: compare's counts and skill loads; each regression, FAIL and WARN with its note and
   capture; for each FAIL, what the session's transcript (`transcript-<session>.jsonl` in the run's folder) shows the
   tester called; for each outcome, `results.md`'s Outcomes row, the skills and calls its agent chose, and a WARN
   its `Calls:` line gave. A status that moved while the tool's answer in the transcripts stayed the same is two testers'
   judgement, not a fix or a regression: say so. Before a release, read each regression's answer in both runs'
   transcripts: in step 9, 15.1 to 15.3 went FAIL, WARN, FAIL over three runs with the same answers, so compare's
   exit 1 alone proves nothing. A PR that ran it quotes compare's output. An issue for a finding only on the
   maintainer's word.

## Done means

- The run's `results.md` exists, and the maintainer has compare's output and the findings.
- Or no run started, and the maintainer knows which check refused it and why.

## Never

- Port 8211 or an override without the maintainer's word: 8211 is their own Kit app, and a run wipes the stage.
- Start a Kit app, or set `OMNI_KIT_ACCEPT_EULA`, on your own (`AGENTS.md`, Build and test).
- Run beside the live suites or another session on the same Kit app.
- Commit anything under `test_project/results/`, or edit a finished run's files.
- Run a tester by hand with tools pre-approved: the script builds its command line and checks its first event.

## Traps

| What broke | When | The guard |
|---|---|---|
| Under `--strict-mcp-config` the plugin's own server never started, and the tester SKIPped every scenario | the plan's step 2, 2026-11-01 | The server comes from the run's `mcp.json`; the init check stops a session without it |
| The tester got the maintainer's auto-memory, the repo's skills and its `CLAUDE.md` files | the plan's step 2, 2026-11-01 | No settings source, `CLAUDE_CODE_DISABLE_AUTO_MEMORY=1`, and the init check |
| `check` refused a bridge copy whose code was the same: it came from an older Windows checkout, with CRLF line endings | the plan's step 9, 2026-11-01 | Files are hashed as git stores them, CRLF as LF |
| A run stopped in Phase 16, Kit silent for 141 s: the tester's own `execute_script` imported the bridge's handler and waited across frames, holding Kit's main thread | the plan's step 9, 2026-11-01 | The tester's rules forbid such code (`test_project/AGENTS.md`); the stop names the call in flight |
| A FAIL's capture was another session's: each session's server numbers its files from 1, and they shared one folder | the plan's step 9, 2026-11-01 | Each session writes to `mcp_output/<session>/` |
