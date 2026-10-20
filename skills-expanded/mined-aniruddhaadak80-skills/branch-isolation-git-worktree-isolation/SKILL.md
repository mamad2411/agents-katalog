---
name: branch-isolation-git-worktree-isolation
description: "Separate directories per branch letting agents work concurrently without stepping on each other."
---
# Isolate parallel work with git worktrees

> Separate directories per branch letting agents work concurrently without stepping on each other.

**Track:** 🔄 Agentic Methodology · **Domain:** Branch Isolation · **Level:** intermediate · **~25 min**

**Who this is for:** Agent Power Users, AI-Native Engineers, Teams Shipping With Agents, Solo Builders

## When to Use This Skill

Separate directories per branch letting agents work concurrently without stepping on each other.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Create worktrees per workstream: git worktree add ../feat-x -b feat-x
2. Install dependencies inside EACH worktree; they do not share node_modules
3. Assign one agent per worktree; forbid cross-worktree checkouts mid-run
4. Name worktree dirs after branches; delete immediately after merge
5. Prune stale worktrees monthly: git worktree prune plus manual sweep
6. Never create a worktree INSIDE another repository's working tree

## Common Pitfalls

- Assuming installed deps carry across worktrees
- Two agents editing the same file via different worktrees then merging blindly

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill branch-isolation-git-worktree-isolation
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill branch-isolation-git-worktree-isolation -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills