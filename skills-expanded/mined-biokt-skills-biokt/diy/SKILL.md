---
name: diy
description: Execute the action most recently proposed in the conversation instead of describing it again. Use when the user says "do it", "go ahead", "just do it", or types /diy after Claude has offered a command, script, or set of steps but not run them.
argument-hint: "[action or hint]"
---

# /diy — Do It Yourself (Execute Pending Actions)

Stop offering, start doing. Find what was most recently proposed in this
conversation and execute it.

## Trigger
User typed `/diy` with optional context: `/diy [action or hint]`

## Steps

1. **Identify the target**
   - No argument: scan the most recent assistant turn for proposed
     commands, scripts, or workflow steps
   - With argument: use it to narrow down if multiple action sets exist
   - Still ambiguous: ask ONE question, then proceed

2. **Announce in one sentence** — "Running X now." — then execute.

3. **Execute using the right tool:**

   | Action | How |
   |--------|-----|
   | Local command (same host as Claude) | `Bash` tool |
   | File operation | `Read` / `Edit` / `Write` tools |
   | Command on another host | `Bash: ssh <host> '<cmd>'` |
   | Jupyter notebook | `Bash: jupyter nbconvert --to notebook --execute --inplace <nb>` |
   | Data transfer | `Bash: rsync -avz <src> <dst>` or `scp` |
   | SLURM submission | `Bash: ssh <host> 'cd <dir> && sbatch <script>'` |
   | Python script | `Bash: python <script>` (local or via SSH) |

4. **On failure:** diagnose, fix, retry. Never stop at the first error.
   Report what changed and why before retrying.

5. **Report:** one sentence per action — what ran, exit code if nonzero,
   key output worth surfacing.

## Host notes
- Claude Code is installed on: local Mac, rubisco, villin, insulin, calmodulin
- agamede and hyperion are accessible via SSH but have no Claude — submit
  jobs there with `sbatch` only, never run interactively

## Rules
- Never skip silently — if something can't execute, say why.
- Use non-interactive flags (`-y`, `--yes`, `--no-input`) to avoid hangs.
- Ask before destructive operations (delete, overwrite, force-push).
- agamede / hyperion: `sbatch` only, no interactive execution.
- Quote SSH commands correctly: `ssh host 'cmd1 && cmd2'`
