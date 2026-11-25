---
name: autonomous-agent-watchdogs
description: Design and verify liveness watchdogs for long-running autonomous agent loops, including durable recovery state, bounded restarts, actionable escalation, messaging failures, and recovery notices.
version: 1.1.0
author: Hermes Agent
license: MIT
platforms: [linux, macos]
metadata:
  hermes:
    tags: [watchdog, liveness, systemd, tmux, autonomous-agents, alerting, recovery]
---

# Autonomous Agent Watchdogs

Use this skill when a long-running autonomous agent can remain process-alive while its internal work chain has died, stalled, lost authentication, or stopped scheduling its next turn.

## Core principle

Process health is not workflow health. Monitor a durable signal of meaningful progress, repair only the failed controller, and escalate when repeated repairs do not restore that signal. A watchdog observes and recovers; it must not become a second driver that independently emits work.

## Failure-model discovery

Before changing anything, map the full chain:

1. Service manager unit or supervisor.
2. Terminal/session wrapper such as tmux.
3. Controller process.
4. Internal scheduler or self-chained wakeup mechanism.
5. Durable progress artifact: transcript, journal offset, heartbeat file, queue acknowledgement, or domain state transition.
6. Recovery action and its cooldown.
7. Messaging path and its own dependencies.

Read the live pane/process state before testing. A real restart during an in-flight action can duplicate side effects, corrupt state, or violate platform caps.

## Liveness signal

- Prefer a signal updated by every healthy cycle, including deliberate no-op cycles.
- Set staleness above the maximum legitimate idle interval plus worst-case turn time and jitter.
- Resolve the signal from the active controller identity rather than “newest file in a directory” whenever possible.
- Validate that the PID is alive, still belongs to the expected controller executable (to reject PID reuse), and that the signal belongs to its current session.
- Normalize and validate session metadata such as `sessionId` and ordering timestamps before comparison.
- Propagate parser/probe failures to the service manager with a non-zero exit; never turn an internal exception into a successful “inconclusive” check.
- Return a human-readable verdict such as `OK`, `STALE`, or `DEAD`; preserve the exact verdict for logs and alerts.
- Check for recovery before applying restart cooldown. Cooldown should suppress another restart, not prevent a healthy check from clearing the incident.

## Durable incident state

Keep recovery state beside the agent’s other operational metrics:

- Consecutive restart count: increment only when the watchdog actually emits a restart.
- Episode start: set on the first restart and retain until recovery.
- Last restart time for cooldown enforcement.
- Last escalation attempt time, persisted immediately before the external send.
- Last successfully delivered escalation time.
- Pending recovery notification and its last attempt time.
- A process lock covering liveness evaluation, restart, and all state transitions.

Use atomic writes and a restrictive umask. Absence may represent the documented initial value, but malformed state must never silently become zero: log it, replace it with a conservative value, and fail closed against restart thrash or notification spam. Persist the restart cooldown timestamp before restarting; if that write fails, abort the restart. A healthy `OK` check resets the restart count and episode start immediately.

## Escalation semantics

- Alert only after a configurable number of consecutive unsuccessful recovery cycles.
- Send once when the threshold is reached, then no more frequently than a configurable repeat interval.
- Distinguish *preflight unavailable* from *delivery attempted*. A disconnected gateway does not consume the repeat window and can retry at the next bounded restart.
- Persist an attempt timestamp immediately before invoking the messaging CLI. This is an idempotency fence: a timeout can occur after the backend accepted the message, so an ambiguous attempt must consume the repeat window even without an exit-0 acknowledgement.
- Record successful delivery separately when the command returns exit `0`. If this success write fails, the already-persisted attempt timestamp still prevents rapid duplicates.
- Apply the same attempt fence to recovery notices. Create recovery-pending state when an escalation may have reached the operator, and remove it only after confirmed delivery; ambiguous failures wait for the repeat interval.
- Never let notification code terminate or block the watchdog indefinitely. Apply a hard total timeout, capture and log all meaningful exit codes, validate message-file creation/write/permissions, and continue recovery.

## Actionable alert content

Include:

