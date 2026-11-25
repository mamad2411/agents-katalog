---
name: noise-removal-via-commit-edit
description: Detect and remove IDE artifact noise (m2e, JDT LS,
    filteredResources) from existing commits using the [git-commit-edit](../git-commit-edit/SKILL.md)
    skill, with mandatory user confirmation.
category: Git & Repository Management
---

# IDE Noise Removal via Commit Edit Skill

> **Skill ID:** `noise-removal-via-commit-edit`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Detect and remove IDE artifact noise from **existing commits** using
the [`commit_edit`](../git-commit-edit/SKILL.md) skill as the execution
mechanism. This skill is a specialized layer that adds noise detection,
classification, tracked-vs-untracked safety analysis, and mandatory
user confirmation on top of the general commit edit workflow.

IDE tooling (VS Code JDT Language Server, Eclipse m2e, IntelliJ)
frequently auto-injects boilerplate into project metadata files
(`.project`, `.classpath`, `.settings/`). When these changes are
accidentally committed alongside functional work, they pollute the
commit history. This skill surgically removes them.

## Source Rules & Prerequisite Skills

| Dependency | Role |
|---|---|
| [`commit_edit`](../git-commit-edit/SKILL.md) | Execution mechanism — interactive rebase, amend, replay |
| [`git_atomic_commit`](../git-atomic-commit-construction/SKILL.md) Step 3g | IDE artifact detection patterns, user confirmation workflow |
| [`git-operation-rules.md`](../../../ai-agent-rules/git-operation-rules.md) | Stash/push/commit protocols |

## Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.x+ |
| Shell | PowerShell 5.1+ or Bash 4+ |
| Access | Write access to the project repository |
| Skills | [`commit_edit`](../git-commit-edit/SKILL.md) must be available |

## When to Apply

Apply this skill when:
- A user asks to "remove noise from a commit" or "clean up IDE
  artifacts from history"
- Inspection of an existing commit reveals IDE-generated boilerplate
  mixed with functional changes
- `git show --stat <commit>` shows a disproportionate number of
  `.project`, `.classpath`, or `.settings/` files alongside functional
  changes
- The user identifies a specific commit with IDE noise and asks to
  edit it

Do NOT apply when:
- The noise is in the **working tree** (uncommitted) — use
  [`git_atomic_commit`](../git-atomic-commit-construction/SKILL.md) Step 3g instead
- The commit needs to be fully split into multiple atomic commits — use
  [`git_history_refinement`](../git-history-refinement/SKILL.md) instead
- The user wants to remove noise from multiple commits across a range —
  apply this skill iteratively, one commit at a time, starting from
  the oldest

---

## Step-by-Step Procedure

### Step 0 — Noise Detection & Classification

#### 0a — Inspect the Target Commit

Show the full file list of the target commit:

```powershell
git show --stat <commit-hash>
```

#### 0b — Separate Noise from Functional Content

Categorize every file in the commit into noise vs functional:

```powershell
# Count noise files (IDE metadata patterns)
git diff --name-only <commit-hash>~1 <commit-hash> -- "*.project" | Measure-Object -Line
git diff --name-only <commit-hash>~1 <commit-hash> -- "*.classpath" | Measure-Object -Line
git diff --name-only <commit-hash>~1 <commit-hash> -- "*.settings/*" | Measure-Object -Line

# Show functional (non-noise) content
git show --stat <commit-hash> -- ':!*.project' ':!*.classpath' ':!*.settings'
```

#### 0c — Verify Noise Content

Inspect a representative noise file to confirm it matches known IDE
artifact patterns:

```powershell
git show <commit-hash> -- <sample-noise-file>
```

**Known IDE noise patterns:**

