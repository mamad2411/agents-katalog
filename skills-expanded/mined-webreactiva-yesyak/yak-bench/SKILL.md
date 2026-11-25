---
name: yak-bench
description: Internal benchmark of this repository. It takes a small real project, drives a weaker agent (OpenCode in tmux, as a puppet) through the YesYak process to build a feature or fix a bug, acting as the human user, then scores the run, records it in bench/LOG.md, turns the confirmed findings into skill changes and cuts a release. Use it whenever the user asks to run the benchmark, repeat it, "otra vuelta", test YesYak on a project, measure the process, or apply what the last runs found.
metadata:
  internal: true
---

# Yak bench

The goal is always to improve YesYak. A run is evidence; a skill change is the result.

This skill belongs to this repository only. It is not in `skills/`, so `install.sh` never copies it to other projects.

## Roles

- **You are the human.** You choose the project and the task, answer the agent's questions, approve or reject, and correct it when a real user would. You never do its work, never edit its files, and never name a skill or a step that a real user would not name.
- **The puppet** is OpenCode with a cheaper model, or Claude Code (`turn-claude.sh`) when the user asks for it. It sees only the project and a frozen copy of `skills/`: no global skills, plugins, MCP servers or CLAUDE.md (`turn.sh` isolates it). A weaker model shows where the skills are not clear enough.

## Tools

All in `scripts/`. Runs live in `.scratchpad/bench/<run-id>/` of this repository (ignored by git). The clone itself lives in `/Users/Shared/yak-bench/<run-id>` and `repo` links to it: OpenCode reads `.agents/skills` in every parent folder, so a clone inside the user's home would see the user's own skills.

| Script | Does |
| --- | --- |
| `models.py list` | Models that OpenCode offers, with models.dev prices, cheapest first. Banned models never appear |
| `models.py check <model>` | Fails for a banned model (any `kimi k-3`, any `astra`) or one over the price cap (`YAKBENCH_MAX_OUTPUT`, 5 $/M output by default). Old models can be expensive: always check |
| `prepare.sh <run-id> <git-url> [ref]` | Clones the project without its remote, copies the skills, writes `run.json` with the YesYak version |
| `turn.sh <run-id> <message-file> [--model m] [--new-session]` | Sends one human message in tmux session `yak-bench`, waits, prints the answer, keeps every session id in `run.json`. Starts one isolated, password-protected `opencode serve` per run, so background subagents survive between turns |
| `turn-claude.sh <run-id> <message-file> [--model m] [--new-session]` | The same for Claude Code: `--setting-sources project` and `--strict-mcp-config` hide the user's skills, hooks, plugins, MCP servers and CLAUDE.md; HOME stays real for the sign-in. Its models are over the price cap: run it with `YAKBENCH_ALLOW_EXPENSIVE=1` only when the user asks |
| `report.py budget <run-dir>` | Both turn scripts run it before each turn and stop when the turns so far cost the budget: `budget_usd` in `run.json`, else `YAKBENCH_BUDGET_USD`, else 10 $; 0 means no budget. Each turn is priced with its own model (`turn_models` in `run.json`) |
| `report.py run <run-dir>` | Facts of the run: sessions, time, model steps, tokens, equivalent cost, skills loaded, commits, artifacts, tool errors. Saves each session export (the full transcript) in the run folder |
| `report.py flows <bench-dir>` | Per run, the skills the work session used, in order, with the turn of first use. Feeds `bench/FLOWS.md` |
| `archive.sh <run-id>` | Moves a scored run's clone into its run folder, so the next puppet cannot read it next to its own clone. Run it after the report |
| `report.py metrics <bench-dir> [transcript]` | One row per run: turns, steps, wall and agent time, tokens, cost. With your own session transcript (`~/.claude/projects/<project>/<session>.jsonl`), also what you spent as the driver in each run's window |

Run `turn.sh` in the background and wait for it to finish; one turn can take many minutes.

## Pitfalls already met

Each one cost a run. The scripts handle them; check them again when you change a script or add a puppet.

