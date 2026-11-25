---
name: systematic-debugging
description: Structured diagnosis of bugs, errors, and stuck processes. Maps symptoms to hypotheses, uses bounded log reading, and produces actionable reports. Use when debugging errors, investigating stuck processes, diagnosing performance issues, or when something isn't working as expected.
user-invocable: true
disable-model-invocation: true
---

# Systematic Debugging

CRITICAL: This is a diagnostic skill. Investigate first, fix second. Don't guess — gather evidence.

## Diagnostic Mindset

- Don't report when healthy. If everything looks fine, say so directly — don't manufacture issues.
- Don't kill or signal processes unless explicitly asked. This is diagnostic only.
- Read errors before guessing causes. The error message is the first evidence.
- Reproduce before fixing. A fix you can't verify is a guess.

## Symptom-to-Hypothesis Map

Start here. Match the symptom to candidate hypotheses, then investigate:

| Symptom | Likely Hypotheses | First Investigation |
|---|---|---|
| High CPU (≥90% sustained) | Infinite loop, runaway regex, tight polling | Sample twice 1-2s apart to confirm sustained; check stack/profile |
| Process in D state (uninterruptible sleep) | I/O hang, disk full, NFS stall, lock contention | Check `dmesg`, disk usage, mount status |
| Process in T state (stopped) | Accidental Ctrl+Z, debugger attached | Check parent process, `fg` to resume |
| Zombie process (Z state) | Parent not reaping children | Check parent PID, signal parent |
| High memory (≥4GB RSS) | Memory leak, unbounded cache, large dataset loaded | Check growth over time, heap snapshot if available |
| Slow response | N+1 queries, blocking I/O on hot path, missing index | Profile request, check DB query count and timing |
| Hung child process | Waiting for stdin, deadlock, network timeout | `pgrep -lP <pid>`, check child's full command line |
| Intermittent failure | Race condition, resource exhaustion, DNS flake | Check timing patterns, add logging, reproduce under load |
| Build failure | Dependency version mismatch, stale cache, missing env var | Clean build, check lock file, diff with working state |
| Test failure (flaky) | Shared state, timing dependency, order dependency | Run test in isolation, check setup/teardown, look for shared mutable state |

## Investigation Steps

### 1. Gather Context
- Read the error message / stack trace carefully. Most errors tell you exactly what's wrong.
- Check recent changes: `git log --oneline -10` and `git diff` — was something just changed?
- Read relevant log files. Use **bounded reading**: tail the last 50-100 lines, don't read the entire log.

### 2. Enable Logging If Needed
If the issue isn't visible in current logs:
- Enable debug/verbose logging for the affected component
- Ask the user to reproduce the issue
- Re-read the log after reproduction

### 3. Form and Test Hypotheses
- Based on symptoms and gathered evidence, form 1-3 hypotheses ranked by likelihood.
- For each hypothesis, identify one specific check that would confirm or eliminate it.
- Run the most discriminating check first.
- If the first hypothesis is disproven, move to the next — don't cling to your initial guess.

### 4. Narrow Down
- Use Grep with `-C 5` context to search for error patterns in logs and code without reading entire files.
- Use `head_limit` on Grep to avoid drowning in results.
- Only Read full files after Grep confirms they're relevant. Glob (near-zero tokens) → Grep (lightweight) → Read (heavy).
- When debugging spans >5 files, spawn a subagent via the Agent tool for isolated investigation.

### 5. Fix and Verify
- Make the minimal fix that addresses the root cause, not the symptom.
- Verify the fix by reproducing the original failure scenario — it should now succeed.
- Check for regressions in related functionality.
- If you can't verify (no repro, no test), say so explicitly.

## Bounded Log Reading

Logs can be enormous. Never read an entire log file.

- **Tail first**: Read the last 50-100 lines to find recent errors.
- **Grep for severity**: Search for `[ERROR]`, `[WARN]`, `FATAL`, `panic`, `Exception`, `traceback` across the full file.
- **Use offset/limit**: When you find a relevant line number, read just that region with surrounding context.
- **Check file size first**: If a log is >1MB, definitely use targeted reads, not full file reads.

## Bug Report Format

When reporting findings, use this two-part structure:

### Short Summary (1-2 sentences)
What's wrong, which component, and the severity. This is what the reader sees first.

```
Example: "Auth service returning 500 on /login — null pointer at session.validate()
when session cookie is expired but token is still cached."
```

### Detailed Thread
- **Symptom**: What was observed (exact error messages, status codes, behavior)
- **Root cause**: What's actually wrong and why (with evidence — file paths, line numbers, log excerpts)
- **Evidence**: Commands run and their output (copy-paste, not paraphrased)
- **Fix**: What was changed or what should be changed (specific files and lines)
- **Verification**: How the fix was verified, or why it couldn't be verified

## Process Diagnostics

When investigating stuck or slow processes:

```bash
# List processes with CPU, memory, state, and uptime
ps -axo pid=,pcpu=,rss=,etime=,state=,comm=,command= | grep -E '<process_name>'

# Check child processes
pgrep -lP <pid>

# Sample CPU usage (confirm sustained, not transient)
# Check twice with 1-2s gap
```

- Filter to relevant processes. Don't dump the entire process table.
- Sample CPU twice to confirm sustained high usage (transient spikes are normal).
- For hung children, get the full command line: `ps -p <child_pid> -o command=`

CRITICAL REMINDER: Investigate before fixing. Bound your log reads. Report only real issues — don't manufacture problems from healthy systems. Reproduce, then fix, then verify.

## Related Skills

- Use `codebase-exploration` patterns to trace code paths during investigation.
- Use `effective-tool-use` patterns when running diagnostic commands safely.
- After fixing, apply `code-verification` patterns to prove the fix works.

## Project Customization

If `user-config.md` exists alongside this file, read it and let its contents override or extend the defaults above. Common customizations:
- Project-specific log locations and formats
- Common failure modes for this system
- Diagnostic commands specific to the tech stack
- Escalation procedures for production issues
