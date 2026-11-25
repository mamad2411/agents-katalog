---
name: mcp-subprocess-dead-detection
description: Diagnose and handle MCP servers whose parent process is alive but the managed subprocess (tor daemon, database, browser, worker) has silently died. Cross-reference MCP tool responses with OS-level probes.
version: 1.0.0
author: Hermes Agent
metadata:
  hermes:
    tags: [mcp-servers, fleet-health, subprocess, monitoring, diagnostic, stale-state]
    triggers:
      - MCP server reports alive but subprocess dead
      - stale MCP configured state
      - subprocess managed by MCP died
      - MCP server alive but daemon gone
      - configured but not running
      - port hostage Docker takeover
      - MCP port claimed by another service
      - HTTP responds but MCP init fails
      - false positive health endpoint
      - tool returns pre-fix error despite fixed code
      - duplicate MCP server process
    related_skills: [mcp-fleet-audit, infrastructure-self-healing-pulse, tor-circuit-rotation]
---

# MCP Subprocess Dead Detection

## Scenario

An MCP server's own process is alive and responding to tool calls, but the
subprocess it manages (daemon, database instance, browser engine, worker) has
silently died. The server reports a stale "configured" or "running" state
because it hasn't detected the subprocess death yet.

**Real example:** The tor_camoufox_bridge MCP server reported
`tor_browser: {status: "configured"}` while `tor.exe` was completely absent
from disk. The bridge's internal broken-connection detection never fired
because no tor process existed to lose a connection to.

## Diagnostic Sequence

When an MCP server's status tools report "configured", "running", or "alive"
but the expected service is unreachable:

### 1. OS-level process check

```bash
# By process name
MSYS_NO_PATHCONV=1 tasklist.exe /FI "IMAGENAME eq <daemon>.exe" /NH /FO CSV

# By port (cross-reference from MCP server documentation)
netstat -ano | grep LISTENING | grep <expected_port>

# By PID (if the MCP server exposes the PID)
powershell.exe -Command "Get-Process -Id <pid> -ErrorAction SilentlyContinue | Select-Object Id, ProcessName, SessionId"
```

**Windows git-bash quirk:** `tasklist.exe /FI "IMAGENAME eq tor.exe"` can return
empty even when the process IS running (MSYS fails to match Services-session
processes). When IMAGENAME returns no matches but netstat shows ports, try
PID-based filtering or PowerShell.

### 2. Protocol-level probe

If the MCP server manages a daemon that listens on ports, verify the daemon's
protocol is actually responsive — not just the port being open:

| Managed Service | Probe |
|----------------|-------|
| Tor SOCKS5 | `curl --socks5-hostname 127.0.0.1:9250 -s --max-time 10 https://api.ipify.org` |
| Tor control | `PROTOCOLINFO` → `AUTHENTICATE` → `GETINFO circuit-status` on port 9251 |
| PostgreSQL | `psql -h 127.0.0.1 -U <user> -d <db> -c "SELECT 1;"` |
| HTTP server | `curl -s -o /dev/null -w "%{http_code}" http://localhost:<port>/` |
| Firefox CDP | `curl -s -o /dev/null -w "%{http_code}" http://localhost:9222/json/version` |

A port that's LISTENING without responding to its protocol is a dead daemon
with a zombie socket (often held open by the MCP server process).

### 3. Binary existence check

The daemon binary itself may be missing from disk while the MCP server holds
a stale "configured" state:

```bash
ls -la ${USER_HOME}/path/to/daemon.exe 2>/dev/null || echo "BINARY MISSING"
```

## Recovery

1. **If the binary is missing:** Reinstall the software. The MCP server cannot
   auto-recover because there's nothing to launch.

2. **If the binary exists but the daemon is dead:** Kill the MCP server process
   (Hermes auto-restarts it, which typically spawns a fresh daemon):
   ```bash
   MSYS_NO_PATHCONV=1 taskkill.exe /F /PID <mcp_server_pid>
   ```
   Wait 15-30s for Hermes to restart the MCP server and verify:
   ```bash
   netstat -ano | grep LISTENING | grep <expected_port>
   ```

