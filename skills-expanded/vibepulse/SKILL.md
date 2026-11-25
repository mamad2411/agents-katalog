---
name: vibepulse
description: Use for VibePulse panel questions, permission behavior, setup, status, or doctor diagnostics for the optional local Codex bridge.
---

# VibePulse

Keep VibePulse interactions opt-in and local. Installing the plugin does not
enable a provider; the saved VibePulse configuration controls routing.

Use `mcp__vibepulse__ask` only for one bounded question with 2-3 explicit
options when you can make a genuine recommendation. Keep labels and details
short, mark at most one option recommended, and send no secrets.

Use native `request_user_input` for free-form answers, secrets, multiple
questions, unsupported shapes, an unavailable panel, timeout, or computer
fallback. Never treat silence, panel absence, or fallback as approval.
Permission decisions remain subject to Codex policy.

For a physical Codex smoke test, use the exact short question
`Ser du APPROVE?` with `Ja` (`APPROVE syns`) and `Nej` (`APPROVE saknas`),
marking only `Ja` recommended. Pass only when the panel visibly shows
**APPROVE**, a human taps it, and the call returns `status: answered`,
`option_index: 0`, `answer: Ja`. **SOMETHING IS WAITING** without answer
buttons is the fit/privacy fallback, not a pass. After a flash, compare
`git describe --tags --always --dirty` from the build checkout with the service's
`otaAvailableVersion` before testing.

Explain that the encrypted relay remains not enabled by this plugin. When the
owner separately enables it, opaque encrypted envelopes leave the LAN but the
question and verdict stay end-to-end encrypted between host and panel.

When setup state is relevant, run `python3 tools/vibepulse_setup.py status`.
When troubleshooting is relevant, run `python3 tools/vibepulse_setup.py doctor`.
From a checkout, prefer its `.venv/bin/python` on POSIX or
`.venv\Scripts\python.exe` on Windows when present; a system `python3` can be
older than the interpreter that actually runs the service. Also run
`tools/tokenserver/smoke.py` with that interpreter for a stale report.

Diagnose these safe signals separately: `claudeProbe` is the active quota
source outcome, `claudeCredential` is saved-credential readiness, and the
`/api/tokens` stale flags are the data actually sent to the panel. If
`claudeProbe` is `usage_http_200 + ok` and the relevant stale flag is false,
the source is live even when the saved credential says `expired`; call that a
future recovery risk, not the current stale cause. Start a new Claude Code CLI
turn to refresh the saved fallback. VibePulse rereads local credentials every
15 seconds, so do not prescribe a tokenserver restart first.

On plugin 0.1.7+, read `VibePulse startup health`: provider stale routes to
provider/credential checks; device path stale to panel power/network/discovery/
firmware; version drift means plugin and host sources differ; server unavailable
routes to service diagnostics. It is read-only and never approves.

If the local API and configured numbers relay are fresh while the glass is
stale, inspect `GET /` → `interactions.panel` for recent direct polling and
read passive logs. `waiting` does not prove failure on a relay-only network,
but fresh LAN and relay with stale glass localizes the device hop. Test relay
with the panel User-Agent; generic Python may get a misleading Cloudflare 403.
Computer USB can exhaust its 500 mA budget during Wi-Fi bursts, so use a
dedicated 5 V supply. Compare installed firmware with current `main`; old
firmware cannot discover another Mac/Windows host. Never reset or flash without
explicit permission, and never infer health from serial silence.

If passive serial repeatedly reports accepted token payloads while the glass
still says `STALE`, compare its Claude/Fable/Codex/Max Tracker stale bits.
Fresh bits localize stale bookkeeping/rendering; current firmware clears
transport stale synchronously and logs only those booleans. Do not treat
`hämtning ok` as UI proof or close the incident before the glass changes.
Never call one successful post-boot request a sustained stale-recovery pass.
Keep the panel on dedicated power beyond its 120-second stale window, require
recent direct polling again, and repeat the canonical physical question. If
the board still answers ping while direct panel polling ages out, the local and
numbers-relay payloads remain fresh, and the repeated question times out,
record a device-side application-HTTP stall rather than blaming provider data.
Current relay-configured firmware has a bounded self-recovery guard: after an
initial quota success, 60 seconds without progress while Wi-Fi still reports
association recycles the station transport and wakes the quota task, which
waits for a new IP before retrying. If no real success follows within another
45 seconds, the device performs one controlled restart. Cold boot stays disarmed
until a new real success, preventing a persistent upstream outage from becoming a restart
loop. Either guard firing is recovery evidence, not a PASS by itself. LAN-only
firmware deliberately does not recover merely because its host sleeps.
After a guarded restart, `interactions.panel.httpStallRecoveryBoot` can prove
the guard fired without serial, not that the stale window/question passed.

Treat fresh numbers plus timed-out questions as a separate transport check.
When more than one `_vibepulse._tcp` service is advertised on the same LAN,
DNS-SD result order cannot identify which computer owns the current question;
the panel may be polling a different healthy Mac or PC. Confirm the service
count without publishing hostnames or private addresses. For a panel shared by
several computers, use the existing end-to-end encrypted interaction relay on
the hosts and enable `TK_VIBEPULSE_INTERACTION_RELAY` in that panel's firmware.
If local `/api/agent-status` reports an active agent while the glass says no
active agent, also check the separate host and firmware live-status switches.
Do not claim a local active row proves the panel route, and do not flash a
relay-enabled image without a fresh explicit authorization.

Explain that this versioned skill does not learn or update itself; new lessons reach Codex after a plugin release and new task.
Do not run install, disable, or uninstall without the user's explicit request.