| Pattern | Source | Content |
|---|---|---|
| `maven2Builder` + `maven2Nature` in `.project` | JDT Language Server (embedded m2e) | Auto-injected when `pom.xml` detected |
| `<filteredResources>` with `regexFilterMatcher` in `.project` | JDT Language Server | Filters `node_modules\|\.git\|__CREATED_BY_JAVA_LANGUAGE_SERVER__` |
| Self-closing tags expanded (e.g., `<comment/>` → `<comment></comment>`) | JDT Language Server | XML reformatting of `.project` |
| `org.eclipse.m2e.core.prefs` in `.settings/` | JDT LS m2e import | m2e workspace preferences |
| `org.eclipse.core.resources.prefs` in `.settings/` | Eclipse workspace | Encoding preferences |

#### 0d — Attribution Accuracy

Correctly attribute the noise source. The agent **MUST NOT** claim
that `.project` modifications come from the VS Code Maven extension
(`vscjava.vscode-maven`). The Maven UI extension provides only the
explorer and goal execution interface. The `.project` and `.classpath`
modifications are injected by the **Eclipse JDT Language Server**
(`eclipse.jdt.ls`), which bundles **m2e** (Eclipse's Maven integration)
internally.

---

### Step 1 — Mandatory User Confirmation

The agent **MUST** present the noise analysis to the user and obtain
explicit confirmation before proceeding. This is non-negotiable because
some projects intentionally track IDE metadata.

#### 1a — Present the Noise Report

````markdown
## IDE Noise Detected in Commit `<short-hash>`

**Commit:** `<short-hash>` — `<commit message>`
**Date:** <commit date>

### Noise Files (<count> files)
| # | File | Noise Type |
|---|---|---|
| 1 | `com.acme.example1/.project` | m2e builder/nature injection |
| 2 | `com.acme.example2/.project` | m2e builder/nature injection |
| ... | ... | ... |

### Functional Files (<count> files, preserved)
| # | File | Change |
|---|---|---|
| 1 | `src/Main.java` | +35 lines (feature logic) |
| 2 | `docs/SETUP.md` | +82 lines (documentation) |
| ... | ... | ... |

### Summary
- **Before edit:** <total> files changed, +<additions> / −<deletions>
- **After edit:** <functional-count> files changed (noise removed)
- **Noise removed:** <noise-count> files

### Proposed discard command:
```powershell
git checkout HEAD~1 -- $(git diff --name-only HEAD~1 HEAD -- "*.project")
```

**⚠️ Warning:** If this project intentionally tracks `.project` files
for shared workspace configuration, removing these changes may break
the intended project setup for other developers.

Proceed with noise removal? (yes / no / inspect further)
````

#### 1b — Act on User Feedback

- **"yes"** — Proceed to Step 2 (execute the commit edit).
- **"no"** — Abort. Do not modify the commit.
- **"inspect further"** — Show full diffs for specific noise files
  so the user can confirm each one:
  ```powershell
  git show <commit-hash> -- "<specific-file>"
  ```
- **Partial removal** — If the user identifies only some files as
  noise, adjust the removal list accordingly.

---

### Step 2 — Execute Commit Edit

Delegate to the [`commit_edit`](../git-commit-edit/SKILL.md) skill for
the actual rebase operation. The steps are:

#### 2a — Stash (if needed)

Per [`commit_edit`](../git-commit-edit/SKILL.md) Step 1.

#### 2b — Interactive Rebase

Per [`commit_edit`](../git-commit-edit/SKILL.md) Step 2.

#### 2c — Remove Noise Files

Once the rebase stops at the target commit, restore all noise files
to their parent's version:

```powershell
# Remove all .project noise
git checkout HEAD~1 -- $(git diff --name-only HEAD~1 HEAD -- "*.project")

# Remove all .classpath noise (if applicable)
git checkout HEAD~1 -- $(git diff --name-only HEAD~1 HEAD -- "*.classpath")
```

**Granular removal** (when only some `.project` files are noise):

```powershell
git checkout HEAD~1 -- "path/to/noise/.project" "other/path/.project"
```

#### 2d — Verify Noise Removal

Before amending, confirm only functional changes remain staged:

```powershell
# Confirm noise files are gone
git diff --cached --stat -- "*.project" | Select-Object -Last 1

# Confirm functional files are untouched
git show --stat HEAD -- ':!*.project' ':!*.classpath'
```

#### 2e — Amend, Continue, Restore

Per [`commit_edit`](../git-commit-edit/SKILL.md) Steps 4–7.

---

### Step 3 — Post-Edit Verification

#### 3a — Tree Parity Check

Verify that the non-noise content of the edited commit is **identical**
to the original. The edit should have changed ONLY the noise files:

```powershell
# Compare file count
git show --stat <new-hash> -- ':!*.project' ':!*.classpath'
```

The functional file count and line changes MUST match the pre-edit
analysis from Step 0b.

#### 3b — Descendant Integrity

Verify all descendant commits were replayed successfully:

```powershell
git log --oneline <new-hash>..HEAD
```

The count must match the pre-edit descendant count from
[`commit_edit`](../git-commit-edit/SKILL.md) Step 0c.

#### 3c — Report Results

Present the final summary to the user:

```markdown
## Noise Removal Complete

**Edited commit:** `<new-hash>` (was `<old-hash>`)
**Before:** <total> files changed, +<old-additions> / −<old-deletions>
**After:** <functional-count> files changed, +<new-additions> / −<new-deletions>
**Noise removed:** <count> files (<type> pattern)
**Descendants replayed:** <count> (all successful)
**Branch divergence:** Force push required (if applicable)
```

---

## Iterative Application

When multiple commits in a range contain noise, apply this skill
**iteratively starting from the oldest commit**. This minimizes
conflict risk during descendant replay:

1. Identify all noisy commits:
   ```powershell
   git log --oneline --all -- "*.project" | Select-Object -First 20
   ```

2. Edit the oldest noisy commit first.

3. After rebase completes, re-identify remaining noisy commits (their
   hashes will have changed due to the rebase).

4. Repeat until all noisy commits are clean.

---

## Scope Coverage

| Category | Convention |
|---|---|
| m2e builder/nature injection | Restore `.project` from parent commit |
| `<filteredResources>` blocks | Restore `.project` from parent commit |
| XML tag reformatting | Restore `.project` from parent commit |
| `.classpath` lib entries (auto-added) | Restore `.classpath` from parent commit |
| `.settings/` m2e/resources prefs | Restore from parent commit |
| Mixed noise + functional in `.project` | Hunk-based staging after parent restore, then re-add functional hunks |

---

## Prohibited Behaviors

The agent is **BLOCKED** from:

- **Auto-removing noise without user confirmation** — The noise report
  and user approval are mandatory, even when the pattern is obvious
- **Misattributing noise source** — Never claim `.project` changes
  come from `vscjava.vscode-maven`; they come from JDT Language Server
  (embedded m2e)
- **Removing files the project intentionally tracks** — If `.project`
  files contain functional configuration mixed with noise, use
  hunk-based staging, not wholesale file restoration
- **Editing multiple commits in a single rebase** — Edit one commit
  per rebase session to minimize conflict risk
- **Skipping the tree parity check** — Post-edit verification is
  mandatory to ensure functional content was not accidentally altered

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| All `.project` files removed but some had functional changes mixed in | Inspect a sample diff before bulk removal; use hunk-based staging for mixed files |
| Assumed `.project` noise came from VS Code Maven extension | Attribute correctly: JDT Language Server bundles m2e internally |
| Edited newest commit first in a multi-commit cleanup | Always start from the oldest noisy commit to minimize replay conflicts |
| Functional `.classpath` entries (e.g., TUL lib paths) removed as noise | The `.classpath` may contain both noise (m2e container) and functional (lib paths); inspect before removing |
| Descendant count mismatch after rebase | A descendant may have become empty (its only changes were to noise files); confirm with user before skipping |
| Post-edit file count doesn't match pre-edit functional count | Re-inspect the amended commit; some functional files may have been accidentally restored to parent state |