3. **If the MCP server manages the daemon via an internal connection** (not a
   subprocess), trigger a recovery action through the MCP tools if available:
   - `browser_new_identity()` for tor_camoufox_bridge
   - `tor_recover_browser()` for tor-browser-mcp
   - Service restart tool or health endpoint

   **⚠️ Bridge managed-tool recovery may not work when the subprocess is truly gone.**
   The tor_camoufox_bridge's `browser_navigate()` and `browser_new_identity()` commands
   are ACKNOWLEDGED but NON-FUNCTIONAL when tor.exe is completely absent (no process,
   no ports). They do NOT auto-start the daemon — `browser_navigate()` spawns orphan
   Firefox processes but tor stays dead. If the bridge's management tools fail to
   revive the daemon, escalate to manual start (below).

4. **Manual subprocess start (alternative when killing MCP server isn't feasible):**
   If the MCP server holds a stale "configured" state but the daemon binary exists
   on disk, start the daemon manually using the MCP server's own config:

   ```bash
   # Find the config file in the MCP server's session/temp directory
   # (varies per service — tor example below)
   tor -f "${USER_HOME}/AppData/Local/Temp/torbrowser-driver-<sessid>/torrc"

   # Wait for bootstrap (check the daemon's log or port availability)
   sleep 12
   netstat -ano | grep LISTENING | grep <expected_port>
   ```

   The existing auth credentials in the session directory (auth cookie, config
   tokens) remain valid because the MCP server's state file is untouched by
   the daemon death. After starting the daemon manually, the MCP server's tools
   should work normally again — no Hermes restart needed.

   **When to use this over killing the MCP server:**
   - Cron sessions where taskkill may produce ACCESS_DENIED
   - The MCP server is managing multiple resources and a restart would
     disrupt others
   - Quick recovery is needed (manual start takes ~12s vs 30-60s for
     Hermes MCP restart cycle)

## Complementary Pattern: Port Hostage (Docker Takeover)

**Scenario:** A non-MCP process (often a Docker container) binds to a port an MCP server previously used. The port responds to HTTP — `curl /health` returns `{"ok":true}` — but the MCP initialize handshake fails. The stale config entry silently persists.

**Real example:** brainmd on port 3000 was overtaken by Buzz Nostr Relay (Docker). The relay's own HTTP server responded to `GET /health` with `{"ok":true}` — indistinguishable from brainmd without an MCP-level probe. Took 4 days to diagnose because HTTP-level probes gave false positives.

**Diagnosis:**
```bash
# 1. Identify Docker containers binding to suspect ports
docker ps --format "{{.Names}} {{.Ports}}" | grep ":<PORT>->"

# 2. MCP initialize handshake — the ONLY reliable liveness test
curl -s http://localhost:<PORT>/mcp \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","method":"initialize","id":1,"params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"audit","version":"1.0"}}}'
# A non-MCP service returns garbage or an error, not a proper serverInfo response.

# 3. Cross-reference with the process that started the MCP server
# If the original was started manually or via stdio and Docker now owns the port
# → permanent displacement
```

**Resolution:** Remove the stale config.yaml entry. Docker containers persist across reboots and never yield ports. Do NOT leave "find alternative port" as a TODO.

**Windows `ss` blindspot:** On Windows git-bash, `ss -tlnp` does NOT report Docker host port bindings (Docker for Windows routes through Hyper-V/WSL2). Always cross-check Docker ports with:
```bash
docker ps --format "{{.Names}} {{.Ports}}" | grep "<PORT>:"
curl -s -o /dev/null -w "%{http_code}" --max-time 3 http://localhost:<PORT>/
```
Only conclude a Docker-hosted MCP server is down when BOTH `docker ps` shows `Exited` AND `curl` fails.

**Distinction from other failure modes (extended):**

| Symptom | Most Likely Cause |
|---------|-------------------|
| Port silent, no process | Daemon never started or binary missing |
| Port listening, protocol times out | Hung daemon (process exists but unresponsive) |
| Port listening, connection refused | Zombie socket from dead process, held by another app |
| Port responds to HTTP but MCP init fails | **Port hostage** — Docker container or other non-MCP process took over the port |
| MCP says "configured", all OS checks confirm dead | Stale state — MCP parent alive, child dead |
| MCP says "configured", processes exist, ports open | Genuinely healthy |
| Tool returns a pre-fix error; on-disk code is correct | **Stale module in live process** — process started before the fix commit (see pattern below) |
| One tool on a server fixed, another still errors | **Partial-fix fingerprint** — live process loaded a file version between two fixes |

## Complementary Pattern: Stale Module in Live MCP Process (Duplicate Instances)

**Scenario:** A tool still returns an error you already fixed. The on-disk code is correct, but the live MCP server process loaded the module BEFORE the fix was committed — a restart is required even though the config is perfect.

**Real example (2026-08-03):** `trading-signals` `technical_signals` kept returning `Unexpected data format: dict` while `market_summary` returned correct live data. Both processes had started 02:31 ET — before fix commit `890da31` (12:53 UTC). `market_summary` worked because its fix was saved to disk before the restart; `technical_signals`' fix came after. A fresh-import of the on-disk code produced full valid output → purely a stale-process issue, NOT a code regression.

**Diagnosis sequence:**

1. **List every process running the server script, with start times** (Windows):
```bash
powershell -NoProfile -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe'\" | Where-Object { \$_.CommandLine -like '*<script-name>*' } | Select-Object ProcessId, CreationDate, CommandLine | Format-List"
# Fallback: wmic process where "name='python.exe'" get processid,creationdate,commandline | grep -i <script-name>
```
2. **Compare CreationDate to the fix commit time** — `git log --oneline -1 -- <script>`. Process started before the commit ⇒ it loaded the pre-fix module.
3. **Check for duplicate PIDs running the same script** — a stale instance frequently runs on system Python while the correct one runs on a pinned venv, both spawned in the same restart second. Only one config entry may exist; the stray instance can shadow the correct one (same-name tools may route to either).
4. **Prove the disk code is correct before blaming config** — fresh-import and call the tool directly with the venv interpreter. Hyphenated filenames (`trading-signals-mcp.py`) can't be imported by module name — use `importlib.util.spec_from_file_location`:
```python
import importlib.util, sys
spec = importlib.util.spec_from_file_location('tsm', 'trading-signals-mcp.py')
m = importlib.util.module_from_spec(spec); sys.modules['tsm'] = m
spec.loader.exec_module(m)
print(m.technical_signals('SPY'))
```
If the fresh run works → restart Hermes and re-verify. Do NOT re-debug code that a fresh import proves correct.

**Resolution:** Restart Hermes (kills both instances, spawns only the configured one). No config change needed.

## Pitfalls

- **Don't trust the MCP server's self-report alone.** The MCP process can be
  alive and responding to tool calls while the subprocess it manages is long
  dead. Always cross-reference with OS-level probes.

- **Bridge MCP management tools (browser_navigate, browser_new_identity, etc.)
  may ACKNOWLEDGE commands but NOT execute them when the subprocess is gone.**
  The tor_camoufox_bridge returns success strings like "Navigating Tor Browser
  to about:blank" or "NEWNYM requested for Tor circuit rotation" even though
  `tor.exe` is absent and no action can occur. The bridge's management tools
  send commands to an internal control channel that doesn't exist. Always verify
  with an OS-level probe (port check, process check, or protocol-level response)
  AFTER calling a recovery tool — don't take the acknowledgment as proof of
  recovery.
- **`tasklist.exe` by IMAGENAME can miss Services-session processes on MSYS.**
  Use PID-based filtering or PowerShell when in doubt.
- **Auto-recovery may not fire when there's nothing to start.** If the daemon
  binary is missing, the MCP server's broken-connection detection never triggers
  because no connection was ever established.
- **Creating new connections to a dead daemon's zombie socket** (CLOSE_WAIT)
  accelerates the system-wide timeout state. If 3+ connections have already
  timed out, skip retries and escalate to a process kill.
- **Not all MCP servers manage subprocesses.** Stdio MCP servers (pipelines,
  transformers, stateless APIs) don't have this problem because they handle
  each request in-process.
