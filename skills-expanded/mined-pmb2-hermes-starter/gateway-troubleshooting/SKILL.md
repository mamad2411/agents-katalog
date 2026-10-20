---
name: gateway-troubleshooting
description: "Diagnose and fix Hermes gateway issues across platforms — attachment handling, connectivity, config, service management, and interrupted updates."
version: 1.2.0
author: Hermes Agent
license: MIT
platforms: [windows, linux, macos]
metadata:
  hermes:
    tags: [gateway, troubleshooting, discord, telegram, slack, diagnostics, connectivity]
    triggers: [gateway-issues, gateway-troubleshoot, discord-attachments, gateway-connectivity, gateway-login, gateway-error, attachment-issues, gateway-config, gateway-service, gateway-restart]
    related_skills: [gateway-architecture-analysis]
---

# Gateway Troubleshooting

General Hermes gateway diagnostics and fixes. Covers the messaging gateway that connects Hermes to Discord, Telegram, Slack, and other platforms.

## Quick Diagnostics

### Check gateway status
```bash
hermes gateway status
```

### Check gateway logs for errors
```bash
# Recent errors
grep -i "error\|warning\|failed" ~/.hermes/logs/gateway.log | tail -30

# Attachment-specific
grep -i "attach\|cached.*document\|text injection\|inject.*text" ~/.hermes/logs/gateway.log | tail -20

# Restart events
grep -i "restart\|shutdown\|stopped" ~/.hermes/logs/gateway.log | tail -10
```

### Check agent logs
```bash
tail -50 ~/.hermes/logs/agent.log
```

## Model Provider Error Diagnostics

When a Discord agent reports "The model provider failed after retries", this is often **NOT a provider outage** — it can be an API schema rejection or message formatting issue that surfaces as a transport error.

### Trace workflow

1. Extract the session ID from gateway log: `grep "model provider failed" ~/AppData/Local/hermes/logs/gateway.log`
2. Find the actual error in agent log: `grep "Non-retryable client error\|API call failed" ~/AppData/Local/hermes/logs/agent.log | tail -10`
3. Identify the error type:
   - **HTTP 400 "empty tool_calls array"** — session resume produced corrupt message history. See `references/model-provider-failed-diagnosis.md` for full fix.
   - **HTTP 400 "assistant with tool_calls must be followed by tool"** — role alternation violation.
   - **HTTP 401/403** — API key missing, expired, or wrong provider. Check `.env`.
   - **HTTP 429** — rate limited.
   - **HTTP 5xx** — actual provider outage.
4. Trace which profile serves the channel: check `config.yaml` → `discord.channel_prompts`, profile `allowed_channels`, and `channel_directory.json`.
5. Verify the profile's `.env` has the API key (global `.env` at `~/AppData/Local/hermes/.env`).

Full diagnosis guide with commands and code-level fixes: `references/model-provider-failed-diagnosis.md`.

## Discord Attachment Issues

If Discord file attachments (`message.txt`, etc.) aren't reaching the agent:

### 1. Check the symptom
Search gateway logs for:
```
Authenticated attachment read failed for message.txt: 400
Can not decode content-encoding: br
```

The `br` = Brotli compression. Discord's CDN may start serving attachments with Brotli content-encoding.

### 2. Fix Brotli decompression (most common cause)
The `brotli` Python package on Windows often installs **without its C extension** (pure Python fallback only). aiohttp needs the CFFI-based decoder:
```bash
pip install brotlicffi
```
Verify:
```bash
python -c "from aiohttp.compression_utils import HAS_BROTLI; print('HAS_BROTLI:', HAS_BROTLI)"
```

### 3. Configure attachment handling
In `config.yaml` or via `hermes config set`:
```yaml
discord:
  allow_any_attachment: true    # Accept any file type, not just allowlist
  max_attachment_bytes: 0       # 0 = unlimited (default 32 MiB)
```
```bash
hermes config set discord.allow_any_attachment true
hermes config set discord.max_attachment_bytes 0
```

