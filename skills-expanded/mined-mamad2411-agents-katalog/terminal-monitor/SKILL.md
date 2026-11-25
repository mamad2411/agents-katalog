---
name: terminal-monitor
description: >
  Utility skill for opening a named terminal pane (tmux or iTerm2) to monitor
  a background Agent-tool teammate or a plain Bash background task in real
  time. For agents (mode: agent), the pane is driven by pushing the native
  <teammate-message>/idle_notification events the orchestrator already
  receives — no output file involved. For plain Bash background tasks (mode:
  bash-task), the pane tails the task's real output_file. Call this skill
  before launching any Agent or Bash background task, passing mode, label,
  pane-name, and the relevant identifier as context. Detects terminal type
  once per session and reuses it across calls.
license: MIT
metadata:
  author: Wesley Egberto
  version: "2.0.0"
  domain: developer-experience
  scope: utility
  role: helper
  triggers: open pane, monitor agent, terminal pane, tmux pane, iterm pane, monitor teammate, agent pane, bash task pane
  related-skills: java-feature-development, react-feature-development, node-feature-development
---

# Terminal Monitor — Utility Skill

Opens a dedicated terminal pane (tmux or iTerm2) to let the user follow a
background Agent-tool teammate, or a plain Bash background task, in real
time.

**Two genuinely different mechanisms, two modes:**

- **`mode: agent`** — for teammates spawned via the `Agent` tool with a
  `name`. These do **not** write to any known output file and are **not**
  tracked under any `.team/<name>/` directory — they communicate
  exclusively through the native mailbox protocol, delivered to the
  orchestrator as `<teammate-message>` blocks and `idle_notification`
  events. The pane is driven by **pushing** those events into it (via
  `tmux send-keys` / iTerm2 `write text`) as they arrive — never by reading
  a file.
- **`mode: bash-task`** — for a plain `Bash(run_in_background: true)`
  command. This genuinely writes to a real `output_file`; there is no
  native message channel for it, so tailing that file is the correct (and
  only) approach here.

Do not try to use `mode: agent` for a raw Bash background task, or
`mode: bash-task` for an `Agent`-spawned teammate — neither will find
anything to read/push.

---

## Parameters (passed by the calling skill via context)

| Parameter | Required | Description |
|-----------|----------|-------------|
| `mode` | yes | `agent` or `bash-task` |
| `label` | yes | Header text displayed in the pane |
| `pane-name` | yes | Short name for the tab/window |
| `agent-name` | if `mode: agent` | The exact `name` passed to `Agent(name: ...)` when spawning the teammate |
| `output-file` | if `mode: bash-task` | The `output_file` path returned by the Bash tool when the command was launched with `run_in_background: true` |

---

## Protocol

Execute the steps below every time this skill is called.

### Step 1 — Detect terminal type (once per session)

If the terminal type has NOT been detected yet in this session, run:

```bash
if [ -n "$TMUX" ]; then
  echo "tmux"
elif [ -n "$ITERM_SESSION_ID" ] || [ "$TERM_PROGRAM" = "iTerm.app" ]; then
  echo "iterm2"
else
  echo "none"
fi
```

Store the result as `TERMINAL_TYPE`. On subsequent calls reuse the stored
value — do NOT re-detect.

If `TERMINAL_TYPE` is `none`, print **once** (not on every call):

```
Terminal multiplexer not detected (no tmux session, ITERM_SESSION_ID not set).
Agents will run without dedicated panes.
To enable live monitoring: run Claude inside a tmux session or use iTerm2.
```

Then return immediately — skip the remaining steps for this call.

---

### Step 2 — Open the pane

**`mode: bash-task`** — tail the real output file as soon as it appears
(unchanged from before — this is a legitimate file-tailing case):

```bash
echo '=== <label> ==='; \
until [ -f <output-file> ]; do sleep 1; done; \
tail -f <output-file>
```

Open it — **tmux**:

```bash
tmux has-session -t agent-monitor 2>/dev/null || \
  tmux new-session -d -s agent-monitor -n "orchestrator"
tmux new-window -t agent-monitor -n "<pane-name>" "MONITORING_CMD; exec bash"
```

**iTerm2** (AppleScript):

```applescript
tell application "iTerm2"
  tell current window
    create tab with default profile
    tell current session
      set name to "<pane-name>"
      write text "MONITORING_CMD"
    end tell
  end tell
end tell
```

**`mode: agent`** — no monitoring command; just open a plain, idle shell
ready to receive pushed keystrokes. Nothing is tailed.

**tmux:**

```bash
tmux has-session -t agent-monitor 2>/dev/null || \
  tmux new-session -d -s agent-monitor -n "orchestrator"
tmux new-window -t agent-monitor -n "<pane-name>" \
  "echo '=== <label> ==='; exec ${SHELL:-bash}"
```

**iTerm2** (AppleScript):

```applescript
tell application "iTerm2"
  tell current window
    create tab with default profile
    tell current session
      set name to "<pane-name>"
      write text "echo '=== <label> ==='"
    end tell
  end tell
end tell
```

**Remember the mapping `<agent-name> → <pane target>`** (tmux:
`agent-monitor:<pane-name>`; iTerm2: the named session) for the rest of the
conversation — this is orchestrator bookkeeping, kept in context, not
written to any file.

---

### Step 3 — Relay events (only for `mode: agent`)

For every `<teammate-message teammate_id="<agent-name>">` or
`{"type":"idle_notification","from":"<agent-name>"}` the orchestrator
receives for a monitored agent, push a short formatted line into that
agent's pane **immediately**, before continuing the turn. Do this for the
entire lifetime of the monitored agent — not just once at spawn time.

To avoid any quoting/escaping issues (quotes, newlines, accented
characters), round-trip the line through base64 rather than embedding it
raw in the pushed command:

```bash
B64=$(printf '%s' "<formatted line, e.g. '[agent-name] <summary or message excerpt>'>" | base64 | tr -d '\n')
```

**tmux** — push it:

```bash
tmux send-keys -t agent-monitor:<pane-name> "echo $B64 | base64 -d" Enter
```

**iTerm2** — push it via AppleScript, targeting the session by name:

```applescript
tell application "iTerm2"
  tell current window
    tell (first session whose name is "<pane-name>")
      write text "echo <B64> | base64 -d"
    end tell
  end tell
end tell
```

This is what makes the pane live — its content is 100% driven by the
native events the orchestrator already receives, never by polling or
reading a file.

---

### Step 4 — Closing line (only for `mode: agent`)

When the monitored agent finishes (final idle notification, explicit
stop, or task completion), push one last line:

```bash
B64=$(printf '%s' "=== <label> finalizado ===" | base64 | tr -d '\n')
tmux send-keys -t agent-monitor:<pane-name> "echo $B64 | base64 -d" Enter
```

Do **not** close the pane automatically — leave it open so the user can
scroll back through the history.

---

### Step 5 — Return to caller

After opening the pane (Step 2), return control to the calling skill
immediately — it proceeds to launch the agent/task without waiting. The
calling skill (or the orchestrator directly) is then responsible for
performing Step 3 on every subsequent event for that agent, and Step 4 on
completion.
