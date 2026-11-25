---
name: verify-ccsn
description: Launch and drive the real cc-safety-net CLI — the hook decision path, explain, status/doctor/statusline, logs, rule and policy config, and the local policy GUI — against an isolated home, capturing evidence. Use when a change needs proof in the running app, not just the test suite.
---

# Verify cc-safety-net

cc-safety-net is a CLI (`cc-safety-net` / `ccsn`) that coding-agent CLIs invoke as a pre-tool-use
hook: JSON describing a tool call arrives on stdin, an allow/deny decision leaves on stdout, and
every decision is appended to an audit log under the active home. Users also run diagnostic
commands (`status`, `doctor`, `explain`, `logs`), config commands (`rule`, `policy`), and a
local web GUI (`gui`).

**Safety invariants for every run:**

- Command strings under test (`git reset --hard`, `rm -rf /`, …) are analyzer INPUT. They go into
  a JSON payload or an `explain` argument. Never execute one in a shell.
- Never run the CLI against the real home. Every invocation goes through `./ccsn-isolated` (see
  Helpers), which redirects `HOME`, `CC_SAFETY_NET_HOME`, and `CC_SAFETY_NET_AUDIT_HOME` into a
  disposable directory. A bare `bun run src/entries/bin.ts` writes to the developer's real
  `~/.cc-safety-net/logs`.
- Never drive `install`, `update`, or `uninstall` (CLI or GUI Integrations tab) in a verification
  run: install detection and npx-cache clearing reach real machine state beyond `$HOME`.
- Run `rule` and `policy` commands from `$WS`, never the repo: without `--global` they write the
  project config under the cwd's `.cc-safety-net/`.

## Launch

No build step: the CLI runs from source with bun. Set up one isolated run:

```bash
REPO=$(git rev-parse --show-toplevel)
RUN_ID=verify-$(date +%Y%m%d-%H%M%S)
export CCSN_VERIFY_HOME=$REPO/artifacts/verify-homes/$RUN_ID   # disposable fake $HOME
EVIDENCE=$REPO/artifacts/verify/$RUN_ID                        # proof artifacts (gitignored)
WS=$CCSN_VERIFY_HOME/workspace                                 # cwd the "agent" works in
mkdir -p "$CCSN_VERIFY_HOME" "$EVIDENCE" "$WS"
```

One-shot commands (hook, explain, status, logs, doctor) need no server — each drive is one
`./ccsn-isolated …` invocation from `$REPO/.agents/skills/verify-ccsn/`.

The only long-lived instance is the GUI:

```bash
cd "$WS" && "$REPO/.agents/skills/verify-ccsn/ccsn-isolated" gui --no-open > "$EVIDENCE/gui.log" 2>&1 &
GUI_PID=$!
```

Ready when `gui.log` contains `CC Safety Net policy GUI: http://127.0.0.1:<port>/?token=<token>`
(poll for it; it appears in under ~2s). The server picks a free port itself, so instances never
collide. Teardown: `kill $GUI_PID` — kill the PID you started, never by process name.

Isolation: two runs side by side are fine as long as each has its own `CCSN_VERIFY_HOME`.

## Doctor

Before driving, prove the instance is worth driving — from the skill directory:

```bash
./ccsn-isolated --version        # must print "dev" — source checkout, not an installed copy
./ccsn-isolated status | head -6 # must print "CC Safety Net — ready" with Level standard
./ccsn-isolated doctor --json --skip-update-check > "$EVIDENCE/doctor.json"
```

If `--version` prints a semver, you are running a packaged copy, not this checkout — stop.
Healthy in `doctor.json` means `engineSelfTest.failed` is 0 and `configState.state` is `"ready"`.
Do not gate on doctor's exit code: under a fresh isolated home it exits 1 solely because no
integration is configured (`integration.none-configured` in `findings`), which is inherent to the
isolation, not a defect. Any other error-severity finding means the checkout is broken — stop and
report rather than driving features — unless your shell exports a host config directory
(`CLAUDE_CONFIG_DIR`, `CODEX_HOME`, `XDG_CONFIG_HOME`, …) that points doctor at real host config;
see [diagnostics.md](features/diagnostics.md).
After the first hook drive, additionally confirm isolation held: entries exist under
`$CCSN_VERIFY_HOME/.cc-safety-net/logs/` and `find ~/.cc-safety-net/logs -name "*ccsn-verify-$RUN_ID*"`
finds nothing (every probe session id starts with `ccsn-verify-$RUN_ID`, so a leak is identifiable
by filename in the real log tree). Match this run's id, not bare `ccsn-verify`: stale files from
older runs can sit in the real tree and would read as a leak.

## Drive

Three drive styles; the per-feature recipes live in [features/](features/README.md).

**Hook (the production path).** Write the payload the coding CLI would send, pipe it in, capture
stdout and the exit code:

