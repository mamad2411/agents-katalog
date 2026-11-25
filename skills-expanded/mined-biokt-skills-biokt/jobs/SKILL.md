---
name: jobs
description: Track running and completed simulation jobs in a project's JOBS.md across all machines. Use when checking which jobs are running, recording a newly submitted job, querying SLURM status, or archiving finished runs.
argument-hint: "[add|update|clean]"
allowed-tools: Read, Write, Edit, Glob, Bash
---

# /jobs — Track Jobs in JOBS.md

Create and maintain a JOBS.md file for the current project, tracking
active and completed simulation jobs across all machines.

## Trigger
- `/jobs` — show current JOBS.md (create if absent)
- `/jobs add` — append one or more new job rows (interactive)
- `/jobs update` — check live status of all active jobs and tidy up
- `/jobs clean` — move all struck-through rows to a Completed archive section

---

## File format

Location: `JOBS.md` in the current project root.

Header block (written once on creation; update `Last updated` on every write):
```
# Jobs — <ProjectName>
Last updated: YYYY-MM-DD
```

Table columns:

| Job | Machine | ID | Type | Started | Status | Notes |
|-----|---------|----|----|---------|--------|-------|

- **Job**: short description of what is running
- **Machine**: host name (rubisco, villin, insulin, calmodulin, agamede, hyperion)
- **ID**: PID nnnnnn or SLURM nnnnnn
- **Type**: `background process` / `array job` / `single job`
- **Started**: date as YYYY-MM-DD
- **Status**: `running` / `pending` / `complete` / `failed` / `killed` / `cancelled`
- **Notes**: key parameters, caveats, outcomes

Finished jobs are struck through with `~~` on every field in their row.

---

## Mode: (no argument)

Read and display the current JOBS.md. If the file does not exist, create
it with the header and an empty table, then confirm to the user.

---

## Mode: add

Ask the user for each required field, or infer from conversation context
if a job was just submitted in this session.

Required: Job, Machine, ID, Type
Defaults: Started = today (YYYY-MM-DD), Status = running

Append the new row to the active table. Update `Last updated`.
If JOBS.md does not exist, create it first.

---

## Mode: update

For every non-struck-through row, check live status via SSH:

| ID type | Check command |
|---------|---------------|
| PID on any host | `ssh <host> 'kill -0 <pid> 2>/dev/null && echo running || echo gone'` |
| SLURM on any host | `ssh <host> 'squeue -j <id> -h 2>/dev/null \| awk "{print \$5}"'` |

SLURM state codes → Status mapping:
- `R` → running
- `PD` → pending
- `CG` → running (completing)
- empty / not found → check final state with `ssh <host> 'sacct -j <id> --format=State -n --noheader 2>/dev/null'`
  - `COMPLETED` → complete
  - `FAILED` → failed
  - `CANCELLED*` → cancelled
  - `TIMEOUT` → failed
  - unresolvable → ask before striking through

After checking all rows:
- Update the Status field for jobs still running or pending
- Strike through rows for jobs that have finished (any terminal state)
- Update `Last updated` in the header
- Print a brief summary: X running, Y pending, Z newly finished, W failed

---

## Mode: clean

Move all struck-through rows out of the active table and into a
`## Completed` section at the bottom of the file. Preserve the rows
verbatim (strikethrough intact). Update `Last updated`.

If a `## Completed` section already exists, append to it rather than
creating a new one.

After cleaning, confirm how many rows were archived and how many active
rows remain.

---

## Rules
- Never delete rows — only strike through or archive to Completed
- Infer project name from the current working directory name
- Ask before striking through if a job's disappearance is ambiguous
  (PID gone but no SLURM record — could be a host reboot or crash)
- agamede and hyperion: SLURM only — never attempt direct PID checks
- Keep SSH commands properly quoted: `ssh host 'cmd1 && cmd2'`
