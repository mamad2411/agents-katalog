# Copilot Babysitter Skill

## Purpose
Monitor the VS Code GitHub Copilot Agent and automatically nudge it to continue
when it stalls, stops reporting progress, or waits unnecessarily for user input.

**Key capability**: Works through macOS screen lock — no need to keep the screen unlocked.

## Design philosophy: semantic judgment, not fixed states

Copilot going **silent is not one state** — it can mean very different things, and each
needs the opposite response:

| Why Copilot is silent | Correct response |
|---|---|
| **Done** — finished the mission, nothing left to do | Stay silent |
| **Truly working** — a real background process is running; it will report | Stay silent |
| **Stuck** — abandoned a monitoring loop, forgot to continue, hit a transient error, or "promised to ping" but can't self-resume | **Nudge to continue** |
| **Asking a routine question** — "shall I proceed?", "which order?", "want me to fix X now?", or already gave a recommendation | **Answer it yourself, nudge with the decision** |
| **Needs a real human** — needs a secret/credential, a destructive/irreversible action, an external/manual action, or a costly trade-off with no clear best option | **Notify Roie** |

The babysitter is smart enough to make routine engineering decisions on Roie's behalf.
It must NOT bounce every "should I continue?" question to Roie — that just recreates the
stall. It answers routine questions itself (approving Copilot's own recommendation, or
using obvious engineering sense like "validate before refactoring" / "fix the blocker
first" / "prove the pattern early") and tells Copilot to proceed autonomously. It only
escalates to Roie for genuinely human matters: secrets/credentials, destructive or
irreversible actions (deleting prod, force-push, spending money, notifying external
people), external actions the agent can't perform, or a real trade-off where guessing
wrong is costly.

Older versions used rigid keyword/state rules (`ONLY_MESSAGE_ON_USER_INPUT`, `wait`,
etc.) that lumped *done / working / stuck* all under "idle" and stayed silent for all of
them — so a Copilot that falsely believed it was "monitoring a deploy" (but had actually
done nothing for hours) slipped through unnoticed.

The current design instead hands the **raw conversation** to the LLM automation, which
**reads it and reasons about *why* Copilot went quiet**. The `supervisor.py` script is a
dumb sensor + actuator; the LLM is the brain:

- `supervisor.py context` → emits a rich LLM-ready snapshot (no decision made).
- `supervisor.py nudge "<msg>"` → sends an LLM-authored, context-specific message.

The deterministic `once` / `monitor` paths still exist for backward compatibility, but the
recommended flow is the semantic one below.

## Setup (One-Time)

### Prerequisites
- macOS
- VS Code with GitHub Copilot extension
- Clawpilot (for automation scheduling)

### Install the copilot-nudge-server Extension

The babysitter relies on a small VS Code extension that runs an HTTP server inside VS Code's
extension host process. This allows sending messages to Copilot Chat  evenprogrammatically 
when the screen is locked.

**Install steps:**

1. Copy the extension to VS Code's extensions folder:
   ```bash
   mkdir -p ~/.vscode/extensions/copilot-nudge-server-0.0.1
   cp extension/extension.js ~/.vscode/extensions/copilot-nudge-server-0.0.1/
   cp extension/package.json ~/.vscode/extensions/copilot-nudge-server-0.0.1/
   ```

 "Developer: Reload Window")

3. Verify the extension is running:
   ```bash
   curl -s http://127.0.0.1:19876/health
   # Expected: {"status":"ok","port":19876,"version":2}
   ```

**Why this works through screen lock:**
- The extension runs as a Node.js HTTP server inside VS Code's extension host process
- It uses internal VS Code commands (`workbench.action.chat. no keyboard/UI injectionopen`) 
- The HTTP server stays active regardless of display sleep or screen lock state
- Messages are queued by Copilot when the agent is busy; processed in order when ready

### Register the Automation in Clawpilot

Create a Clawpilot automation that runs every 2 minutes:
- Name: "Copilot Agent Monitor"
- Schedule: "every 2 minutes"
- Prompt: (see the automation prompt template in this skill)

## Architecture (Clawpilot Automation Mode)

The babysitter runs as a Clawpilot automation (every 2 minutes). Each run:

1. **Check  `stat -f "%m"` on the session file vs current timestaleness** 
2. **If active (< no action needed, report OK90s)** 
3. **If stalled (> diagnose and nudge:90s)** 
   a. Try HTTP nudge first (works through screen lock)
   b. If HTTP fails, check screen lock status
   c. Read session context for what agent was doing
   d. Determine if agent needs nudge or hit real blocker
   e. Send contextual nudge OR alert Roie via Teams