```bash
printf '%s' '{"hook_event_name":"PreToolUse","tool_name":"Bash","session_id":"ccsn-verify-'"$RUN_ID"'-reset","cwd":"'"$WS"'","tool_input":{"command":"git reset --hard"}}' \
  | ./ccsn-isolated hook --coding-cli
```

Deny prints `{"hookSpecificOutput":{…,"permissionDecision":"deny","permissionDecisionReason":"…Rule: git.reset-hard…"}}`;
allow prints nothing. Both exit 0 for Claude Code — the decision is the stdout JSON, never the
exit code. `--claude-code` is the legacy alias of `--coding-cli`; `./ccsn-isolated hook --help`
lists every accepted integration flag (payload shapes and exit codes differ per host; see
`src/hosts/<id>/hook.ts`).

**Plain CLI.** `./ccsn-isolated explain --json "<command>"`, `status`, `doctor --json
--skip-update-check`, `logs --json [--all]`, `rule …`, `policy check <file>`. `logs` reads every
project's entries in the active home; narrow with `--session` or `--project`. `explain` reads,
and `rule` and `policy` write, the project config under the cwd's `.cc-safety-net/`
(`ccsn-isolated` runs from your cwd), so run `rule` and `policy` from `$WS`.

**GUI.** Drive the API with curl (`GET /api/policy?token=$TOKEN`; POSTs need the
`x-cc-safety-net-token: $TOKEN` header too), or the page with a browser (playwright-cli or
claude-in-chrome) at the printed URL. Views are hash-routed: `#overview`, `#activity`, `#policy`
(labelled Protections), `#rules` (Custom rules), `#integrations` (Agents), `#settings`; stable
handles are element ids (`#activity-feed`, `#save`, `#tester-open` and the dialog's
`#tester-input`, `#tester-run`, `#tester-result`) and `a[data-nav="<view>"]`.

## Evidence

Everything lands in `$EVIDENCE` (`artifacts/verify/<run-id>/` — gitignored, survives cleanup).

- Exercise the real user path: payloads through `hook --<integration>` exactly as the host CLI
  sends them, not `checkCommand` library calls or internal functions.
- Capture the action and the resulting state: for a hook decision, save the payload, the stdout
  decision, and the exit code, then pair it with the side effect — the audit entry in
  `$CCSN_VERIFY_HOME/.cc-safety-net/logs/<cwd-slug>/<YYYY-MM>/<date>-<session_id>.jsonl` (or its
  absence: plain allows under default policy are also recorded, so assert content, not existence).
- The hook answers; the host enforces. A hook proof covers the decision and the audit trail —
  it cannot prove a file survived, and staging a sentinel proves nothing (this harness never
  executes the command). Survival proofs live in `tests/e2e`, which stage a real host runner.
- An allow proof is a negative: empty stdout AND exit 0 AND an `allow` audit entry for the
  session id. Capture all three — empty stdout alone also looks like a crash swallowed by a pipe.
- GUI proofs: screenshot with the view name visible, plus the API response or on-disk policy file
  (`$CCSN_VERIFY_HOME/.cc-safety-net/policy.json`) showing the mutation stuck.
- Record with every artifact: feature ID, the exact command, and the entry point used.

## Cleanup

```bash
kill $GUI_PID 2>/dev/null          # only if this run started a GUI
/bin/rm -rf "$CCSN_VERIFY_HOME"    # /bin/rm — plain rm may be aliased to trash on this machine
```

Cleanup removes the isolated home and any GUI process this run started — nothing else. Never
delete `$EVIDENCE`, never touch the real `~/.cc-safety-net`, and never kill by process name
(other bun processes are not yours). Run this after failed attempts too.

## Helpers

`ccsn-isolated` (executable, in this directory) runs the CLI from source under the isolated home:

```bash
CCSN_VERIFY_HOME=/abs/disposable/dir ./ccsn-isolated <command> [args...]
```

It requires `CCSN_VERIFY_HOME` to be absolute, redirects `HOME`/`USERPROFILE`/
`CC_SAFETY_NET_HOME`/`CC_SAFETY_NET_AUDIT_HOME` into it, blanks the `CC_SAFETY_NET_LEVEL`/
`STRICT`/`PARANOID*`/`WORKTREE` overrides a developer shell might export (a blank value also
shadows the legacy `SAFETY_NET_*` names), unsets `CC_SAFETY_NET_AUDIT_SCOPE` (`blocked` would
drop the allow entries every allow proof needs, and a blank value is invalid and does the same),
and execs `bun run <repo>/src/entries/bin.ts "$@"` with stdin/stdout/exit code passing through,
so hook payloads pipe straight in. It runs the CLI from your current cwd — `cd` into `$WS` for
cwd-scoped commands like `explain`, `rule`, and `policy`.
