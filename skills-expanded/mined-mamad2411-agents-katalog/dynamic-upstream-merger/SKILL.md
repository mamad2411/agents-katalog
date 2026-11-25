---
name: dynamic-upstream-merger
description: "Smart fork sync tool — preserves customizations while merging upstream updates. Handles content conflicts, modify/delete, and add/add conflicts with rules-based + LLM-powered resolution."
version: 1.5.0
author: <you> / the operator
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [git, merge, fork, upstream, sync, customization, conflict-resolution]
    triggers: [upstream-sync, merge-conflict, fork-merge, rebase-conflict, git-merge, smart-merge, qa-lead-fixes, defensive-branch, cross-workstation, local-patch-branch, divergence-monitoring, divergence-check, pre-rebase, rebase-decision, post-rebase-validation]
---

# Dynamic Upstream Merger (DUM)

## Purpose

Automates the process of syncing a forked git repository with its upstream while preserving custom changes. When a rebase or merge produces conflicts, DUM:

1. Identifies which files are customized (from a manifest or by comparing with upstream)
2. For each conflict, decides whether to keep our version, take upstream's version, or merge both
3. Uses configurable resolution strategies with LLM-powered fallback for complex cases
4. Completes the sync and reports what happened

## Phase 0: Pre-Rebase Assessment (Divergence Monitoring)

**Before running any sync/merge command, assess divergence** to decide whether to pull upstream now or defer. This is the single most important step for maintaining local patches over an active upstream — pulling too eagerly creates churn; deferring too long makes rebases painful.

### Step 0: Ensure Clean Working Tree

Before any divergence measurement, confirm the working tree is completely clean:

```bash
git status --short
git stash list
```

Both must produce zero output. **WIP changes (staged, unstaged, or stashed) block rebase operations and mask conflict detection.** If the tree is dirty:

- **Commit** if the change is complete and stands alone — especially important if it has been sitting across multiple pulse/status-check cycles while divergence keeps growing. Every cycle without committing widens the delta.
- **Stash** if the change is incomplete or experimental: `git stash push -m "WIP: description"`

> **Pulse/cron workflow pitfall:** In periodic status-check sessions (pulse jobs, recurring reports), WIP changes commonly sit unstaged across multiple cycles. The agent sees "1 modified file" each run and defers, but the divergence that accumulates between cycles makes every future rebase harder. **Commit or stash the WIP the first cycle you encounter it.** Do not let it sit across two consecutive cycles.

### Step 1: Measure Divergence

```
# Count commits behind upstream
git rev-list --count HEAD..origin/main

# Count commits ahead (local patches)
git rev-list --count origin/main..HEAD
```

### Step 2: Check File Overlap

If zero local fix files are touched by upstream commits, the rebase is predicted clean. If they do overlap, manual reconciliation is needed:

```
# List upstream commits since last merge base
git log --oneline --format="%h %s" HEAD..origin/main

# Check if any touch your critical fix files
git log --oneline --format="%h %s" HEAD..origin/main -- tools/approval.py tools/tirith_security.py

# Stat check for broader file-level risk
git diff --stat origin/main..origin/main~N
```

**📖 For quantitative per-file delta analysis — measuring exactly how many lines upstream changed in each file you also modified — see `references/rebase-delta-analysis.md`**. This covers the `git merge-base` + `git diff --stat` technique for file-level risk assessment, function-level hunk overlap detection, WIP syntax checking before rebase, and a decision matrix based on per-file delta size.

**📖 For semantic upstream change analysis — understanding *what* upstream's refactor does (not just how many lines changed) and how it interacts with your local fixes — see `references/upstream-change-semantic-analysis.md`**. This covers categorizing local/upstream interactions (same-zone vs cross-zone vs pipeline-order-dependent), reading upstream refactors for intent, and detecting semantic regression vectors that no textual-merge analysis can catch.

### Step 3: Predict Merge Safety

The most reliable approach is a trial rebase on a throwaway branch — this exercises git's actual merge logic rather than approximating it:

```bash
# Fetch latest upstream first
git fetch origin
# Create temp branch at current HEAD and attempt rebase
TRIAL_BRANCH="trial-rebase-$(date +%s)"
git checkout -b "$TRIAL_BRANCH"
if git rebase origin/main 2>&1; then
  echo "✅ Rebase predicted CLEAN — no conflicts"
  git checkout "$(git rev-parse --abbrev-ref HEAD)@{upstream}" 2>/dev/null \
    || git switch - 2>/dev/null
  main_branch="main"  # may be origin/main; restore
else
  echo "❌ Conflicts detected — aborting trial"
  git rebase --abort 2>/dev/null
  git switch - 2>/dev/null || git checkout main
fi
git branch -D "$TRIAL_BRANCH" 2>/dev/null; true
```

