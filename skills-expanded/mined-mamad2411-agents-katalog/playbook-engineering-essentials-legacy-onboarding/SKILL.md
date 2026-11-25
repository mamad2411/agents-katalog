---
name: playbook-engineering-essentials-legacy-onboarding
description: "Mental model built through safe probes, tests, and first merged fix within two weeks."
---
# Playbook: Onboard onto a legacy codebase fast

> Mental model built through safe probes, tests, and first merged fix within two weeks.

**Track:** 🗺️ Engineering Essentials · **Domain:** Journey Playbooks · **Level:** journey · **~90 min**

**Who this is for:** All Software Engineers

## When to Use This Skill

Mental model built through safe probes, tests, and first merged fix within two weeks.
Use it whenever a matching task appears in conversation — the agent loads these instructions on demand.

## Journey Steps

1. Step 1 — Hunt bugs systematically (Node.js): start with "Reproduce deterministically first; flaky repro = flaky fix"
2. Step 2 — Refactor without breaking behavior (Python): start with "Pin current behavior with characterization tests where gaps exist"
3. Step 3 — Practice git discipline teams thank you for (Go): start with "Atomic commits: one logical change, imperative message with why"
4. How it fits together: Pick any stack variant matching the codebase. Characterization tests are your map.

### Referenced Skills

- `debug-craft-systematic-bug-hunt-node`
- `code-quality-refactor-safely-python`
- `collab-workflow-git-discipline-go`

## Commands

**Install all referenced skills**
```bash
npx skills add aniruddhaadak80/skills --skill debug-craft-systematic-bug-hunt-node && npx skills add aniruddhaadak80/skills --skill code-quality-refactor-safely-python && npx skills add aniruddhaadak80/skills --skill collab-workflow-git-discipline-go
```

---

Part of [aniruddhaadak80/skills](https://github.com/aniruddhaadak80/skills) · Browse all at https://skills.sh/aniruddhaadak80/skills