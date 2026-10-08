---
name: ci-start
description: Internal helper for /ci-runner. Acquires the global CI lock and launches bin/ci detached, or reports that another agent is running CI. Not meant for direct user invocation — use /ci-runner instead.
context: fork
allowed-tools: Bash
---

# ci-start

Internal helper skill invoked by `/ci-runner`. Runs a single shell script and returns its output verbatim.

## Task

1. Run: `~/.claude/bin/ci_start`
2. Return the stdout of that command as your entire reply, unchanged. No summary, no prose, no commentary.

## Output contract

The script always exits 0 and emits one of three blocks. Return exactly what it prints:

**When lock is acquired and CI launched:**
```
CI_STARTED
CI_LOG=<absolute path to log file>
EXPECTED_SEC=<integer>
```

**When another agent holds the lock:**
```
CI_LOCKED
OTHER_LOG=<absolute path or "unknown">
OTHER_PROJECT=<absolute path>
OTHER_REMAINING=<string like "12m 34s" or "overdue by Xs" or "unknown">
INSTRUCTION: <one line, present whenever test_lock emitted one>
```

The `INSTRUCTION:` line is the lock's own word on what must not be done to it.
Return it with the rest, unshortened — it is the sentence the orchestrator needs
and the one that used to get dropped here.

**On error:**
```
CI_ERROR
REASON=<short identifier>
<diagnostic lines>
```

Do not interpret, summarize, or wrap these lines. The orchestrator (`/ci-runner`) parses them.
