---
name: wechat-remote-control
version: 2.0.0
description: |
  WeChat Remote Control for Claude Code. Three sub-commands:
  - login:  Authenticate WeChat account (scan QR code). Run once before first use
            or after session expiry.
  - attach: Register this Claude Code session as the WeChat remote target.
            Bridge daemon starts in background; it watches the CC session file
            and forwards assistant output to WeChat.
  - sync:   Show WeChat conversation history since last attach, for context.
  Use when stepping away from the terminal and handing off to WeChat.
allowed-tools:
  - Bash
  - Read
  - Edit
---

# /wechat-remote-control

Determine whether the user wants **login**, **attach**, or **sync**, then follow the steps below.

If the user just says `/wechat-remote-control` with no args, default to **attach**.

**Key principle:** When any step encounters a problem, fix it directly by running commands.
Never ask the user to copy-paste and run commands themselves — handle everything here.

---

## Architecture overview (for Claude's reference)

The bridge uses a **tmux-injection** model, bundled in this skill directory.

- **Bridge daemon** (`node src/index.js`): polls ilink WeChat API for messages, injects
  them into the user's tmux-hosted CC session via `tmux send-keys`.
- **Hook server**: listens on Unix socket `/tmp/cc_wechat_hook.sock`. CC hooks (PreToolUse,
  Stop, Notification) send events here via `hook.py`.
- **Response forwarding**: on Stop/Notification hook, reads CC transcript JSONL, finds the
  response to the injected WeChat message, and forwards it to WeChat. Terminal-initiated
  responses are NOT forwarded.
- **All state lives in one directory**: `~/.wechat-remote-control/`
  - `accounts/<accountId>.json` — WeChat credentials
  - `state.json` — tmux target, autoApprove, transcriptPath
  - `bridge.json` / `bridge.pid` / `cc_pid` — daemon metadata
  - `logs/bridge-YYYY-MM-DD.log` — rotated logs (30-day retention)
  - `history.jsonl` — injected messages and forwarded responses

**Critical: process kill safety.** Do NOT use `pgrep -f` or `grep` with bridge path strings
in the same bash command that does other work. Claude Code wraps commands in `bash -c "..."`,
so the pattern matches the shell itself, causing self-termination. Always use the Python
`/proc` scanner shown below, in a **separate** bash call from the start command.

---

## login — Authenticate WeChat account

Run this once before first use, or whenever the bridge reports session expiry.

### Step 1: Check if already logged in

```bash
ls ~/.wechat-remote-control/accounts/*.json 2>/dev/null | head -1
```

If account files exist, note them and ask the user whether they want to re-login
or if this was triggered by a session expiry. If they're just setting up fresh, proceed.

### Step 2: Locate skill directory and ensure dependencies

```bash
SKILL_DIR=$(find "$HOME" -maxdepth 7 -type f -name "login.js" 2>/dev/null \
  | grep "wechat-remote-control/dist/wechat/login.js" | head -1 \
  | sed 's|/dist/wechat/login.js||')
echo "SKILL_DIR=${SKILL_DIR:-NOT_FOUND}"
test -d "$SKILL_DIR/node_modules/qrcode" && echo "qrcode: OK" || echo "qrcode: missing"
```

Note the SKILL_DIR value. If qrcode is missing, install it:

```bash
cd "$SKILL_DIR" && npm install --production --ignore-scripts 2>&1 | tail -3
```

### Step 3: Fetch QR code and display

Replace `SKILL_DIR` with the actual path found above, then run:

```bash
node --input-type=module -e "
  import { createRequire } from 'module';
  import { startQrLogin } from 'SKILL_DIR/dist/wechat/login.js';

  const { qrcodeUrl, qrcodeId } = await startQrLogin();

  let qrcodeText = null;
  try {
    const require = createRequire('SKILL_DIR/package.json');
    const QRCode = require('qrcode');
    qrcodeText = await new Promise((res, rej) =>
      QRCode.toString(qrcodeUrl, { type: 'utf8', small: true, margin: 0 }, (e, s) => e ? rej(e) : res(s))
    );
  } catch(e) {
    // qrcode not available
  }

  console.log(JSON.stringify({ qrcodeUrl, qrcodeId, qrcodeText }));
"
```

Parse the JSON. Then **in the same reply**, output `qrcodeText` verbatim as a code block,
then **immediately** run the waitForQrScan command below — do NOT wait for user input.
Example reply:

```
请用微信扫描以下二维码登录：

​```
<qrcodeText here>
​```
```

If `qrcodeText` is null, show the URL instead.

### Step 4: Wait for scan (run immediately after displaying QR — no user input needed)

Replace `SKILL_DIR` and `QRCODE_ID` with actual values:

```bash
node --input-type=module -e "
  import { waitForQrScan } from 'SKILL_DIR/dist/wechat/login.js';
  const result = await waitForQrScan('QRCODE_ID');
  console.log(JSON.stringify({ status: 'confirmed', accountId: result.accountId }));
"
```