4. **Post-nudge  60s after nudge, re-check timestamp changedverification** 

## Screen Lock Handling

**Problem**: When macOS screen is locked, all UI automation (osascript keystrokes) silently
 text goes to the lock screen password field. osascript still returns exit 0.fails 

**Solution**: The HTTP nudge bypasses this entirely. The decision tree is:

```
1. Try HTTP nudge (curl POST to :19876)
 done (works through screen lock!)

      2. Check screen lock (ioreg)
 Teams alert only, cannot nudge via UI
 try UI nudge (osascript fallback)
```

**Screen lock detection:**
```bash
ioreg -n Root -d1 -w0 | grep -q '"IOConsoleLocked" = Yes'
# Exit 0 = screen IS locked, Exit 1 = screen is unlocked
```

## Nudge Methods

### PRIMARY: HTTP (Non-UI, Works Through Screen Lock)

```bash
curl -s -X POST http://127.0.0.1:19876/nudge \
  -H "Content-Type: application/json" \
  -d '{"message": "YOUR_MESSAGE"}'
```

**Health check** (verify extension is running):
```bash
curl -s http://127.0.0.1:19876/health
# Returns: {"status":"ok","port":19876,"version":2}
```

**File-based alternative** (if HTTP unreachable):
```bash
echo 'YOUR_MESSAGE' > ~/.copilot/nudge-queue.txt
```
The extension polls this file every 2 seconds.

### FALLBACK: UI (Only When HTTP Fails AND Screen Unlocked)

```applescript
tell application "Code" to activate
delay 0.5
tell application "System Events"
    tell process "Code"
        key code 35 using {command down, shift down}  -- Cmd+Shift+P
        delay 0.5
        keystroke "chat focus input"
        delay 0.3
        keystroke return
        delay 0.4
        keystroke "YOUR_MESSAGE_HERE"
        delay 0.2
        keystroke return
    end tell
end tell
```

## Session File Monitoring

**Target session** (update these for your workspace):
- Workspace hash: `680f52b117f3c92a8c4998a69b70dacc`
- Session ID: `3df56667-99c5-4383-ac30-7acb02f89aa9`
- Full path: `~/Library/Application Support/Code/User/workspaceStorage/{hash}/chatSessions/{sessionId}.jsonl`

**Staleness check**:
```bash
stat -f "%m" "$SESSION_FILE" && date +%s
 stalled
```

## Auto-Nudge Policy (semantic)

The LLM automation reasons over `supervisor.py context` and acts only when needed:

1. **Working / Done** → do nothing (stay silent).
2. **Stuck** → send ONE tailored nudge via `supervisor.py nudge "<msg>"`. The command
   enforces `MAX_NUDGES` (default 5) consecutive nudges and records state.
3. **Already nudged, no reaction yet** (`nudged_since_last_activity: true`) → wait one
   cycle; do not double-nudge.
4. **Nudge counter auto-resets** the moment Copilot writes to the session after a nudge
   (it reacted), so a fresh stall later starts from zero.
5. **After `MAX_NUDGES` with no progress** → back off and alert Roie via Teams.
6. **Routine question** ("shall I proceed?", "which order?", "want me to fix X now?", or
   Copilot already gave a recommendation) → **answer it yourself** and nudge with the
   decision. Approve Copilot's recommendation, or use obvious engineering sense (validate
   before refactoring, fix the blocker first, prove the pattern early). Also tell Copilot
   to keep going autonomously and stop only for genuinely human matters — not just to ask
   permission to continue.
7. **Needs a real human** → do NOT nudge; notify Roie via Teams. Reserve this for: a
   secret/credential/OTP only Roie has; a destructive or irreversible action (delete prod,
   force-push, spend money, notify external people); an external/manual action the agent
   can't perform; or a costly trade-off with no clear best option.

**Answering routine questions is the default, not the exception.** Bouncing every
"should I continue?" back to Roie recreates the very stall the babysitter exists to
prevent. The nudge message should state the decision clearly (which option / what order /
"yes, proceed"), a brief why, and instruct Copilot to continue autonomously.

