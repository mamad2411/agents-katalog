---
name: cmux-sessions
description: Launch, observe and narrowly control cmux terminal or agent sessions with the cmux CLI. Use for Dispatcher-to-Worker session creation, explicit cross-session routing, bounded screen reads, or a user-authorized session correction; do not use Computer Use when socket automation is available.
---

# cmux sessions

Apply [runtime-independent roles](../../runtime-compatibility.md). Verify each
role/runtime/client tuple; a terminal or skill catalog entry is not launch,
resume, callback or execution-fence qualification.

Use cmux as live-session transport. Squad remains authoritative for work
ownership, reservations, dependencies and environment locks.

For an authorized replacement, use the coordinator's
[session continuity contract](../../../coordination-skills/squad-dispatcher/references/session-continuity.md).
cmux process control does not transfer task, reservation, environment or execution
ownership. Do not reuse the Worker-only launcher/envelope for a Deployer unless
the installed package explicitly supports that role.

## Preflight

Use the bundled binary when `cmux` is not on `PATH`:

```sh
CMUX_BIN=/Applications/cmux.app/Contents/Resources/bin/cmux
"$CMUX_BIN" ping
"$CMUX_BIN" capabilities --json
"$CMUX_BIN" identify --json
"$CMUX_BIN" tree --all --json
```

An external Dispatcher may mutate sessions only when capabilities reports
`access_mode: automation`. `cmuxOnly` means the process is outside the trusted
socket boundary; do not bypass it. Use Computer Use only when the user requests
it or the CLI capability is genuinely unavailable.

## Runtime permission mode and resume

Record and honor the user's selected runtime permission mode in the launcher.
For Claude, explicit user authorization for YOLO selects
`--permission-mode bypassPermissions`; `auto` can still deny commands and
`--allow-dangerously-skip-permissions` only enables an option. Verify the
installed CLI contract and then the actual process arguments/status bar.
Do not enable bypass implicitly or in response to a denial without user
approval. This setting does not expand task scope, WIP or ENV authority, and a
Dispatcher's permission mode does not automatically propagate to its Workers.
Pass each newly launched session's authorized mode explicitly.

When asked to change a running session's mode, inspect live work first. Preserve
its native session id, claims, external-operation state and assignment. Stop
the local client as authorized and resume the same id (Claude: `--resume ID
--permission-mode MODE`); do not send the original assignment again or create a
replacement reservation. Verify the old process exited before resuming and
check the effective mode afterward. An external rollout continues independently
of stopping the client and must remain supervised on resume.

For controller-owned launch, bounded model-transport recovery and authorized
live instruction adoption, use [assignment continuity](../../lifecycle-continuity.md).
A mode change must use the native resume interface and preserve active custody.

## Create and bind one Worker

Run the selected package's `worker_preflight.py` before session creation, using
the actual client's skill entries and required executable names. Resolve missing
capabilities or stale assignment identity before paying for a Worker startup.
This local receipt does not replace Squad ownership or runtime approval checks.
For Claude cold starts, use the package's `claude_worker_launcher.py` with a
separate schema-valid launch config and pass `--launch-config` to preflight.
The same launcher must pass `--check` with inherited parent identity removed
before creating the workspace. Use native Squad coordination when available;
select the explicit Codex-wrapper compatibility adapter only for an installed
wrapper requiring it. Do not handwrite identity/guard loops. Only a successful
read of an exact unbound reservation is a binding wait; command errors and
invalid output fail immediately with bounded, sanitized diagnostics.

Create a new workspace with an owned worktree and a reviewed launcher:

```sh
"$CMUX_BIN" new-workspace \
  --name '[#981][STUDIO-084] short title' \
  --cwd /absolute/owned/worktree \
  --command /absolute/reviewed/launcher.sh \
  --focus false
```

Read the returned identifiers or resolve them once with `tree --all --json`.
Persist the workspace UUID, surface UUID and native agent session ID with the
matching dispatch reservation. The Worker title prefix and assignment identity
must agree. Never bind a native to two reservations or relabel a workspace to
imitate reassignment. An authorized related-work amendment retains the current
primary identity and follows the Dispatcher's existing-owner routing; cmux input
alone cannot transfer assignment authority.

For terminal notifications, record a runtime-tagged callback route at launch:
cmux workspace UUID, surface UUID, native session id and Squad agent id, or an
actual App thread/host id. Resolve the endpoint read-only before dispatch; do
not send a dummy prompt to test it. A Claude UUID is not a Codex App thread id.
These cmux identifiers prove identity, not a safe callback channel. Background
terminal events must be persisted in Squad; use only a verified message API or
mailbox for wakeup. Never inject callbacks with send/send-key/paste/Enter, even
when the input appears empty. Never save, clear, restore or submit a user draft
to deliver an event. Missing safe transport means pending reconciliation, not
a delivered callback or a user message-copying chore.

