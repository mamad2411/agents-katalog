---
name: daemon-start
description: Start the asciinema chunker daemon. TRIGGERS - start daemon, resume chunker, enable backup.
allowed-tools: Bash
argument-hint: ""
model: haiku
disable-model-invocation: false
---

# /asciinema-tools:daemon-start

Start the asciinema chunker daemon via launchd.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Execution

### Check if Already Running

```bash
/usr/bin/env bash << 'CHECK_EOF'
PLIST_PATH="$HOME/Library/LaunchAgents/com.cc-skills.asciinema-chunker.plist"

if ! [[ -f "$PLIST_PATH" ]]; then
  echo "ERROR: Daemon not installed. Run /asciinema-tools:daemon-setup first."
  exit 1
fi

if launchctl list 2>/dev/null | grep -q "asciinema-chunker"; then
  echo "ALREADY_RUNNING"
  cat ~/.asciinema/health.json 2>/dev/null | jq -r '"Status: \(.status) | PID: \(.pid) | Last push: \(.last_push)"' || true
  exit 0
fi

echo "NOT_RUNNING"
CHECK_EOF
```

### Start Daemon

```bash
/usr/bin/env bash << 'START_EOF'
PLIST_PATH="$HOME/Library/LaunchAgents/com.cc-skills.asciinema-chunker.plist"

if launchctl load "$PLIST_PATH"; then
  echo "Daemon started"
  sleep 2

  if launchctl list 2>/dev/null | grep -q "asciinema-chunker"; then
    echo ""
    echo "Status:"
    cat ~/.asciinema/health.json 2>/dev/null | jq . || echo "Waiting for health file..."
  else
    echo "WARNING: Daemon may not have started correctly. Check logs:"
    echo "  /asciinema-tools:daemon-logs"
  fi
else
  echo "ERROR: Failed to start daemon"
  exit 1
fi
START_EOF
```

## Output

On success:

```
Daemon started

Status:
{
  "status": "ok",
  "message": "Monitoring ~/.asciinema/active",
  "pid": 12345,
  ...
}
```

## Troubleshooting

| Issue                  | Cause                       | Solution                                  |
| ---------------------- | --------------------------- | ----------------------------------------- |
| Daemon not installed   | Setup not run               | Run `/asciinema-tools:daemon-setup` first |
| Failed to start daemon | Launchd configuration error | Check `launchctl error` and re-run setup  |
| Health file missing    | Daemon still initializing   | Wait 5 seconds, check `/daemon-status`    |
| Daemon keeps stopping  | Script error or credentials | Check `/asciinema-tools:daemon-logs`      |


## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
