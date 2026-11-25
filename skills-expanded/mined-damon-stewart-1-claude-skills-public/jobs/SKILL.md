---
name: jobs
description: Check status of dispatched background Claude tasks. Use when the user says "jobs", "check jobs", "job status", "what's running", or "/jobs".
user_invocable: true
---

# Jobs: Check Background Task Status

The user wants to see the status of dispatched background Claude tasks.

## What to do

1. **List all job metadata files:**

```bash
ls -t ~/.claude/jobs/*.meta 2>/dev/null
```

If no files exist, tell the user "No dispatched jobs found. Use `/dispatch` to send a task to background."

2. **For each job, read the `.meta` file** and display a summary table:

| Job ID | Status | Task | Started | Exit Code |
|--------|--------|------|---------|-----------|

   Status indicators and display treatment:
   - `complete` (green)
   - `running` (blue)
   - `failed` (red): non-zero exit, not a timeout
   - `timed_out` (orange): exit code 124, gtimeout killed it; was actively running, not crashed. Offer to re-dispatch with a higher TIMEOUT_SECS.
   - `stale` (yellow): process died silently without updating meta; see step 5

   The `exit_code` field may be absent in older meta files; show blank if missing.

3. **For completed jobs**, check if the output file exists and offer to read it:
   - "Job X is complete. Want me to read the output?"

4. **For failed or timed_out jobs**, automatically show the last 20 lines of the `.log` file:

```bash
tail -20 ~/.claude/jobs/<JOB_ID>.log
```

   Include the exit_code from the meta file in the summary. If a failed job has an output file (partial results from fallback extraction), mention it.

5. **For running jobs**, check if the process is still alive:

```bash
# Check if any claude process is running for this job's log file
ps aux | grep -l "claude" | head -5
```

If the process died but status still says "running", update the meta file to "failed" and check the log file for errors.

6. **If the user asks about a specific job**, read both the `.meta` and `.log` files. The log contains the full JSON output from Claude, including session ID. If the user wants to continue a job's conversation:

```bash
unset CLAUDECODE && claude -p "Continue where you left off" --resume <session_id>
```

## Cleanup

If the user says "clean jobs" or "clear jobs", offer to remove completed and failed job files:

```bash
# Remove .meta, .log, and .md files for completed and failed jobs
grep -l "status: \(complete\|failed\)" ~/.claude/jobs/*.meta | while read f; do
  base="${f%.meta}"
  rm -f "$f" "${base}.log" "${base}.md"
done
```

Always confirm before deleting.