This blocks until the user scans. Allow up to 3 minutes. If it throws "expired", go back
to Step 3 to get a fresh QR code and display it again.

### Step 5: Verify and report

```bash
ls ~/.wechat-remote-control/accounts/*.json 2>/dev/null
```

If no files: retry from Step 3. Otherwise confirm login success.

---

## attach — Register this session as WeChat remote target

### Step 1: Pre-flight checks (run all in one bash call)

```bash
echo "=== bridge installed ==="
test -f $HOME/.claude/skills/wechat-remote-control/src/index.js && echo "OK" || echo "NOT_FOUND"
echo "=== account ==="
ls ~/.wechat-remote-control/accounts/*.json 2>/dev/null | head -1 || echo "NOT_FOUND"
echo "=== tmux ==="
echo "SESSION:$(tmux display-message -p '#S' 2>/dev/null); WINDOW:$(tmux display-message -p '#I' 2>/dev/null); PANE:$(tmux display-message -p '#P' 2>/dev/null)" || echo "NOT_IN_TMUX"
echo "=== existing attach ==="
cat ~/.wechat-remote-control/state.json 2>/dev/null || echo "{}"
```

**If bridge NOT_FOUND:** tell user bridge is not installed, stop.
**If account NOT_FOUND:** run **login** flow first, then continue.
**If NOT_IN_TMUX:** tell user they must run CC inside tmux. Stop.

### Step 2: Check for existing attach — prompt for override

If `state.json` shows `active: true` and `injectTarget` exists, show the user:

> "WeChat Remote Control is currently attached to tmux `<session>:<window>.<pane>`
>  (since <attachedAt>). Override with this session? [Y/n]"

Default: **Y** (override). If user says no, stop.

### Step 3: Write state.json and bridge.json

Detect the current tmux target via **process ancestry** (reliable) and transcript path automatically.
`$PPID` in the bash subprocess is the CC process PID.

**Critical:** Do NOT use `tmux display-message` for the pane — it reports the currently
focused client window, not the pane where CC lives. Use process ancestry via /proc instead.

```bash
CWD=$(pwd)
CC_PID=$PPID
ENCODED=$(echo "$CWD" | sed 's|[^a-zA-Z0-9-]|-|g')
TRANSCRIPT=$(ls -t "$HOME/.claude/projects/$ENCODED"/*.jsonl 2>/dev/null | head -1)
SESSION_ID=$(basename "$TRANSCRIPT" .jsonl 2>/dev/null)
python3 -c "
import json, os, time, datetime, subprocess

cc_pid = $CC_PID
cwd = '$CWD'
transcript = '$TRANSCRIPT'
session_id = '$SESSION_ID'

# Find the tmux pane where this CC process lives via /proc ancestry
tmux_session = tmux_window = tmux_pane = None
try:
    result = subprocess.run(
        ['tmux', 'list-panes', '-a', '-F', '#{pane_pid}\t#{session_name}\t#{window_index}\t#{pane_index}'],
        capture_output=True, text=True
    )
    pane_map = {}
    for line in result.stdout.strip().split('\n'):
        parts = line.split('\t')
        if len(parts) == 4:
            pane_map[int(parts[0])] = tuple(parts[1:])
    pid = cc_pid
    while pid > 1:
        if pid in pane_map:
            tmux_session, tmux_window, tmux_pane = pane_map[pid]
            break
        try:
            with open(f'/proc/{pid}/status') as f:
                for line in f:
                    if line.startswith('PPid:'):
                        pid = int(line.split()[1]); break
        except:
            break
except Exception as e:
    print(f'pane scan error: {e}')

if not tmux_session:
    # Fallback
    import subprocess as sp
    tmux_session = sp.run(['tmux', 'display-message', '-p', '#S'], capture_output=True, text=True).stdout.strip()
    tmux_window  = sp.run(['tmux', 'display-message', '-p', '#I'], capture_output=True, text=True).stdout.strip()
    tmux_pane    = sp.run(['tmux', 'display-message', '-p', '#P'], capture_output=True, text=True).stdout.strip()

d = os.path.expanduser('~/.wechat-remote-control')
os.makedirs(d, exist_ok=True)

# Write state.json
state = {
    'injectTarget': {
        'session': tmux_session, 'window': tmux_window, 'pane': tmux_pane,
        'attachedAt': int(time.time() * 1000)
    },
    'autoApprove': True, 'active': True, 'transcriptPath': transcript
}
with open(os.path.join(d, 'state.json'), 'w') as f:
    json.dump(state, f, indent=2)

# Write bridge.json
bridge = {
    'sessionId': session_id, 'cwd': cwd, 'ccPid': cc_pid,
    'attachedAt': datetime.datetime.now(datetime.timezone.utc).isoformat()
}
with open(os.path.join(d, 'bridge.json'), 'w') as f:
    json.dump(bridge, f, indent=2)

# Store ccPid separately
with open(os.path.join(d, 'cc_pid'), 'w') as f:
    f.write(str(cc_pid))

# Update sessions.json active to this session.
# Strategy: set active=null so the bridge's auto-pick logic kicks in on next scan.
# The bridge (lines 350-362 in src/index.js) prefers the session whose tmux matches
# state.json's injectTarget — which we just wrote correctly above.
# Do NOT try to match by name here: sessions.json may have stale tmux values from
# before the bridge scanner ran, causing wrong matches (e.g. exp2 at 0:4.0 which later
# moves to 0:2.0 after the scanner updates it).
tmux_target = f'{tmux_session}:{tmux_window}.{tmux_pane}'
sessions_path = os.path.join(d, 'sessions.json')
if os.path.exists(sessions_path):
    sessions = json.load(open(sessions_path))
    sessions['active'] = None
    with open(sessions_path, 'w') as f:
        json.dump(sessions, f, indent=2)
    print(f'OK: target={tmux_target} active=null (bridge will auto-pick) ccPid={cc_pid}')
else:
    print(f'OK: target={tmux_target} ccPid={cc_pid}')
"
```