## Observe without disturbing

```sh
"$CMUX_BIN" sessions list --json
"$CMUX_BIN" read-screen --workspace WORKSPACE --surface SURFACE --lines 80
```

Use explicit targets and bounded output. A quiet or idle screen is not terminal
while a reservation, claim, CI/deployment operation or environment lock is live.
Do not focus, flash, move, close, kill or replace a healthy Worker for monitoring.

## Worker workspace lifecycle color

For Dispatcher-owned Worker workspaces, use Blue while assigned work remains
nonterminal, and the native clear-color action after terminal reconciliation.
This is presentation only, never assignment, claim or completion authority.
Use the persisted explicit workspace UUID; never the current/focused workspace.
Verify automation access and the reservation/native-session/workspace mapping
before changing a color. Do not color the Dispatcher or unrelated workspaces.

```sh
"$CMUX_BIN" workspace-action --workspace WORKSPACE_UUID --action set-color --color Blue
"$CMUX_BIN" workspace-action --workspace WORKSPACE_UUID --action clear-color
```

Set Blue after successful launch and binding. Keep it through CI, deployment,
claim waiting, idle turns and decision requests. Do not attach clearing to a
Claude Stop hook or process exit: neither proves the assigned work has ended.
The Worker clears its own workspace after recording its terminal outcome and
required claim release or acknowledged handoff, with no live external operation.
The Dispatcher repeats this idempotent projection during its existing bounded
reconciliation cycle, including completed/failed/cancelled reservations with a
recorded workspace. A stopped client with unresolved claims or rollout stays
colored until recovery/handoff is reconciled. An Issue may remain open after a
valid terminal handoff; color indicates this Worker's assignment, not Issue closure.

When the installed executable has `squad dispatch retire-color`, use it instead of
the raw action: it applies the terminal gate and records the result separately from
client exit (`squad dispatch retirement` shows both). Never clear a color or exit a
client from the raw cmux action to imitate a retirement result.

Color failure must not block delivery, alter claims, resend assignments or inject
terminal input. Record a bounded diagnostic and retry on the next existing cycle;
a closed/missing workspace needs no recreation. Persist the desired/applied color
and workspace UUID in coordination metadata, not strict assignment envelopes.
Do not add a daemon, heartbeat or role solely for colors. When loading this rule,
reconcile existing mapped workspaces as well as future launches.

## Send a bounded intervention

Input is allowed only for the initial assignment, an explicit user override, an
immediate safety/scope correction, or one verified dependency transition.
These permissions do not authorize altering unrelated pending input. If a draft
or command is present or input ownership is uncertain, do not inject or submit.
Background terminal callbacks are excluded; use the durable event path above:

```sh
"$CMUX_BIN" send --workspace WORKSPACE --surface SURFACE 'message'
"$CMUX_BIN" send-key --workspace WORKSPACE --surface SURFACE enter
"$CMUX_BIN" read-screen --workspace WORKSPACE --surface SURFACE --lines 40
```

Never send routine progress questions, acknowledgements or resource-wait
reminders. Verify the title/IDs immediately before sending and read the screen
once afterward. Durable decisions and outcomes belong in Squad/checkpoints, not
only in terminal scrollback.

## Native event receiver

A Claude Dispatcher may use the package's `terminal_receiver.py` with a
session-specific config and `--settings` file. The launcher pins absolute binary,
ledger and Python paths, native session id, recipient, owner PID, state directory
and a fresh incarnation on every start/resume. `--write-settings` generates
SessionStart/PostToolUse/Stop command hooks with `asyncRewake: true`; it is a
hook field, not an event name. The helper owns one locked receiver per session,
terminates an old incarnation, and never accesses terminal input. Validate one
real idle wake and acknowledgement before declaring this transport available.
Preserve user-selected permission mode and native id on a cutover; do not restart
an active Worker to install a Dispatcher receiver.

For new Claude Workers needing asynchronous design decisions, include
`event_executable` in the separate launch config. Preflight checks the structured
publish capability; the canonical launcher creates a Worker-role native receiver
with the child's own identity/PID/incarnation. Decision replies use the durable
ledger, never terminal input. Existing Workers are not silently restarted.

For an established durable Squad callback/decision route, publish the authorized
event there even when a terminal shows unsent input or an automatic suggestion.
Input state only constrains keystroke injection, not ledger message publication.
A suggestion is neither a user instruction nor approval. Unknown human drafts
remain protected; verify acknowledgment/adoption through the durable receiver.
