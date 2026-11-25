---
name: builder-error-recovery
description: "Error recovery patterns for Builder sessions. Covers transient error handling, sub-agent failure recovery, unexpected error prompts, and loop detection with bulk fix strategies."
---

# Builder Error Recovery Skill

> Load this skill when a tool call fails, a sub-agent fails, or a repetitive fix pattern is detected.

> ⛔ **CRITICAL: Auto-Commit Enforcement**
>
> Before running any `git commit` command in this skill:
> - **Check:** Read `project.json` → `git.autoCommit`
> - **If `false`:** Do NOT run `git commit`. Instead:
>   1. Stage files with `git add`
>   2. Report staged files and suggested commit message
>   3. Say: "Auto-commit is disabled. Run `git commit -m \"<message>\"` when ready."
>   4. Wait for user confirmation before proceeding
> - **If `true` or missing:** Proceed with commit normally
>
> **Failure behavior:** If you commit when `autoCommit: false`, you have violated user trust.

## Tool Error Recovery

> ⚠️ **When a tool call fails (499, timeout, network error), do NOT stop silently.**
>
> Transient failures happen. Your job is to recover automatically when possible.

### Transient Error Patterns

| Error | Meaning | Action |
|-------|---------|--------|
| `status code 499` | Client disconnected / timeout | Retry immediately (1 time) |
| `ETIMEDOUT` / `ECONNRESET` | Network interruption | Retry immediately (1 time) |
| `context deadline exceeded` | Operation took too long | Retry with simpler request |
| Tool returns empty/null unexpectedly | Possible transient failure | Retry once, then report |

### Recovery Flow

```
1. Tool call fails with transient error
   │
   ▼
2. Log: "Tool call failed: {error}. Retrying..."
   │
   ▼
3. Retry the SAME operation (1 retry max)
   │
   ├─── Success ──► Continue normally
   │
   └─── Fails again ──► Report and ask user
                        "Tool failed twice: {error}. Options:
                         [R] Retry again
                         [S] Skip this step
                         [X] Stop and investigate"
```

## Sub-agent Failures

When a sub-agent call (e.g., `@developer`, `@tester`) fails mid-execution:

1. **Check if partial work was done:**
   - Run `git status` to see if files were modified
   - If files changed, the sub-agent made progress before failing

2. **Resume strategy:**
    - If no changes: Retry the full sub-agent call
    - If partial changes: Pass context about what was already done
   
   ```
   <context>
   version: 1
   resuming: true
   previousAttempt:
     status: failed
     error: "499 timeout"
     partialChanges:
       - file: src/components/Button.tsx
         status: modified
   </context>
   
   Continue from where you left off. The previous attempt failed with a 499 timeout.
   Check git status to see what was already changed, then complete the remaining work.
   ```

3. **After 2 sub-agent failures:** Stop and report to user with options

## Never Stop Silently

If you encounter an error and don't know how to proceed:

```
⚠️ UNEXPECTED ERROR

I encountered an error I don't know how to handle:
  Error: {error details}
  Context: {what I was trying to do}

Options:
  [R] Retry the operation
  [I] Investigate (show me what to check)
  [X] Stop workflow
```

**Do NOT:** Just stop responding and wait for the user to notice.

## Loop Detection and Bulk Fix

> **Load `self-correction` skill when detecting repetitive fix patterns.**

After fixing the same issue type 3+ times, load the skill for:
- Detection triggers (same test failure, lint error, type error)
- Self-check protocol
- Bulk fix strategy selection
- User reporting format
