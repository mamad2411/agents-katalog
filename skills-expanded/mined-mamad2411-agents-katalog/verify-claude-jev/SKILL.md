---
name: verify-claude-jev
description: >
  Drive and prove claude-jev (Claude Code plugin) the way a user/session would:
  isolated HOME, stdin JSON hooks, jev CLI, and compaction rows bridge. Use for
  /verify-claude-jev, verifying hook fail-open, routing, rules, compaction, or
  the jev CLI and stats script after changing scripts/.
---

# Verify claude-jev

claude-jev is a Claude Code plugin. Users do not open a web UI; they install the
plugin and Claude Code invokes Python hooks on stdin JSON. Agents also call
`scripts/jev.py`, and `scripts/stats.py` scores live decisions (driven here
via `control-jev stats`). This skill drives those surfaces from the shell with
an isolated `HOME` so a verification run never shares `~/.claude` logs and
caches with a live session.

Maintain the feature map under `features/` as the app changes. Use
`/maintain-verification-skill` to refresh entry points, selectors/commands, and
gotchas when hooks or skills drift.

## What this skill proves here

**In-band (proved by this skill's own launch → doctor → drive → cleanup loop):**

- `python3 -m compileall` over `scripts/` and `eval/`
- Hook stdin contract: empty/malformed events and no-key fail-open exit `0`
  without live classify (silent stdout)
- `src/compactor.ts rows` bad-input fallback, pin-tail keep (no Jev call), and
  no-key multi-row Jev-error fallback (`fallback` when >`PIN_TAIL` rows need
  judging and both `TYPESAFE_API_KEY` and `OPENROUTER_API_KEY` are unset)
- `jev.py` missing-key exit `2`, `status`, and the pinned-provider key rule
- Each command hook's on/off toggle (`CLAUDE_PLUGIN_OPTION_<FIELD>=false`): no Jev
  call, for `PROMPTROUTER`, `SUBAGENTROUTER`, and `RULES`. **Not** `COMPACTION` —
  `src/compactor.ts` has no gate and that toggle lives only in `register.ts`, so it
  cannot be proved in-band.
- `stats.py` on an empty home
- `comparators.py which` naming the pinned version under the verify home, and a
  rules judgment that completes with no ast-grep installed (`sg: none`)
- Bash snapshot hooks recording a shell write as a turn hunk, and marking the diff partial outside git

**Out-of-band (needs a real key; the pane and `/compact` also need Claude Code):**

- A real Claude Code session with the plugin loaded (`claude`, function hooks,
  trusted workspace)
- Live Jev classification / routing / rule judgments. These need a real
  `TYPESAFE_API_KEY` or `OPENROUTER_API_KEY` but **not** Claude Code: with a key
  in the environment, `control-jev hook` drives the router hint, the subagent
  route, the brief-check denial, the rule block and its budget, `jev noul`, and
  the populated `stats` report. Without a key those paths are unproven, not
  failing.
- End-to-end `/compact` through `hooks/register.ts`, and the `/claude-jev`
  settings pane (see `features/settings-pane.md`) — the only paths that need a
  real interactive Claude Code session.

Do not report an out-of-band path as verified because the in-band fail-open
path passed. Feature files mark live entries **out-of-band**; run those on a
machine that has a real key, and remember that the settings pane and
function-hook `/compact` additionally need Claude Code itself.

## Launch

There is no long-lived server. Launch means: create a disposable home, point
`CLAUDE_PLUGIN_ROOT` at this checkout, and record a run id. Ready when
`control-jev doctor` exits 0.

```bash
export PATH="$PWD/.cursor/skills/verify-claude-jev/bin:$PATH"
# TYPESAFE_API_KEY / OPENROUTER_API_KEY are out-of-band for live classify;
# without either, hooks fail open
control-jev launch
# prints run_id=... home=/tmp/jev-verify-... evidence_dir=... ready=1
# subsequent control-jev commands read the active run from the control state file
# force a specific id with JE_VERIFY_RUN_ID=... (must match [A-Za-z0-9._-]+,
# no `..`); reuse the last home with launch --reuse
eval "$(control-jev env)"   # exports CLAUDE_PLUGIN_ROOT (+ run vars after launch)
```

Teardown is `control-jev cleanup` (see Cleanup). Never drive an instance whose
verify home was not created by `control-jev launch` for this run.

Isolation: each run uses `VERIFY_HOME=/tmp/jev-verify-$RUN_ID`; child
processes see that path as `HOME`, and `control-jev` also pins
`CLAUDE_CONFIG_DIR=$VERIFY_HOME/.claude` for every child. That pin matters:
`jev.config_dir()` prefers `CLAUDE_CONFIG_DIR` over `~/.claude`, so an inherited
one (this repo's AGENTS.md tells agents to export it for hand-fed hook events)
would silently send every log, cache, and rule-count assertion in the feature
map somewhere else. Consequence for you: a run's state lives in
`$VERIFY_HOME/.claude/`, and bypassing the harness — calling
`python3 scripts/…` directly with only `HOME=` set — re-exposes the hole, so
add `env -u CLAUDE_CONFIG_DIR` there. Active-run state lives under
`$XDG_RUNTIME_DIR/jev-verify-control` when set, otherwise
`/tmp/jev-verify-control-<uid>` (mode 0700) — never a world-writable shared
path. The state file is a validated `RUN_ID=` line only (never `source`d).
Prefer `eval "$(control-jev env)"`, which exports recipe vars without
touching `HOME`. Do not point two drives at the same verify home.

## Doctor

Read-only check that the active run is worth driving:

```bash
control-jev doctor
```

Requires: `python3` compiles `scripts/` and `eval/`; empty stdin to
`src/prompt-router.ts` exits 0 with empty stdout; empty stdin to
`src/compactor.ts rows` exits 0 with a JSON `fallback`; disposable verify home
exists. Writes `$EVIDENCE_DIR/doctor.txt`. Fail the run if `doctor=fail`.

`TYPESAFE_API_KEY` and `OPENROUTER_API_KEY` may both be unset. Doctor reports
`typesafe_api_key=unset` and `openrouter_api_key=unset` and still passes —
fail-open without a key is the in-band expectation. Live classification is
out-of-band; see feature files. Doctor also runs `comparators.py which` and
records the result as `comparators_which=`: `(none)` on a home with no
ast-grep, which is the state every comparator must degrade to.

**Read those two key lines before driving anything.** `control-jev` passes the
caller's environment through, so on a machine that has real keys the no-key
recipes silently become live calls: they cost money, they append real rows to
the verify home, and an empty stdout then proves nothing about fail-open. If
doctor prints `set`, start every in-band recipe with
`unset TYPESAFE_API_KEY OPENROUTER_API_KEY CLAUDE_PLUGIN_OPTION_TYPESAFEAPIKEY`
in the same shell — the third is the pane-saved key, it resolves a provider on its
own (`status` then reports `"key": "saved"`), and a "no-key" fixture with it set
makes a real call. A bare
assignment does not reach the child either way — use `export` when a recipe
wants a fake key), and run the live recipes in a shell that keeps the keys.

## Drive

Harness: `control-jev` (shell). Prefer it over raw python so verify home and
evidence paths stay consistent.

Before any recipe JSON that expands `$CLAUDE_PLUGIN_ROOT` (or other run vars),
load the exportable assignments:

```bash
eval "$(control-jev env)"
```

`control-jev env` always prints `export CLAUDE_PLUGIN_ROOT=…` for this
checkout. After `launch`, it also prints `RUN_ID`, `VERIFY_HOME`, and
`EVIDENCE_DIR`. It never exports `HOME`.

```bash
# Hook with a JSON event argument (or pipe JSON on stdin with no arg)
control-jev hook prompt_router '{"prompt":"hi","transcript_path":""}'
control-jev hook subagent_router '{"tool_input":{"prompt":"find callers of foo","subagent_type":"Explore"}}'
control-jev hook rules '{"hook_event_name":"PostToolUse","cwd":"'"$CLAUDE_PLUGIN_ROOT"'","tool_input":{"file_path":"'"$CLAUDE_PLUGIN_ROOT"'/scripts/jev.py","old_string":"x","new_string":"y"}}'

# Compaction rows bridge
control-jev rows /path/to/event.json
# or: control-jev rows < event.json

# Jev CLI missing-key (in-band). Live noul needs TYPESAFE_API_KEY or
# OPENROUTER_API_KEY (out-of-band).
control-jev jev -- noul "Is this a yes/no check?" "state text"
control-jev stats -- --days 7
```

Stable handles: script paths under `scripts/`, JSON field names Claude Code
sends (`prompt`, `tool_input`, `hook_event_name`, `messages`), and CLI
subcommands listed by `python3 scripts/jev.py --help`. Prefer those over
scraping log prose.

Feature recipes live in `features/`. Start from the baseline in
`features/README.md`, then follow one feature file end to end.

## Evidence

Proof root for a run (named location; survives cleanup):

`.cursor/skills/verify-claude-jev/artifacts/<RUN_ID>/`

Override with `JE_VERIFY_EVIDENCE` if needed. Capture:

- Command, stdout, stderr, and exit code for every drive step.
- The JSON event fed to a hook (action) and the hook's stdout (result).
- For compaction: the `messages` or `fallback` object, plus proof that
  pin-tail keep, bad-input fallback, or no-key multi-row Jev-error fallback
  matches the feature file (including `fallback-nokey.json` when that path ran).
- For mutations of disposable state under `$VERIFY_HOME/.claude/`: a second
  read of the file after the action. The three command hooks append decision rows
  only when Jev answers, so an empty log means no answer — but `src/compactor.ts rows`
  appends a `"source": "rows"` line to `jev-compact-log.jsonl` on every keep,
  **including the zero-call pin-tail keep**, so that file is not a live-call counter.

```bash
control-jev evidence doctor.txt
control-jev save session-compaction/rows-out.json -
```

Standards: exercise the real stdin/CLI path Claude Code or the agent uses —
not internal setters. Capture the action and the resulting state. Mocks only
at the production boundary already used by the plugin (missing
`TYPESAFE_API_KEY` and `OPENROUTER_API_KEY` → fail open / `jev: set
TYPESAFE_API_KEY or OPENROUTER_API_KEY` unpinned). When proving a no-key path, observe
the real surface: hooks stay silent at exit 0; `jev` CLI exits 2 with the
set-key message; `rows` no-key multi-row fallback exits 0 with JSON
`{"fallback":…}` (e.g. `jev: Error: every chunk failed`) — not silence or exit 2. A
key saved in the `/claude-jev` settings pane does not apply here:
Claude Code hands it to hooks as `CLAUDE_PLUGIN_OPTION_TYPESAFEAPIKEY`, and `control-jev` runs the scripts directly.

In-band evidence proves compile + fail-open / pin-tail / no-key multi-row
Jev-error fallback / missing-key. That Jev-error fallback still has no API
key and is not live classify.
Out-of-band evidence (live classify, real `claude` session, function-hook
compaction, the `/claude-jev` settings pane) belongs on a machine with
Claude Code and `TYPESAFE_API_KEY` or `OPENROUTER_API_KEY`; do not treat an
empty fail-open transcript as that proof.

## Cleanup

```bash
control-jev cleanup
```

Removes only `/tmp/jev-verify-$RUN_ID` for the active run and clears the
control state file. Does **not** delete `.cursor/skills/verify-claude-jev/artifacts/<RUN_ID>/`.
After cleanup, confirm evidence still exists:

```bash
test -d .cursor/skills/verify-claude-jev/artifacts/<RUN_ID>
ls .cursor/skills/verify-claude-jev/artifacts/<RUN_ID>
```

`cleanup` empties the single active-run slot, so a later run's cleanup leaves an
earlier run unaddressable by `control-jev save` (`no active run`) even though its
home and evidence are still on disk. Re-adopt it before writing more evidence:
`JE_VERIFY_RUN_ID=<that run id> control-jev launch`.

Never `pkill` by script name. Never remove another run's home.

## Cost

Every live recipe calls `api.typesafe.ai` (or OpenRouter) with the key in your
environment and spends real money; one rules edit event is several chunked
calls. Prove a live path once per audit, keep the run's logs, and read them for
the rest (`jev-router-log.jsonl`, `jev-calls.jsonl`) instead of re-driving. Do
not launch a second run to confirm a line a finished run already produced, and
never hand a live recipe to a helper agent: one coordinator drives, or the same
fixture gets billed once per helper.

## Helpers

Executable: `.cursor/skills/verify-claude-jev/bin/control-jev`

```bash
control-jev launch|doctor|env|cleanup|status
control-jev hook <prompt_router|subagent_router|rules> [json]
control-jev rows [json-file]
control-jev jev -- <jev.py args...>
control-jev stats -- <stats.py args...>
control-jev evidence <relpath>
control-jev save <relpath> -
control-jev help
```

Put `bin/` on `PATH` for the session, or invoke it by absolute path from the
repo root.

## Feature map

See [features/README.md](features/README.md). Drive one mapped feature per
proof unless the task asks for coverage.