> **Why a trial rebase over `git merge-tree`:** `git merge-tree` outputs conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) as part of the tree blob but does **not** exit non-zero on conflicts nor emit the word "CONFLICT." A throwaway-branch rebase is simpler, equally fast, and exercises git's actual conflict resolver including rename detection and recursive merge strategies.

If conflicts exist, examine them:
- `git diff --name-only --diff-filter=U` lists conflicted files
- Check if the conflicts are in files where your local approach should win (e.g., Windows-specific path handling that upstream reverts), or where non-trivial reconciliation is needed

### Step 4: Decide When to Rebase

| Condition | Action |
|-----------|--------|
| < 10 commits behind, zero file overlap | Pull immediately — low risk, low churn |
| < 50 commits, zero file overlap | Pull — worth staying current |
| > 50 commits, zero file overlap | Consider pulling — divergence can grow fast |
| **Any divergence** with file overlap in customized files | Pull ASAP — overlapping upstream changes risk becoming harder to reconcile as divergence grows. Each cycle widens the diff. **Deferring makes the merge harder, not easier.** |
| Upstream reverted your fix (common with platform-specific patches) | Pull — your fix auto-reapplies via semantic stacking on top of the revert. `git merge-tree` reports 0 textual conflicts. Manual check post-rebase: `git diff HEAD~1 -- <fix-file>` confirms ordering is intact. |
| qa-lead/fixes branch is >500 behind | Rebase it irrespective of main divergence to keep it mergeable. Stale qa-lead branches lose value as recovery points. |

**Factor in divergence velocity, not just absolute count.** A repo 50 commits behind growing at 2/day is very different from 50 behind growing at 50/day. Measure velocity by tracking the behind-count across consecutive checks:

```bash
# Track velocity — run this each check cycle
echo "Behind: $(git rev-list --count HEAD..origin/main)"
echo "Since last check: $((NEW_BEHIND - OLD_BEHIND)) new upstream commits"
```

If velocity is >20 commits/hour and you're already >100 behind, the rebase window is closing fast — pull within the same session rather than deferring to the next cycle.

### Step 5: Post-Rebase Validation (CRITICAL)

After every rebase, validate that local fix patterns survived:

```
# 1. Verify fix file changes are intact
git diff HEAD~1 -- tools/approval.py

# 2. Run regression test suites
python -m pytest tests/tools/test_approval.py tests/tools/test_tirith_security.py -x -q --no-header

# 3. Check for unintended deletions
git diff --stat HEAD~1

# 4. Verify test count hasn't dropped (tests may be lost in merge)
python -m pytest tests/tools/test_approval.py --collect-only | grep "selected"
```

A rebase that produces zero textual conflicts can still semantically undo a fix if upstream reordered the same pipeline. Always validate post-rebase with (`git diff` + test run).

> **📖 For the full methodology on detecting these semantic regressions — pipeline-order-dependent fixes, upstream refactors that change regex/policy engines, and categorizing each local fix's interaction risk — see `references/upstream-change-semantic-analysis.md`**. The cross-zone vs same-zone vs pipeline-order-dependent framework tells you which effects will survive a clean merge and which will silently break.

#### Windows-Specific Recurring Pattern: `Path.home()` / `USERPROFILE` / `HOME`

**This is the most commonly re-lost fix across Windows rebases.** The pattern: a test monkeypatches `HOME` to control where `Path.home()` resolves during a test. On Windows, `Path.home()` ignores the `HOME` env var entirely — it uses `USERPROFILE` (or `HOMEDRIVE`+`HOMEPATH`). The fix is to add `monkeypatch.setenv("USERPROFILE", ...)` alongside every `monkeypatch.setenv("HOME", ...)` call.

**Why it keeps getting lost:** Upstream contributors (mostly macOS/Linux) occasionally rewrite test files. They see `monkeypatch.setenv("HOME", ...)` and keep it, but never add `USERPROFILE` because they don't run on Windows. When you rebase onto their rewrite, the `USERPROFILE` line vanishes — even though `HOME` survived — and the test breaks silently on your platform. Merge-tree reports zero textual conflicts (the `HOME` line is untouched), so this is a **pure semantic regression**.

