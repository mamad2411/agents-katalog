---
name: collab-workflow-git-discipline-go
description: "Commit hygiene, branch strategy, and recovery skills preventing shared-repo disasters."
---
# Practice git discipline teams thank you for (Go)

> Commit hygiene, branch strategy, and recovery skills preventing shared-repo disasters.

**Track:** 🧰 Engineering Essentials · **Domain:** Collaboration Workflow · **Level:** foundation · **~25 min**

**Who this is for:** All Software Engineers

## When to Use This Skill

Commit hygiene, branch strategy, and recovery skills preventing shared-repo disasters.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Steps

1. Atomic commits: one logical change, imperative message with why
2. Branch names carry ticket refs: feat/123-short-slug
3. Rebase local before PR; merge only via repo's chosen strategy
4. Master interactive rebase, reflog rescue, and bisect fluently
5. Never rewrite shared branches; force-push with lease only when agreed
6. Tag releases and keep changelog in sync mechanically
7. Run pprof profiles; check goroutine leaks with goleak
8. Enforce vet/lint gates; keep error wrapping with %w intact

## Common Pitfalls

- git push --force default aliasing over teammates
- Thousand-line 'WIP' commits nobody can review

## Commands

**Install with skills CLI**
```bash
npx skills add aniruddhaadak80/skills --skill collab-workflow-git-discipline-go
```

**Install globally**
```bash
npx skills add aniruddhaadak80/skills --skill collab-workflow-git-discipline-go -g
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills