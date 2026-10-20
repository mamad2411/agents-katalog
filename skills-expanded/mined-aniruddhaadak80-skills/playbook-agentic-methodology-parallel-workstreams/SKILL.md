---
name: playbook-agentic-methodology-parallel-workstreams
description: "Worktree isolation plus dispatch discipline letting multiple agents ship concurrently without collisions."
---
# Playbook: Run parallel agent workstreams safely

> Worktree isolation plus dispatch discipline letting multiple agents ship concurrently without collisions.

**Track:** 🗺️ Agentic Methodology · **Domain:** Journey Playbooks · **Level:** journey · **~85 min**

**Who this is for:** Agent Power Users, AI-Native Engineers, Teams Shipping With Agents, Solo Builders

## When to Use This Skill

Worktree isolation plus dispatch discipline letting multiple agents ship concurrently without collisions.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Isolate parallel work with git worktrees: start with "Create worktrees per workstream: git worktree add ../feat-x -b feat-x"
2. Step 2 — Dispatch subagents with fresh-context discipline: start with "Extract each task's brief to its own file; the brief is the ONLY requirements source"
3. Step 3 — Receive agent code review without ego or obedience: start with "Reproduce or locate every claim before acting; reviewers are fallible too"
4. How it fits together: One agent per worktree, one brief per task. Cross-tree edits are how weekends die.

### Referenced Skills

- `branch-isolation-git-worktree-isolation`
- `execution-discipline-subagent-dispatch-discipline`
- `branch-isolation-receiving-code-review-gracefully`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill branch-isolation-git-worktree-isolation && npx skills add aniruddhaadak80/skills --skill execution-discipline-subagent-dispatch-discipline && npx skills add aniruddhaadak80/skills --skill branch-isolation-receiving-code-review-gracefully
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills