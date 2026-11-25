---
name: branch
description: >-
  Fork an in-flight research-agent run at its current checkpoint into a named
  branch with its own state, log, attempts, and git worktree, sharing the
  parent's goal and findings read-only. Use to pursue a competing strategy
  without disturbing the main line; a main-line synthesis compares branches.
argument-hint: "<branch-name> [focus] [budget: N cycles, H hours]"
---

# Branch a Research Run

Fork the run per: $ARGUMENTS

## Step 1: Parse Arguments

1. **Branch name** (required): kebab-case identifier, e.g. `induction-proof`, `adversarial-search`. Derive one from the stated strategy if the user did not name it, and confirm it.
2. **Branch focus** (optional): one or two sentences on what this branch should pursue differently from the main line.
3. **Budget** (optional): a cycle cap and/or hours for this branch.

## Step 2: Verify the Run and the Name

- `.research/goal.md` must exist (Read tool); if not, there is nothing to branch: suggest `/research-agent:research`.
- `.research/branches/<name>/` must NOT already exist (Glob tool). If it does, offer `/research-agent:resume <name>` or a different name.

## Step 3: Check Code Isolation

A branch edits and evaluates project code in its own git worktree so it cannot disturb the main line's eval.

- Bash: `git -C <working directory> rev-parse --is-inside-work-tree`. If this is not a git repo, worktree isolation is unavailable: tell the user the branch will keep all code changes inside its own attempts/ directories, and launch without `isolation`.
- If it is a git repo, check `git status --porcelain`. The worktree starts from HEAD, so uncommitted changes (including main-line work in progress) will not be in it. If the output is non-empty, tell the user and ask whether to proceed or commit first (AskUserQuestion).

## Step 4: Launch the Researcher in Branch Mode

Spawn the researcher (Agent tool, `subagent_type: research-agent:researcher`, and `isolation: "worktree"` when Step 3 found a git repo) with:

    <mode>branch</mode>
    <branch>{kebab-case name}</branch>
    <branch-focus>
    {the focus, or "explore an alternative approach to the goal"}
    </branch-focus>
    <budget max_cycles="{N}" max_hours="{H}"/>    (only when given)
    <working_directory>
    {absolute path to current working directory, NOT the worktree}
    </working_directory>

## Step 5: Inform the User

> Branch `{name}` forked from the current checkpoint. Its state lives under `.research/branches/{name}/`; its code changes live in its own git worktree, committed once per cycle. The goal and the parent's confirmed findings are shared read-only.
>
> - `/research-agent:status` shows all branches alongside the main line
> - `/research-agent:resume {name}` continues this branch later (in the same worktree)
> - `/research-agent:synthesize {name}` concludes just this branch; a main-line `/research-agent:synthesize` compares all branches