**Post-rebase detection command:**
```bash
# Find any test that sets HOME without USERPROFILE — these will break on Windows
grep -rn 'monkeypatch.setenv("HOME"' tests/ | \
  grep -v 'monkeypatch.setenv("USERPROFILE"' | head -20
```

**Fix when detected:**
```python
# Add USERPROFILE alongside HOME every time
monkeypatch.setenv("HOME", "/home/user")
monkeypatch.setenv("USERPROFILE", "/home/user")  # Windows compat
```

**Known affected test files (all fixed at least once):**
- `tests/agent/lsp/test_workspace.py` — `test_normalize_path_expands_tilde`
- `tests/agent/test_prompt_builder.py` — various PostSetup tests
- `tests/tirith/` — various platform-guard tests
- `tests/tools/test_approval.py` — config write-protection tests
- `tests/plugins/` — hindsight PostSetup tests

Run the grep command above as part of every post-rebase check on Windows. Like the `git diff HEAD~1 -- <fix-file>` check, this catches regressions that no textual-merge analysis can see.

## Usage

```bash
# 1. Initialize — analyzes fork vs upstream, generates customization manifest
python merger.py init /path/to/repo https://github.com/upstream/project

# 2. Sync — fetch upstream changes and smart-merge
python merger.py sync /path/to/repo [--strategy smart]

# 3. Interactive resolve — step through remaining conflicts
python merger.py resolve /path/to/repo [--interactive]
```

## Resolution Strategies

| Strategy | Behavior |
|----------|----------|
| `smart` (default) | Uses the customization manifest + heuristics to auto-resolve. Falls back to LLM for unknown conflicts. |
| `keep-ours` | Local customizations win in all conflicts |
| `keep-theirs` | Upstream changes always win |

## Sync Methods

| Method | Behavior |
|--------|----------|
| `merge` (default, preferred) | Creates a merge commit. Preserves all custom commits in history. Recommended for most forks. |
| `rebase` | Replays custom commits on top of upstream. **Danger:** if conflicts are resolved to upstream, empty commits get dropped, losing custom files. Only use when you want linear history. |

**⚠️ CRITICAL: Always prefer `merge` over `rebase` for fork sync.** When you rebase and resolve conflicts to upstream (even in just some files), git can drop custom commits it considers "empty" — permanently removing added files and custom code from the branch. Merge keeps all commits and just adds a merge commit on top.

## Conflict Types & Resolution

### 1. Content Conflicts
Both sides modified the same file. Resolution:
- **High-priority custom files** → always keep-ours
- **Unmodified files** → always theirs
- **Medium-priority** → smart merge (attempt to combine both sides)

### 2. Modify/Delete Conflicts
One side deleted a file the other modified. Resolution:
- **We deleted, they modified** → if in `custom_removed_files`, keep deleted; otherwise accept theirs
- **They deleted, we modified** → if in `custom_changes`, keep ours; otherwise accept deletion

### 3. Add/Add Conflicts
Both sides added the same file. Resolution:
- If it's in `custom_added_files`, keep ours
- Otherwise, take theirs

## Customization Manifest

Auto-generated by `init`, the manifest lives at `.hermes/merger-customizations.json` in the repo. It records:

```json
{
  "custom_changes": {
    "path/to/file.rs": {
      "reason": "Added model provider selection for OpenRouter support",
      "strategy": "merge-upstream-additions",
      "priority": "high"
    }
  },
  "custom_added_files": ["path/to/new-file.md"],
  "custom_removed_files": ["path/to/deleted-file.rs"],
  "last_upstream_base": "abc123def"
}
```

## CI Integration

For GitHub Actions, you don't need to download the merger.py script. The customization manifest + bash conflict resolver is self-contained:

```yaml
- name: Merge upstream changes (with smart conflict resolution)
  run: |
    git checkout main
    git merge upstream/main 2>&1 || {
      echo "Conflicts detected. Auto-resolving..."
      for file in $(git diff --name-only --diff-filter=U); do
        if python -c "
import json
with open('.hermes/merger-customizations.json') as f:
    m = json.load(f)
if '$file' in m.get('custom_changes', {}) or '$file' in m.get('custom_added_files', []):
    exit(0)
exit(1)
"; then
          echo "  Keeping our version: $file (customized)"
          git checkout --ours -- "$file"
        else
          echo "  Taking upstream version: $file (not customized)"
          git checkout --theirs -- "$file"
        fi
        git add "$file"
      done
      git commit --no-edit
      echo "Auto-merge completed"
    }
```

See `references/ci-integration.md` for a full workflow example.

## Script

The `merger.py` script is the core engine. See `scripts/merger.py` for the full implementation.