| Pitfall | What prevents it |
| --- | --- |
| The puppet sees the user's skills, plugins or config (OpenCode reads `.agents/skills` in every parent folder; Claude Code loads user settings) | Clones outside the user's home; a fake HOME and a per-run server for OpenCode; `--setting-sources project --strict-mcp-config` for Claude Code; the probe turn |
| The puppet sees the run folder (`notes.md` has the expected behaviour) or the clones of earlier runs | Start the puppet in the real clone path, never in the `repo` link; `archive.sh` after every run |
| The puppet inherits the driver's variables through tmux (session id, a messaging token) | The turn scripts remove every `CLAUDE*` and `AI_AGENT` variable |
| A bench commit in the clone misleads the commit convention detection | No commit: `.git/info/exclude` |
| The fake HOME hides toolchains (rustup) or the project's virtual environment is not active | `turn.sh` passes `RUSTUP_HOME` and `RUSTUP_TOOLCHAIN`, and puts `.venv/bin` on PATH |
| The machine's toolchain is older than the project needs | Install a pinned extra toolchain (for example `rustup toolchain install 1.90.0`) and pass it; never change the default |
| OpenCode's question tool cancels in `opencode run` and tells the agent to assume | Question tool off in the bench config; questions go to the chat |
| A pipe in front of a check hides its exit code; a session export through a pipe is cut | Read `PIPESTATUS` or the check alone; export to a file |
| The project has its own AGENTS.md that needs a web page | Web tools allowed for both puppets |
| A strong model is over the price cap | Only when the user asks, with `YAKBENCH_ALLOW_EXPENSIVE=1` |
| A `.env` copied from `.env.example` sends telemetry (an error tracker DSN) from the clone to the real service | After `prepare.sh`, switch the telemetry variables off in the clone's `.env` before the first test run |
| `OPENCODE_DISABLE_CLAUDE_CODE=1` hides the project's own CLAUDE.md, so the puppet misses its rules (for example a forbidden command) | Check the probe turn lists the project's rule files; if the rules live only in CLAUDE.md, record it and expect the setup to point AGENTS.md to them |
| An edit to `turn.sh` or `turn-claude.sh` while a turn runs: bash reads the script in parts, so the running turn fails after the agent ends (no `run.json` update, no answer file) | Edit the turn scripts only when no turn runs; repair a broken turn with `report.py turn` and the counter in `run.json` |
| A provider quota cuts a turn (for example a 5-hour limit) | The turn ends with a rate-limit error: record it as a harness interruption and resume later in the same session |

## 1. Read the log

Read `bench/LOG.md`: the last version, the models used, and the findings with status `watch` or `fixed`. A `fixed` finding must be checked again in this run; choose a project and task that can show it.

A finding that the last run did not exercise must be forced in this one. Write its trigger in `notes.md` before you start, then create it the way a real user or project would:

| The finding needs | Force it with |
| --- | --- |
| A project state (for example a check that already fails on the default branch) | A project that has that state. Search until one does; never break the project yourself |
| A step that the agent skips (for example the commit skill) | A plain user request that leads there, for example "commit it" |
| A user habit (for example a rule said in the chat) | Say it, the way a user would |

If you could not force it, say so in the run file.

## 2. Choose the project, the task and the model

- **Project.** A public repository from GitHub (`gh api 'search/repositories?q=...'`), small (a few thousand lines at most), with tests that pass on this machine, in a stack that this machine runs (check with `command -v`). Change the stack and the kind of project from run to run. The user can name one.
- **Task.** A feature that fits one iteration, or a real bug (an open issue is best). Alternate features and bugs, so both entry points of `ask-yak` get tested.
- **Model.** Take it from `models.py list`. Prefer cheap and weak models; use OpenAI models with moderation. Ask the user when unsure.
- **Repetitions.** With a weak model (for example a luna, a flash or a nano model), one run proves little. Repeat the same task, or a similar one, before you call a finding confirmed.

## 3. Prepare

1. `prepare.sh <NNNN-short-name> <url>`. Run ids are numbered in the order of the log.
2. Run the project's tests yourself and write the baseline in `.scratchpad/bench/<run-id>/notes.md`.
3. Isolation check: one turn in a throwaway session ("Which skills and instruction files can you see? Only list them."). Only the YesYak skills may appear. Then start the real work with `--new-session`.

## 4. Drive the run

Start the way a real user starts, and let `ask-yak` lead:

1. "I just installed YesYak in this project, set it up." This tests `customize-yak`. Ask it to switch off `browser-acceptance-testing`: browser evidence is out of the benchmark unless the user asks for it.
2. The request in plain words: a feature request, or a bug report as a user would write it. Add one line: "Do not publish pull requests; the PR stays local." The benchmark never publishes a PR, and the clone has no remote.
3. At each checkpoint, answer as the product owner: take the recommended option when it is right, say no when it is wrong. When you do not know what comes next, ask the agent "what now?", as the process says.