- Number of consecutive restart attempts.
- Episode start time in the operator’s timezone.
- Exact watchdog verdict.
- Most recent real upstream/API error, when safely extractable from the current session artifact.
- Concrete operator commands to connect to the host and attach to the controller session.
- The likely remediation only when supported by the extracted error (for example, re-authentication).

Do not dump entire transcripts, credentials, request headers, user messages, or unrelated agent output. Parse structured events first, then redact bearer tokens, API-key-like strings, JWTs, refresh/access-token values, and other credential patterns before the text leaves the host. Bound the final diagnostic length.

## Messaging dependency checks

A messaging CLI can exist while its gateway/backend is offline. Before sending:

1. Verify the absolute binary path because service-manager PATHs are minimal.
2. Inspect the gateway’s durable state and require the target platform to be connected.
3. Skip the send when disconnected and log that delivery was unavailable.
4. Bound the send with a wall-clock timeout.
5. Log the command’s exit code without logging secrets or recipient identifiers beyond the configured alias.

## TDD without disturbing production

Build a temporary harness before production changes:

- Copy the watchdog and config into a temporary root.
- Override home/root/config knobs through environment variables.
- Stub the service manager so restart attempts are recorded but no real unit changes.
- Stub the messaging CLI and capture subject/body/exit code.
- Create fake gateway state for connected and disconnected cases.
- Create a live fake session mapping and transcript; manipulate transcript mtime to produce `OK` and `STALE`.
- Include a representative structured API-error event.

Required cases:

1. Counter increments per emitted restart.
2. Alert fires exactly at threshold.
3. No duplicate inside repeat cooldown, including an ambiguous timeout/non-zero result after the CLI was invoked.
4. Re-alert after repeat cooldown.
5. Disconnected gateway does not invoke messaging, is logged, and retries when the gateway reconnects.
6. Messaging exit code and pre-send preparation failures are logged.
7. Actionable body contains count, start, verdict, extracted error, and attach commands.
8. Structured error extraction tolerates valid JSON whitespace and redacts credential-looking material.
9. `OK` resets state.
10. Recovery sends once after an alerted or ambiguously attempted incident; failed delivery remains pending without spam.
11. Two concurrent invocations emit only one restart and one state transition.
12. Invalid numeric knobs fail closed before restart; malformed persisted state is logged and uses conservative defaults.
13. Syntax/static checks pass.
14. A naturally scheduled production check completes successfully without a restart.

## Deployment verification

- Confirm the installed unit executes the edited script directly; if so, avoid reinstalling or restarting unnecessarily.
- Confirm the fallback work-driver timer remains disabled when two drivers would duplicate actions.
- Let the normal watchdog timer perform one natural check and inspect its completion status and journal.
- Verify no restart stamp, incident counter, or alert marker was created during a healthy check.
- Never send a false live alert unless the user explicitly authorizes it; use a fake messaging binary instead.

## Pitfalls

- Treating `active (running)` as proof that a self-chained loop still schedules work.
- Placing the cooldown before the `OK` check, delaying incident reset and recovery notification.
- Having no lock because “systemd serializes the unit”; a manual invocation can still race the timer.
- Recording only successful delivery time. A timeout after backend acceptance is ambiguous and can create duplicates unless an attempt marker was persisted first.
- Treating malformed numeric state as zero, which can erase cooldowns, lose counts, and trigger spam.
- Accepting arbitrary numeric config without bounds/validation, then allowing arithmetic or probe failures to look successful.
- Filtering JSON by one exact serialized spacing instead of parsing candidate events structurally.
- Sending raw upstream error text without credential redaction.
- Checking only `kill(pid, 0)` and accepting a stale session mapping after PID reuse.
- Clearing escalation state before a recovery notice is safely delivered.
- Testing by killing/restarting the real controller while a platform action may be in flight.
- Adding a second timer that fires work instead of observing progress.
- Using socket read timeouts where a hard total deadline is required.
- Assuming a notification binary implies its platform gateway is connected.

## References

- See `references/session-chain-escalation.md` for a concrete systemd + tmux + transcript + Hermes/WhatsApp implementation pattern.