**Detecting a false "still working" claim** — treat as *stuck* when Copilot says things like
"I'll ping you when it clears", "I'll report at the next milestone", or "still building",
but has been idle a long time (background agents CANNOT self-resume — once the turn ends
Copilot waits forever), or it repeats the same "same phase as last check" status across
turns with no new tool activity. When in doubt between *working* and *stuck*, treat as stuck.

**Nudge messages must be contextual** — read what the agent was doing and tell it exactly
what to do next. For an abandoned background/deploy watch: instruct it to re-check NOW
(tail the log, grep for errors, `pgrep` the process, verify real state directly via
`az`/`kubectl`), decide whether the job finished/failed/stalled, then proceed or fix.
Do NOT just send "continue".

## Teams Status Updates

Only message Roie for genuine human-in-the-loop blockers or after max-nudge back-off —
keep it to 1-2 lines with the session title and the exact thing Copilot is waiting for.
Do not send routine "still working" status pings.

## Helper Tools

### supervisor.py commands
```bash
# Rich LLM-ready snapshot (idle time, mission, last response, tool states,
# nudge bookkeeping). Makes NO decision — the LLM reasons over this.
python3 ~/.copilot/skills/copilot-babysitter/supervisor.py context

# Send an LLM-authored message to Copilot chat (respects MAX_NUDGES; --force overrides).
# Prefer piping via stdin (heredoc) so backticks, $(...), quotes, or ! in the message
# are NOT interpreted by the shell:
python3 ~/.copilot/skills/copilot-babysitter/supervisor.py nudge <<'NUDGE_EOF'
your tailored message here
NUDGE_EOF
# (An inline arg also works for simple messages: supervisor.py nudge "message")

# Clear the consecutive-nudge counter (e.g. after the user intervenes manually).
python3 ~/.copilot/skills/copilot-babysitter/supervisor.py reset

# Keep-awake: ensure a detached `caffeinate` keeps the Mac from idle-sleeping
# so the every-2-minute monitor never stalls. Idempotent. This is invoked
# AUTOMATICALLY on every `context` call, so normally you never run it by hand.
python3 ~/.copilot/skills/copilot-babysitter/supervisor.py keepawake
python3 ~/.copilot/skills/copilot-babysitter/supervisor.py stopawake   # stop it

# Legacy/diagnostic:
python3 ~/.copilot/skills/copilot-babysitter/supervisor.py status
python3 ~/.copilot/skills/copilot-babysitter/supervisor.py read 3
python3 ~/.copilot/skills/copilot-babysitter/supervisor.py once     # deterministic one-shot
```

The `context` snapshot includes `nudged_since_last_activity` and `nudge_count` so the LLM
can avoid double-nudging and knows when to back off. It also includes a `keepawake` field
(`started` / `already-running` / `skipped`) confirming the anti-sleep guard is active.

## Keeping the machine awake (anti-sleep)

Scheduled automations only fire while the Mac is awake and the app is running — a sleeping
machine silently skips 2-minute ticks (this caused a ~1h monitoring gap once). To prevent
idle-sleep, `supervisor.py context` automatically ensures a detached `caffeinate -dimsu`
process is running (tracked via `~/.copilot/copilot-supervisor-caffeinate.pid`, idempotent,
macOS-only). No manual step is needed.

**Caveat — clamshell (lid-closed) sleep:** `caffeinate` does NOT prevent a MacBook from
sleeping when the lid is closed on battery. For that, additionally run (needs admin/password):
```
sudo pmset -a disablesleep 1     # prevent lid-close sleep
sudo pmset -a disablesleep 0     # re-enable normal sleep later
```

## Requirements

| Component | Purpose | Required? |
|-----------|---------|-----------|
| copilot-nudge-server extension | HTTP nudge (primary) | **Yes** |
| Accessibility permissions | UI fallback only | No (if HTTP works) |
| macOS `ioreg` | Screen lock detection | Yes |
| Clawpilot automation | Scheduling | Yes |

## Known Limitations

- If VS Code crashes or reloads, extension reactivates automatically on next startup
- Session file can be very large ( too big to parse last line efficiently300MB+) 
- osascript returns exit 0 even when keystrokes fail (UI fallback only)
- Extension uses port 19876; if port is taken it tries 19877
- Anti-sleep `caffeinate` cannot prevent lid-closed (clamshell) sleep on battery — use `sudo pmset -a disablesleep 1` for that

## Extension Source

The extension source is in `extension/` in this repo. See `extension/extension.js` and
`extension/package.json`.
