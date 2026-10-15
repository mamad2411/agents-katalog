---
name: git-pre-read-diagnostics
description: Run 5 git commands before reading any code to diagnose a new codebase — code churn hotspots, bus factor, bug clusters, project velocity, and firefighting frequency. Use when onboarding to a new project, starting a codebase audit, or deciding where to focus refactoring/analysis efforts.
license: MIT
---

# Git Pre-Read Diagnostics

Five git log commands that diagnose a codebase before you open a single file. Derived from [Ally Piechowski's article](https://piechowski.io/post/git-commands-before-reading-code/).

Run these from `app/` or `src/` (not repo root) to avoid lockfiles and generated code dominating results.

## 1. Code Churn Hotspots

```bash
git log --format=format: --name-only --since="1 year ago" | sort | uniq -c | sort -nr | head -20
```

The 20 most-changed files. The top file is usually the one everyone warns about. High churn on an unowned file is a patch-on-patch signal — the blast radius of a small edit is unpredictable.

**Cross-reference with step 3:** a file that is high-churn *and* high-bug is your single biggest risk.

## 2. Bus Factor & Contributor Map

```bash
git shortlog -sn --no-merges
```

All contributors ranked by commit count. If one person accounts for ≥60%, that's your bus factor. If they left 6 months ago, it's a crisis.

Also check recent activity separately:

```bash
git shortlog -sn --no-merges --since="6 months ago"
```

If the top overall contributor doesn't appear in this window, flag it. If there are 30 total contributors but only 3 active in the last year, the builders are not the maintainers.

**Caveat:** squash-merge compresses authorship — output reflects who merged, not who wrote.

## 3. Bug Clusters

```bash
git log -i -E --grep="fix|bug|broken" --name-only --format='' | sort | uniq -c | sort -nr | head -20
```

Files with most bug-related commits. Depends on commit message discipline — useless if the team writes "update stuff". Even a rough map is better than no map.

**Compare against step 1.** Files on both lists keep breaking and never get properly fixed.

## 4. Project Velocity

```bash
git log --format='%ad' --date=format:'%Y-%m' | sort | uniq -c
```

Commit count by month over the entire repo history. Look for shapes:
- **Steady rhythm** — healthy
- **Count drops by half in a month** — someone probably left
- **Declining curve over 6-12 months** — team losing momentum
- **Periodic spikes followed by quiet** — batch releases, not continuous shipping

## 5. Firefighting Frequency

```bash
git log --oneline --since="1 year ago" | grep -iE 'revert|hotfix|emergency|rollback'
```

Revert and hotfix frequency. A handful per year is normal. Every couple weeks means the team doesn't trust its deploy process (unreliable tests, missing staging, painful rollbacks). Zero results is also a signal — either stable or nobody writes descriptive messages.