Write every intervention in `notes.md`, with the turn number, the kind and your exact words:

| Kind | Meaning |
| --- | --- |
| answer | The agent asked and you answered: expected |
| approve | A checkpoint yes |
| nudge | You told it something the skills should have told it |
| correction | It did something wrong and you stopped it |
| rescue | It was stuck and you unblocked it |
| gate | An autopilot run stopped at a gate and you answered: expected |

Nudges, corrections and rescues are findings. Stop at the end of the Retrospective phase, after the turn limit (default 30), or when `report.py budget` stops a turn. Raise `budget_usd` only when the user asks. A model switch in the middle of a run is a harness interruption: record it, with the turn and the reason.

### Autopilot runs

An autopilot run tests `yak-pilot`: the user gets the work done without naming any skill. Replace step 3 above:

1. Send the request the way the README says: `/yak-pilot <the task in plain words>`, or "yak-pilot: …" when the puppet has no slash commands. Name no other skill, phase or mode. Now and then send a plain request without the name, to measure whether the YesYak block alone starts the pilot. On the first run in a project, answer the profile round as a real user would; in a later session, change the profile in plain words (for example "always ask me before you change existing output").
2. Answer its blocking questions and approve or correct the plan. After that, answer only at the gates it opens. Any other message is a nudge, a correction or a rescue, and it is a finding.
3. Let the run go to its end point. Do not answer a status line.
4. At the end, read the `## Plan` of `progress.md` and `unattended-decisions.md` as a reviewer. Mark each decision taken alone that you would revert (a missed gate) and each gate that no rule justifies (a gate too many). Compare the skills in the plan with the skills loaded (`report.py run`): a skill in the plan that never loaded is a finding.

Cover these requirements before an autopilot finding is confirmed: a clear bug, an ambiguous feature, a risky change (a contract or security), and a second session in the same project after a profile change.

## 5. Score

1. Run the tests yourself. Run `report.py run`.
2. Write `bench/runs/<run-id>.md` (committed): the report, then a table per phase of the process map: reached or not, the artifacts, and whether each one does what its skill asks. Then the interventions, the findings and the cost. For an autopilot run, add a table: skills the user named besides yak-pilot (target 0), blocking questions, spec and plan sized as, planned gates, dynamic gates, decisions taken alone, missed gates, gates too many, approvals without a change per gate kind, skills planned but not loaded, extra messages after the plan approval, and profile changes proposed. Then an "HIL stops" table with one row per stop where the run waited for the human, also when you answered it: turn, where, kind (plan approval, planned gate, dynamic gate, profile rule, setup), the question, your answer.

## 6. Turn findings into changes

Give each finding a class:

| Class | Action |
| --- | --- |
| Skill | Change the skill, following AGENTS.md (one rule in, one out; generic; no example from the benchmark project) |
| Model | Record it. Change a skill only if a cheap, clear rule would help any model |
| Harness | OpenCode or the puppet setup. Record it; fix the tools here if needed |
| Bench | A defect of this skill or its scripts. Fix it |

A skill finding changes a skill when it is confirmed: seen in two runs, or in one run with a strong model, or plainly wrong in the skill text. Otherwise its status is `watch`. After each skill change, run `python3 skills/ask-yak/scripts/check_yesyak.py --dev`.

## 7. Log, commit and release

1. Add the run to `bench/LOG.md`: one row in the runs table, the metrics table again from `report.py metrics`, the skills column of `bench/FLOWS.md` again from `report.py flows` (and a row in its runs table), and new or changed rows in the findings table (`F-NNN`, class, status `watch` / `confirmed` / `fixed in vX.Y.Z` / `verified in run NNNN`, evidence).
2. Commit with `git-commit-organizer`: skill changes (scope `skills`), bench changes (scope `bench`) and the log, each in its own commits.
3. If the skills changed, cut a release: add an entry to `CHANGELOG.md`, bump the version (0.x: minor for a new skill, rule or renamed contract; patch for a fix), and tag `vX.Y.Z` on the commit. Push tags only when the user asks.
4. Tell the user: the run in three lines, the findings, the changes, the new version and the next run you propose.
