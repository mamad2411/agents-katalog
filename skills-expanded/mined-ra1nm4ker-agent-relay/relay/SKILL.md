---
name: relay
description: Check Agent Relay status, handoff readiness, decisions, history, and execution mode for the current managed conversation. Use for $relay, $relay doctor, $relay status, $relay why, $relay history, $relay mode, or Relay profile-switch questions. Not for developing the Relay repository.
---

Use the installed Relay CLI to answer from actual state. Codex invokes this skill with `$relay`;
`/relay` and `/relay:doctor` are Claude commands, not Codex commands.

Relay-managed Codex terminals supply `RELAY_EXECUTABLE`, `RELAY_CONFIG_ROOT`, `RELAY_STATE_ROOT`,
`RELAY_PROJECT_DIR`, and `RELAY_SESSION_ID`. Check that all five are nonempty before running the
commands below. If absent, explain that the conversation has no verified Relay terminal context
and suggest `relay doctor` in a terminal in the project. Do not guess a session or owner from
the working directory, profile name, or conversation text.

Choose the command matching the request (default: status). Use the shell tool and preserve
the quoted environment variables as individual arguments:

```sh
"$RELAY_EXECUTABLE" --config-root "$RELAY_CONFIG_ROOT" --state-root "$RELAY_STATE_ROOT" doctor --project "$RELAY_PROJECT_DIR"
"$RELAY_EXECUTABLE" --config-root "$RELAY_CONFIG_ROOT" --state-root "$RELAY_STATE_ROOT" status --project "$RELAY_PROJECT_DIR"
"$RELAY_EXECUTABLE" --config-root "$RELAY_CONFIG_ROOT" --state-root "$RELAY_STATE_ROOT" why --project "$RELAY_PROJECT_DIR" --session "$RELAY_SESSION_ID"
"$RELAY_EXECUTABLE" --config-root "$RELAY_CONFIG_ROOT" --state-root "$RELAY_STATE_ROOT" history --project "$RELAY_PROJECT_DIR" --session "$RELAY_SESSION_ID"
```

Report the relevant CLI output concisely. Doctor exit code 1 with a readiness report means
not ready, not an execution failure. Status lists multiple conversations: identify this one
using `RELAY_SESSION_ID`, not merely the most recently active session. Never invent health,
trust acceptance, quota, or a successful handoff. Report a sandbox denial as a denial.

## $relay mode: show or change this conversation's execution mode

`$relay mode` shows the current execution mode; `$relay mode autonomous`/`$relay mode
interactive` changes and persists it on the current Relay Session. This is behavioral intent
only (whether to keep working without asking to proceed) — it never changes a sandbox setting,
an approval policy, or any provider permission.

```sh
"$RELAY_EXECUTABLE" --config-root "$RELAY_CONFIG_ROOT" --state-root "$RELAY_STATE_ROOT" mode --project "$RELAY_PROJECT_DIR" --session "$RELAY_SESSION_ID"
"$RELAY_EXECUTABLE" --config-root "$RELAY_CONFIG_ROOT" --state-root "$RELAY_STATE_ROOT" mode autonomous --project "$RELAY_PROJECT_DIR" --session "$RELAY_SESSION_ID"
"$RELAY_EXECUTABLE" --config-root "$RELAY_CONFIG_ROOT" --state-root "$RELAY_STATE_ROOT" mode interactive --project "$RELAY_PROJECT_DIR" --session "$RELAY_SESSION_ID"
```

When the command actually changes the mode, its own output states the new mode plus what it
means in behavioral terms — e.g. "Execution mode is now autonomous. From this point forward,
continue the current task without asking whether you should proceed. Stop only when: the task
is complete, you are genuinely blocked on missing information, an action requires explicit user
authorization, or continuing would be unsafe or ambiguous." Treat that as a real, immediate
instruction for the rest of THIS conversation, not just a status line to relay to the user: if
the mode just became autonomous, act on it starting with your very next step; if it became
interactive, go back to asking before significant next steps as usual. An autonomous mode never
means ignoring a genuine blocker, a destructive action needing approval, or an explicit user
instruction.

For switching to a *named* profile, never run `relay switch` inside the current agent shell
directly: it is not the same process as the one Relay is supervising, and stopping it mid-command
would be running the switch's own kill target. Instead ask the supervising Relay process itself to
do it, over the same control channel Claude's in-agent switch already uses:

```sh
"$RELAY_EXECUTABLE" --json --config-root "$RELAY_CONFIG_ROOT" --state-root "$RELAY_STATE_ROOT" switch-request <requested-profile> --project "$RELAY_PROJECT_DIR" --session "$RELAY_SESSION_ID"
```

This prints a JSON envelope; read `data.outcome`:

- `"answered"` — the supervisor decided. Report `data.message` to the user verbatim (this is the
  actual accept/refuse result, `data.ok` true or false); if accepted, the supervising terminal
  reopens the conversation on the new profile in a moment, no further action needed.
- `"no_supervisor"`, `"stale_session"`, `"unreachable"`, or `"timeout"` — no verified Relay
  supervisor could be reached (rare: e.g. `relay resume`/`relay codex` was not what started this
  terminal). Fall back: show the user a shell-quoted command to run in another terminal instead,
  using the actual environment values for executable, roots, project and session:

  ```text
  <relay> --config-root <config> --state-root <state> switch <requested-profile> --project-dir <project> --session <session> --no-attach
  ```

The interactive profile picker (no specific target named) only exists in a real terminal — when
the user wants to choose rather than name a profile, go straight to the manual fallback above with
the profile omitted, not `switch-request` (which always requires one). Do not edit trust settings,
accept prompts, change permissions, install integrations, or mutate Relay state as part of a
health/status request.