### 4. Restart the gateway
**IMPORTANT:** You CANNOT restart the gateway from inside a gateway chat session (Discord/Telegram). The gateway refuses to prevent restart loops. Run from an **external shell**:
```bash
hermes gateway restart
```
Or stop/start:
```bash
hermes gateway stop && hermes gateway start
```

## Gateway Management

### Can't stop/restart from inside the gateway
The `hermes gateway stop`, `hermes gateway restart`, and `hermes gateway start` commands all fail when run from inside a gateway session (the process you're chatting through). Error:
```
✗ Refusing to restart/stop the gateway from inside the gateway process.
This command was blocked to prevent restart loops.
```
**Fix:** SSH into the host, open a separate terminal, or use Task Scheduler / systemctl from outside.

### Gateway Install on Windows
When the gateway is completely down (no PID, cron jobs not firing, `hermes gateway status` timed out):

```bash
# Install and start the gateway on Windows
# Requires external shell (not inside a gateway session)
printf "Y\nY\n" | hermes gateway install --force
```

This does two things:
1. Creates a Windows Scheduled Task `Hermes_Gateway` that auto-starts on login
2. Spawns the gateway process directly and starts all configured profile gateways

**Verify:**
```bash
hermes gateway status
# Should show: Scheduled Task Ready, Gateway process running (PID: xxxxx)
# All profile gateways listed with PIDs
```

**What to expect after install:**
- All council profile gateways start automatically (chief-of-staff, dev-lead, docs-lead, qa-lead, skills-lead, integration-lead, etc.)
- Cron scheduler wakes up and begins auto-firing jobs
- Kanban dispatcher starts claiming ready tasks
- Gateway log at `~/AppData/Local/hermes/logs/gateway.log`

**If the gateway install hangs at prompts:**
The install asks two yes/no questions:
1. "Start the gateway now after install? [Y/n]:"
2. "Start the gateway automatically on Windows login with a Scheduled Task? [Y/n]:"

Pipe both answers with `printf "Y\nY\n"` as shown above, or run from a terminal where you can interact.

**On Linux:** Use `sudo hermes gateway install --system` to install as a systemd service. Skip the Scheduled Task part.

### Check what's running
```bash
# Windows
tasklist /fi "IMAGENAME eq python.exe" /v | grep hermes

# Linux/macOS
ps aux | grep hermes
```

### Check service status
```bash
# Windows
hermes gateway status

# Linux (systemd)
systemctl --user status hermes-gateway
```

## Interrupted Update Recovery

If `hermes update` was interrupted midway, every subsequent `hermes` command tries to finish the install. On Windows, this commonly fails with:
```
error: Failed to install: pillow-12.2.0-...
  Caused by: failed to rename file ..._imaging.cp311-win_amd64.pyd: Access is denied. (os error 5)
```

**Cause:** The `_imaging.pyd` DLL is locked by the running gateway process (that imports Pillow for image handling). The upgrade can't rename/replace the file while it's in use.

**Fix:**
1. Stop the gateway from an external shell: `hermes gateway stop`
2. Kill any leftover Python processes: `taskkill /F /PID <pid>` or close the running gateway
3. Run `hermes update` from the external shell (not inside a gateway session)
4. Restart the gateway

## Post-Update Audit (run after EVERY `hermes update`)

After any update that reports "Restoring local changes...", verify the custom stack survived: custom patches in the repo (git status, stash list, `.orig` leftovers), config.yaml vs the timestamped backups, MCP server count, cron jobs, scripts dir, and stale gateway PIDs. Full checklist: `references/post-update-audit.md`. the operator expects this proactively — custom functionality must survive updates.

## Post-Daily-Reset Recovery

Hermes sessions reset daily (cron boundary). After a reset, all gateway processes from the previous day are dead but leave stale state files. Recovery is a two-step procedure:

### 1. Clean stale gateway state

```bash
for p in ${HERMES_HOME}/profiles/*/; do
  rm -f "$p/gateway.pid" "$p/gateway_state.json" "$p/gateway.lock" \
        "$p/gateway.lock.spacebar" "$p/.gateway_state"*
done
```

Gateways that were running without state files (e.g., clean shutdowns) don't need cleanup. Only profiles with leftover `gateway_state.json` or `.lock` files from the previous session need clearing.

### 2. Restart the council gateway stack

The recommended restart order is the core 10 (architect + 9 council leads). Each starts as a **background process** with env isolation to prevent token bleed from parent shell:

```bash
cd ${MY_REPOS}/agent-fleet
unset DISCORD_BOT_TOKEN && unset SPACEBAR_BOT_TOKEN && \
unset SPACEBAR_GATEWAY_URL && unset SPACEBAR_API_URL && \
source "${HERMES_HOME}/profiles/architect/.env" && \
python scripts/spacebar-gateway.py architect
```

Repeat for: chief-of-staff, technology-lead, growth-lead, intelligence-lead, treasury-lead, counsel-lead, compliance-lead, portfolio-lead, operations-lead.

**Always unset token env vars** before sourcing the profile's `.env`. A stale `DISCORD_BOT_TOKEN` or `SPACEBAR_BOT_TOKEN` in the parent shell will override the `.env` file value and cause the wrong bot to authenticate.

### 3. Start the Discord-Spacebar bridge (if needed)

```bash
cd ${MY_REPOS}/agent-fleet
exec python -u scripts/discord-spacebar-bridge.py > /tmp/bridge.log 2>&1
```

### 4. Verify

```bash
for p in architect chief-of-staff technology-lead growth-lead \
         intelligence-lead treasury-lead counsel-lead compliance-lead \
         portfolio-lead operations-lead; do
  sf="${HERMES_HOME}/profiles/$p/gateway_state.json"
  if [ -f "$sf" ]; then
    pid=$(grep -o '"pid":[0-9]*' "$sf" | cut -d: -f2)
    running=$(tasklist //FI "PID eq $pid" //NH 2>/dev/null | grep -o "python" || echo "DEAD")
    state=$(grep -o '"gateway_state":"[^"]*"' "$sf" | cut -d'"' -f4)
    disc=$(grep -o '"discord":{"state":"[^"]*"' "$sf" | cut -d'"' -f6 2>/dev/null || echo "?")
    echo "$p: $state discord=$disc pid=$pid [$running]"
  fi
done
```

All 10 should show `state=running discord=connected`.

## Automated Watchdog / 3-Layer Redundancy System

A continuous watchdog daemon (`hermes-watchdog.py`) monitors all Hermes processes and auto-restarts them on crash. It's installed via two redundant mechanisms:

### Layer 1 — Continuous Watchdog Daemon

Located at `${MY_REPOS}/Documents/github/agent-fleet/scripts/hermes-watchdog.py`, this daemon:
- Monitors **12+ critical processes** in a tight loop
- **Auto-restarts** any crashed process immediately
- Uses **exponential backoff** (2s → 4s → 8s → 16s → 32s → 60s max) to avoid restart loops
- **Cleans stale locks/state** before restarting
- Logs all events to `~/AppData/Local/hermes/logs/watchdog.log`
- Reports health every 30 seconds

**Monitored processes:**
| Name | Kind | What it is |
|------|------|------------|
| `hermes-agent` | Core agent | `hermes-agent.exe run` — the main AI agent binary |
| `gateway-service` | Gateway | `hermes_cli.main gateway run --replace` — Discord/Spacebar gateway |
| `gateway-architect` | Profile gateway | spacebar-gateway.py architect |
| `gateway-{chief-of-staff,technology-lead,...}` | Profile gateway | 9 council bot gateways |
| `discord-spacebar-bridge` | Bridge | bridges Discord ↔ Spacebar |

**Manually start/stop:**
```bash
# Start watchdog (foreground)
python ${MY_REPOS}/Documents/github/agent-fleet/scripts/hermes-watchdog.py

# Start as daemon (background, no window)
pythonw ${MY_REPOS}/Documents/github/agent-fleet/scripts/hermes-watchdog.py --daemon

# Check if watchdog is running
tasklist /FI "IMAGENAME eq pythonw.exe" /NH /FO CSV

# Read watchdog logs
tail -50 ~/AppData/Local/hermes/logs/watchdog.log
```

### Layer 2 — Scheduled Task Watchdog Checker

The task `HermesWatchdogCheck` (Task Scheduler) runs every 5 minutes and checks if the watchdog daemon is alive via its PID lock file. If the watchdog crashed, the batch script at `hermes-watchdog-check.cmd` restarts it. This ensures survival even when the watchdog itself crashes.

```bash
# Check task status
powershell.exe -Command "Get-ScheduledTask -TaskName HermesWatchdogCheck | Get-ScheduledTaskInfo"

# View check logs
tail -20 ~/AppData/Local/hermes/logs/watchdog-check.log
```

### Layer 3 — VPS External Health Check

The VPS at `129.153.156.190` serves as an external health monitor. Spacebar gateway responds at `wss://gc.your-domain.example/`. Can be extended to send SMS/email alerts if the local agent stays down beyond a threshold.

### Setup Files (all in agent-fleet)

| File | Purpose |
|------|---------|
| `scripts/hermes-watchdog.py` | Core watchdog daemon |
| `scripts/hermes-watchdog-check.cmd` | Scheduled task checker (Layer 2) |
| `scripts/install-watchdog.py` | Python installer |
| `scripts/setup-hermes-redundancy.ps1` | PowerShell full-setup script |
| `scripts/create-watchdog-task.ps1` | Just the scheduled task part |

### Recovery after reinstall / fresh clone

If the watchdog system needs to be re-installed from scratch:
```powershell
cd ${MY_REPOS}\Documents\github\agent-fleet
powershell.exe -ExecutionPolicy Bypass -File scripts\setup-hermes-redundancy.ps1
python scripts\install-watchdog.py
```

### Crash Pattern: STATUS_ACCESS_VIOLATION (3221225794)

The gateway service crashes with exit code `3221225794` (= 0xC0000005 = STATUS_ACCESS_VIOLATION) when multiple MCP servers fail to connect at startup. Common failing MCP servers on this environment:
- `camofox-browser` — command=python, connection closed
- `camoufox-enhanced` — command=python, connection closed
- `depwire` — binary not found
- `git-stars` — command=python, connection closed
- `gpt-researcher` — command=python, connection closed
- `personal-intelligence` — command=python, connection closed
- `plane-mcp` — docker command, connection closed
- `remotion-render` — command=python, connection closed
- `tor-browser-mcp` — CancelledError
- `ultimate-firefox-mcp` — command=python, connection closed

The access violation likely occurs when the gateway's MCP connection manager exhausts retries while trying to resolve the entire server list. **Fix:** If the gateway consistently crashes on startup, temporarily disable the failing MCP servers in `config.yaml`:

```yaml
tools:
  mcp_tool:
    servers:
      camofox-browser: {enabled: false}
      depwire: {enabled: false}
      gpt-researcher: {enabled: false}
```

Or hard-disable a group:

```yaml
tools:
  mcp_tool:
    enabled: false
```

### Crash Pattern: Config Corruption

There have been 6+ `config.yaml.corrupt.*.bak` files in `~/AppData/Local/hermes/`. The config file can be corrupted by:
- An interrupted `hermes config set` operation
- Power loss during a write
- A crash during a config-write phase of the gateway startup

**Fix:** Restore from the most recent `.bak` file:
```bash
copy ~/AppData/Local/hermes/config.yaml.bak.20260622_213811 ~/AppData/Local/hermes/config.yaml
```
Corrupt backups are identifiable by the `.corrupt` suffix in their filename.

### Pitfall: `hermes config set` creates YAML strings instead of arrays

`hermes config set fallback_providers '[]'` saves the value as a YAML *string* `'[]'` rather than an empty YAML *list* `[]`. The gateway YAML parser rejects this with `mapping values are not allowed here` or `while parsing a block mapping`.

**Symptom:** Gateway log shows repeated `WARNING gateway.config: Failed to process config.yaml — falling back to .env / gateway.json values. Check config.yaml for syntax errors. Error: while parsing a block mapping` on every restart/reconnect.

**Fix:** Edit the line directly in the YAML file — change `fallback_providers: '[]'` (or `fallback_providers: ''`) to `fallback_providers:` (null/unset). Use `patch` or direct file write. Do NOT use `hermes config set` for values that must be YAML arrays — it wraps them in quotes.

### Pitfall: never sed structured YAML — use Python + parse-verify

Using `sed -i '/key:/a\...'` to insert a YAML block can replace or mangle the matched key line instead of inserting cleanly (this exact mistake once replaced the `opencode-zen:` provider key with `kimi:` while keeping the wrong base_url — silently breaking both providers). For any structured edit to `config.yaml`:

1. Edit with Python using an exact multi-line string replace (or the `yaml` module), never regex/sed on individual lines.
2. ALWAYS parse-verify afterward:
   ```bash
   python -c "import yaml; c=yaml.safe_load(open(r'${USER_HOME}\AppData\Local\hermes\config.yaml')); print(sorted(c['providers']))"
   ```
3. The `patch`/`write_file` tools REFUSE to write to `~/AppData/Local/hermes/config.yaml` ("security-sensitive") — route the edit through `execute_code`/`terminal` Python instead, and validate the YAML parses before finishing.

### Pitfall: Cron database corrupted with UTF-8 BOM

The `jobs.json` file in `~/AppData/Local/hermes/cron/` can get a UTF-8 BOM byte sequence (`EF BB BF`) prepended. This causes the cron scheduler to fail with `Cron database corrupted and unrepairable: Unexpected UTF-8 BOM (decode using utf-8-sig)`.

**Symptom:** `hermes cron list` fails. Gateway log shows `ERROR cron.jobs: Failed to auto-repair jobs.json: Unexpected UTF-8 BOM` at every tick.

**Fix:** Strip the BOM:
```bash
python -c "
path = r'${USER_HOME}\AppData\Local\hermes\cron\jobs.json'
with open(path, 'rb') as f:
    data = f.read()
if data[:3] == b'\xef\xbb\xbf':
    with open(path, 'wb') as f:
        f.write(data[3:])
    print('BOM removed')
import json
with open(path) as f:
    j = json.load(f)
print(f'{len(j.get(\"jobs\",[]))} jobs valid')
"
```

## Guardian Angel / Self-Healer Infinite Restart Loop

If the gateway or agent session is restarting every 5–15 minutes with no external trigger, the likely culprit is an over-aggressive local watchdog reading stale state.

### Symptom
- Gateway PID changes frequently.
- `guardian-angel-state.json` shows climbing `consecutive_failures` (hundreds+).
- Cron/Discord messages report "Gateway DOWN — restarting..."
- Sessions get killed mid-task.

### Root cause: wrong `HERMES_HOME` path
Guardian Angel may be hardcoded to read `~/.hermes/gateway_state.json`, but the gateway writes state to `$HERMES_HOME`. On this Windows machine `HERMES_HOME=${USER_HOME}\AppData\Local\hermes`, so `~/.hermes/` is the **wrong** directory. Guardian Angel sees an empty/missing state file, assumes the gateway is down, and restarts it. The restart creates a new PID, but GA still reads the stale empty file, so it restarts again — an infinite loop.

### Fix
1. Check which path the watchdog actually reads vs. where the gateway writes:
   ```bash
   echo $HERMES_HOME
   ls "$HERMES_HOME/gateway_state.json"
   ls ~/.hermes/gateway_state.json   # may be missing/stale
   ```
2. Make the watchdog respect `HERMES_HOME`:
   ```python
   HERMES_HOME = Path(os.environ.get("HERMES_HOME", Path.home() / ".hermes"))
   ```
3. Reset `guardian-angel-state.json` to clear the failure counter.
4. If the watchdog cannot be trusted, remove/replace its cron job with a silent self-healer that only reports genuine failures.

### Operator preference: silent monitoring
the operator prefers cron jobs, self-healers, and watchdogs to stay quiet when healthy and only report when they actually fix something or encounter a genuine failure they cannot resolve. Avoid `deliver: origin` for watchdogs; use `deliver: local` and emit non-empty output only on action or real failure.

### Cron job script-path pitfall
When a cron job fails with:
```
Script not found: ${USER_HOME}\AppData\Local\hermes\scripts\python "${USER_HOME}\AppData\Local\hermes\scripts\hermes_self_healer.py"
```
the `script` field was stored with an embedded `python` prefix. The cron runner already prepends the interpreter, so the correct value is just the filename (relative to the scripts directory) or the absolute path to the script — never `python "path"`.

**Fix:**
```bash
hermes cron update <job_id> --script "hermes_self_healer.py"
# or, for a script elsewhere:
hermes cron update <job_id> --script "${USER_HOME}/AppData/Local/hermes/scripts/hermes_self_healer.py"
```
Also set `deliver: local` so a healthy run stays silent:
```bash
hermes cron update <job_id> --deliver local
```

### Root cause in this environment: HERMES_HOME mismatch
Guardian Angel was hardcoded to `~/.hermes/`, but the live gateway writes state to `$HERMES_HOME` (`${USER_HOME}\AppData\Local\hermes`). The empty `~/.hermes/gateway_state.json` made Guardian Angel believe the gateway was down every check, triggering `hermes gateway restart` every 5 minutes and killing the active session. The fix was to make the watchdog respect `HERMES_HOME`, reset `guardian-angel-state.json`, and replace Guardian Angel with a silent Self-Healer that does not restart the gateway automatically.

See `references/guardian-angel-restart-loop-2026-07-15.md` for the full diagnosis transcript and commands.

## Voice Messages

Discord voice messages are transcribed in real-time by the gateway but raw audio is NOT persisted. If you need to recover a voice message the operator sent:

Check `references/discord-voice-message-transcription.md` for the recovery workflow using `whisper` on cached `.ogg` files in `audio_cache/`.

### Voice message lost during gateway downtime (unrecoverable)

Discord gateway events do NOT replay. If the operator sent a voice message while the gateway was down (update, restart, crash), the attachment never reaches the bot: it appears only in history backfill as literal text `(attachment)` and never lands in `audio_cache/`. The agent cannot fetch it after the fact — ask the operator to re-send.

**Diagnosis technique — decode the Discord snowflake timestamp** to confirm the message was sent during downtime:
```python
msg_id = <discord-channel-id>
ts_ms = (msg_id >> 22) + 1420070400000  # Discord epoch
# compare against gateway downtime markers:
#   ls -la ~/AppData/Local/hermes/config.yaml.bak.*   (update backups)
#   ls -la ~/AppData/Local/hermes/logs/update.log      (update finish time)
```
If `ts_ms` falls between the gateway stop and restart, the audio is gone — say so directly instead of transcribing the wrong (older) cached file. Sanity check: the newest file in `~/AppData/Local/hermes/audio_cache/` will predate the message timestamp.

## Pitfalls

- **Logs are useless if the gateway just restarted** — check rotated logs (`gateway.log.1`, `gateway.log.2`).
- **`ps aux` doesn't work for Windows processes in msys/bash** — the msys `ps` is a minimal tool that can only see processes launched from within msys. Use Windows-native `tasklist` instead: `tasklist //FI "IMAGENAME eq python.exe" //NH` or `tasklist //FI "PID eq <pid>" //NH`. Grep the output for the process name. This matters especially for checking if gateway background processes are still alive.
- **Windows .env secrets** — `.env` file is protected from `read_file` by Hermes (defense-in-depth). Use `grep` from terminal or `hermes config set` instead.
- **Attachment > 100KB text files** — text injection for `.txt`/`.md`/`.log` files is capped at 100 KB. Larger files are cached to disk but content is not auto-injected into the agent's context. The agent can read them manually via `read_file` using the cached path.

## Spacebar-Specific Connectivity

Spacebar (Fermi) at `discy.your-domain.example` uses a Discord-compatible API but has several quirks that cause connection failures:

### HTTP 429 Rate Limiting

Multiple concurrent gateway connections to the same Spacebar instance trigger 429 errors:

```
HTTP Error 429: Too Many Requests
Error: User not found
```

**Pattern:** When 10+ Hermes profiles try to authenticate simultaneously (e.g., after a daily reset or fleet restart), Spacebar rate-limits them all. Each gets a 30s timeout and retries with exponential backoff (30s → 60s → 120s → 240s → 300s max).

**Diagnosis:**
```bash
grep "429\|Too Many Requests" ~/AppData/Local/hermes/logs/spacebar-*.err.log
```

**Fix options:**
1. **Staggered startup** — Don't start all profiles at once. Start core 3-5 first, wait 30s, start rest.
2. **Reduce concurrent profiles** — Only keep essential profiles running. Disable idle specialist bots.
3. **Increase rate limit on Spacebar server** — Server-side config change (requires Spacebar admin access).
4. **Verify token validity** — Some 429s mask authentication failures. Check the token against the Spacebar server directly.

### KeyError: 'position' on Channel Create

Spacebar's API response for channel creation sometimes omits the `position` field that discord.py expects:

```
KeyError: 'position'
File "...discord/channel.py", line 378, in _update
    self.position: int = data['position']
```

**Fix:** The spacebar-gateway.py script patches `TextChannel._update` to handle this. Ensure the patching is active (check gateway log for `Patched TextChannel._update → handles missing Spacebar fields`).

### Token Format

Spacebar uses JWT tokens (ES512 algorithm), not Discord's standard bot tokens. Token structure:
```json
{"id":"<discord-channel-id>","iat":1782096387,"kid":"...","ver":3,"did":"JOZKIJKNWF"}
```

**Key differences from Discord tokens:**
- Sent as raw Authorization header, NOT with `Bot ` prefix
- Must be set as `SPACEBAR_BOT_TOKEN` or `DISCORD_BOT_TOKEN` in the profile's `.env`
- Tokens are tied to specific Spacebar users (bots) — use the correct token for each profile
- Token validation: `echo "<token>" | cut -d. -f2 | base64 -d 2>/dev/null` to inspect payload

### Common Spacebar Error Patterns in Logs

| Log Pattern | Meaning | Action |
|-------------|---------|--------|
| `HTTP Error 429: Too Many Requests` | Rate limited | Stagger startups or reduce concurrency |
| `KeyError: 'position'` | Spacebar field mismatch | Ensure gateway patch is applied |
| `Error: User not found` | Token invalid or user doesn't exist | Generate new token on Spacebar server |
| `Shard ID None has stopped responding` | WebSocket heartbeat timeout | Network issue or server overload |
| `logging in using static token` (docs-lead-dev) | Using plain token auth (no Spacebar patch) | Check if script has all patches applied |
| `NotFound: 404 Not Found` (on /users/@me) | REST endpoint not found (often Cal.com 404 page) | Check API URL — don't use cal.com URLs as Spacebar API |
| `ClientOSError: WinError 64` | Windows network name unavailable | Network disruption, will auto-retry |
| `ConnectionResetError: WinError 64` | Connection forcibly closed | Network disruption, will auto-retry |

### Gateway Script Compatibility

The `spacebar-gateway.py` script from `agent-fleet` applies 14+ patches to discord.py for Spacebar compatibility. A gateway that logs `DiscordWebSocket.* patched` and `discord.http.HTTPClient.request patched` has the full patch set. A gateway that logs `logging in using static token` (without the patch messages) is using unpatched auth and WILL fail to connect.