### Step 4: Configure hooks in settings.json

Read `~/.claude/settings.json`. Merge the hooks — do not overwrite other settings.

Target hooks config:
```json
{
  "hooks": {
    "PreToolUse": [{"matcher": "", "hooks": [{"type": "command", "command": "python3 $HOME/.claude/skills/wechat-remote-control/hook.py pretooluse"}]}],
    "Stop": [{"matcher": "", "hooks": [{"type": "command", "command": "python3 $HOME/.claude/skills/wechat-remote-control/hook.py stop"}]}],
    "Notification": [{"matcher": "", "hooks": [{"type": "command", "command": "python3 $HOME/.claude/skills/wechat-remote-control/hook.py notification"}]}]
  }
}
```

If hooks are already present with the same commands, skip this step.

### Step 5: Configure status line in settings.json

Check if `statusLine` is already configured. If not (or if the command points elsewhere),
merge it into `~/.claude/settings.json` without overwriting other settings:

```bash
python3 -c "
import json, os
path = os.path.expanduser('~/.claude/settings.json')
settings = json.load(open(path)) if os.path.exists(path) else {}
desired = {
    'type': 'command',
    'command': 'bash \$HOME/.claude/skills/wechat-remote-control/status.sh'
}
if settings.get('statusLine') == desired:
    print('ALREADY_SET')
else:
    settings['statusLine'] = desired
    with open(path, 'w') as f:
        json.dump(settings, f, indent=2)
    print('OK')
"
```

If `ALREADY_SET`, skip silently.

### Step 6: Ensure bridge daemon is running (service model)

The bridge is a singleton service. Check if it's already running via PID file before starting.
Never kill a healthy bridge just because attach was called again.

**Check existing daemon:**

```bash
PID_FILE="$HOME/.wechat-remote-control/bridge.pid"
BRIDGE_RUNNING=0
if [ -f "$PID_FILE" ]; then
    STORED_PID=$(cat "$PID_FILE")
    if kill -0 "$STORED_PID" 2>/dev/null; then
        echo "already running PID=$STORED_PID"
        BRIDGE_RUNNING=1
    else
        echo "stale PID file, cleaning up"
        rm -f "$PID_FILE"
    fi
fi
echo "BRIDGE_RUNNING=$BRIDGE_RUNNING"
```

**Only if BRIDGE_RUNNING=0 — start daemon** (separate bash call):

```bash
nohup node $HOME/.claude/skills/wechat-remote-control/src/index.js >> /tmp/cc_wechat_bridge.log 2>&1 &
NEW_PID=$!
echo $NEW_PID > $HOME/.wechat-remote-control/bridge.pid
echo "PID=$NEW_PID"
```

**Verify** (after ~3 seconds):

```bash
kill -0 <NEW_PID> 2>/dev/null && echo "running" || echo "FAILED"
```

If FAILED: read the last 30 lines of `/tmp/cc_wechat_bridge.log` and diagnose.

### Step 7: Report success

```
WeChat Remote Control activated

Tmux target: <session>:<window>.<pane>
Auto-approve: on
Bridge: running (PID <pid>)
Transcript: <transcript path>

You can leave the terminal now. WeChat messages will be injected into this
CC session via tmux. CC responses triggered by WeChat will be forwarded back.

Terminal-initiated responses are NOT forwarded to WeChat.
```

---

## sync — Show WeChat conversation history

### Step 1: Format and show history

```bash
python3 $HOME/.claude/skills/wechat-remote-control/format_history.py 2>/dev/null \
  || (tail -20 ~/.wechat-remote-control/history.jsonl 2>/dev/null || echo "No WeChat history found.")
```

If no history exists, check the bridge logs:

```bash
tail -50 ~/.wechat-remote-control/logs/bridge-$(date +%Y-%m-%d).log 2>/dev/null | grep -E "INFO|WARN|ERROR" | tail -20
```

### Step 2: Summarize

Give a one-line summary of what happened while the user was away.
