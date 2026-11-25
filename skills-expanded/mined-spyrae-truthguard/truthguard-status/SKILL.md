---
name: truthguard-status
description: Show TruthGuard session statistics
allowed-tools: Bash
---

Show the current TruthGuard session status by reading the session log.

## Steps

1. Read the session log file at `~/.truthguard/session.log`. If it doesn't exist, report "No events recorded this session."

2. Count events by type:
```bash
LOG="~/.truthguard/session.log"
if [ -f "$LOG" ]; then
  BLOCKED=$(grep -c "blocked" "$LOG" 2>/dev/null || echo 0)
  FILE_ALERTS=$(grep -c "phantom-edit" "$LOG" 2>/dev/null || echo 0)
  EXIT_WARNINGS=$(grep -c "exit-code" "$LOG" 2>/dev/null || echo 0)
  BUILD_FAILURES=$(grep -c "build-fail" "$LOG" 2>/dev/null || echo 0)
  TEST_FAILURES=$(grep -c "test-fail" "$LOG" 2>/dev/null || echo 0)
  COMMITS_BLOCKED=$(grep -c "commit-blocked" "$LOG" 2>/dev/null || echo 0)
  VERIFICATIONS=$(grep -c "verify" "$LOG" 2>/dev/null || echo 0)
  TOTAL=$(wc -l < "$LOG" | tr -d ' ')
  echo "Log has $TOTAL entries"
else
  echo "No session log found"
fi
```

3. Check if hooks are active by looking at the project's `.claude/settings.json` or user settings for TruthGuard hook entries.

4. Report in this format:

```
🛡️ TruthGuard Status
━━━━━━━━━━━━━━━━━━━━━━━
Hooks: ✅ PreToolUse (Bash, Write/Edit) | PostToolUse (Bash, Write/Edit)

Session Events:
  🛑 Commands blocked:    X
  ⚠️ Exit code warnings:  Y
  📝 Phantom edit alerts:  Z
  🔨 Build failures:       A
  🧪 Test failures:        B
  🚫 Commits blocked:      C
  ✅ Verifications run:    D
  ━━━━━━━━━━━━━━━━━━━━━━━
  Total events:            N
```

5. If no events, show a clean status:
```
🛡️ TruthGuard Status
━━━━━━━━━━━━━━━━━━━━━━━
Hooks: ✅ Active
Session: Clean — no warnings or blocks this session.
```