## Defensive Branch Pattern (Cross-Workstation Survival)

When multiple machines/workspaces share a fork, one machine running `git reset --hard origin/main` (by a CI/CD process, another agent profile, or a stale script) silently destroys local commits made on any other machine. After 6+ cycles of this pattern in the Hermes dev team, the proven countermeasure is a **defensive branch**:

### Setup

```bash
# 1. Create a persistent branch for local fixes
git checkout -b qa-lead/fixes
# Add all your local patches here

# 2. Push to a fork as offsite backup
git remote add pmb2 git@github.com:your-fork/hermes-agent.git
git push pmb2 qa-lead/fixes

# 3. After each sync, rebase the qa-lead branch onto latest main
git checkout qa-lead/fixes
git rebase origin/main
git push pmb2 qa-lead/fixes --force  # force-push OK — personal branch
```

### Recovery After Reset

When `git reset --hard origin/main` destroys local commits:

```bash
# Option A — qa-lead branch (fastest)
git cherry-pick qa-lead/fixes~5..qa-lead/fixes  # replay last 5 fixes
git checkout -B qa-lead/fixes HEAD              # re-align qa-lead branch
git push pmb2 qa-lead/fixes --force

# Option B — reflog (last resort, full systematic workflow)
# See references/reflog-recovery.md for the complete 7-phase
# systematic recovery (classify commits, handle conflicts,
# handle working tree overlap, verify, push).
git reflog --date=iso --format="%H %gd %gs" | head -50
git cherry-pick <oldest-sha>   # one at a time, oldest first
git cherry-pick <second-sha>
```

### Tactical Rules

- **qa-lead/fixes is a personal patch branch** — force-push is expected; it is NOT a shared development branch
- **Keep multiple fork backup branches** named with dates:
  `qa-lead/recover-<sha>` (immediate recovery point)
  `qa-lead/verified-fixes-<YYYY-MM-DD>` (periodic snapshots)
- **Rebase onto origin/main after every upstream sync** — qa-lead/fixes stays mergeable so cherry-picks are clean
- **Only commit finished, validated fixes** — qa-lead/fixes is not a WIP branch. Every commit should stand alone as something worth preserving
- **When upstream reverts a fix you need** (common with Windows-specific patches), keep it on qa-lead/fixes. On each sync, cherry-pick it back. The reflog on the qa-lead branch itself is a safety net.

### When This Pattern Is Needed

Any setup where:
1. You maintain local patches that cannot (or should not) be pushed to upstream `origin/main`
2. Multiple independent workstations or agent profiles share the same repo
3. One of those workspaces runs `git reset --hard origin/main` as part of its standby/sync workflow

The AI dev team (Hermes Forge + other profiles) hitting the same repo from different machines is the canonical case.

## Pitfalls

- **Rebase loses custom files** — If you rebase and resolve conflicts to upstream's version, git drops the commit as "empty" and your added files vanish into thin air. Always use `--method merge` for fork sync. The git reflog can recover lost commits if this happens.
- **Cross-workstation reset destroys local commits** — If another machine/agent profile runs `git reset --hard origin/main`, your un-pushed commits are discarded. Mitigate with a defensive branch (`qa-lead/fixes`) pushed to a fork. Recovery via cherry-pick from the qa-lead branch is faster than reflog (which itself can be wiped by subsequent operations).**Do not rely on origin/main as safe storage for local patches.**
- **Semantic merge: zero textual conflicts ≠ fix survived** — When upstream reverts a pipeline ordering (e.g., moves backslash-strip before path rewrite) but your commit restores it on top, auto-merge reports 0 conflicts. The fix is intact only because it was applied *after* the revert. This stacking works by coincidence of commit ordering — if the next rebase interleaves new upstream commits that touch the same function, the auto-merge may silently choose upstream's order over yours. Always run `git diff HEAD~N -- <fix-file>` and the targeted test suite after every rebase, even when merge-tree reports clean. This pattern is the single most common cause of silent regression in multi-patch workflows.
- **Python json inside bash YAML** — When embedding the manifest check in GitHub Actions YAML, use `python -c "..."` with single-quoted JSON keys and proper escaping. Heredocs with raw JSON break YAML parsing.
- **Sync failure cascade** — If the CI workflow's merge step fails mid-way, the next run starts from the current state (not from where it left off). The merge commit from a partial run may have resolved some files and left others. Always check `git status` before retrying.
- **Origin vs head divergence** — After a failed rebase attempt that was pushed (force-push), the local and remote diverge. The merge approach avoids this by not requiring force-push.
