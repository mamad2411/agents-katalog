---
name: gitignore-rules
description: Audit .gitignore files for common pitfalls — especially directory-ignore patterns that silently break negation rules — and apply verified fixes.
category: Git & Version Control
---

# Gitignore Rules Skill

> **Skill ID:** `gitignore-rules`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Audit `.gitignore` files for structural errors and common pitfalls that
cause rules to silently fail. The most critical pattern this skill
detects is the **directory-ignore + negation failure**: when a directory
is ignored with a trailing slash (`dir/`), Git stops descending into it
entirely, so any negation patterns (`!dir/*.ext`) that follow are
**silently ignored** — the intended files are never tracked.

This skill scans for these and other pitfalls, applies safe fixes,
and verifies correctness using `git check-ignore`.

## Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.x+ |
| Shell | PowerShell 5.1+ or Bash 4+ |
| Access | Write access to the repository |

## When to Apply

Apply this skill when:

- A user asks to review, audit, or fix `.gitignore` rules
- A user reports that ignored files are not being tracked despite negation patterns
- A user adds new `.gitignore` rules with directory ignores and negations
- `git status` does not show files the user expects to be tracked
- A new `.gitignore` is being created with selective ignore/track patterns

Do NOT apply when:

- The user explicitly wants to ignore an entire directory with no exceptions
- The `.gitignore` contains only simple file-pattern rules (no negations)
- The user says "just commit it, no review needed"

---

## Core Concept: Directory-Ignore vs Contents-Ignore

This is the single most important distinction in `.gitignore`:

| Pattern | Git Behavior | Negations Work? |
|---|---|---|
| `dir/` | Ignores the **directory itself** — Git will not descend into it | **No** — negations are silently ignored |
| `dir/*` | Ignores all **contents** of the directory — Git still enters it | **Yes** — negations are evaluated |

### Why This Matters

```gitignore
# BROKEN — negation silently fails
pevers/
!pevers/*.zip

# FIXED — negation works correctly
pevers/*
!pevers/*.zip
```

In the broken example, Git sees `pevers/` and skips the entire directory.
It never reads the `!pevers/*.zip` line. The `.zip` files are ignored
along with everything else. **No warning or error is produced.**

---

## Step-by-Step Procedure

### Step 1 — Locate All `.gitignore` Files

Find every `.gitignore` in the repository. Projects may have multiple
`.gitignore` files at different directory levels.

**PowerShell:**

```powershell
Get-ChildItem -Recurse -Filter ".gitignore" |
    Where-Object { $_.FullName -notmatch '\\(\.git|node_modules|target|dist)\\' } |
    ForEach-Object { $_.FullName }
```

**Bash:**

```bash
find . -name ".gitignore" \
    -not -path '*/.git/*' \
    -not -path '*/node_modules/*' \
    -not -path '*/target/*'
```

### Step 2 — Scan for Directory-Ignore + Negation Patterns

For each `.gitignore`, identify any pattern pair where:

1. A directory is ignored with a trailing slash: `something/`
2. A negation pattern targets files inside that directory: `!something/*.ext`

**Detection logic (pseudocode):**

```
for each line in .gitignore:
    if line matches "^[^!#].*/$":           # directory ignore (trailing slash)
        dir_name = extract directory name
        scan subsequent lines for "^!{dir_name}/":
            if found → FLAG as pitfall
```

**PowerShell example:**

```powershell
$lines = Get-Content ".gitignore"
for ($i = 0; $i -lt $lines.Count; $i++) {
    $line = $lines[$i].Trim()
    if ($line -match '^([^!#].+)/$') {
        $dir = $Matches[1]
        # Check if any subsequent line negates inside this directory
        for ($j = $i + 1; $j -lt $lines.Count; $j++) {
            if ($lines[$j].Trim() -match "^!$dir/") {
                Write-Warning "Line $($i+1): '$line' blocks negation on line $($j+1): '$($lines[$j].Trim())'"
            }
        }
    }
}
```

### Step 3 — Flag and Report Findings

Present findings in a structured table:

| Line | Pattern | Issue | Affected Negation(s) |
|---|---|---|---|
| 5 | `pevers/` | Directory-ignore blocks negation | Line 6: `!pevers/*.zip` |
| 8 | `output/` | Directory-ignore blocks negation | Line 9: `!output/*.log` |

**Severity:** These are **silent failures** — Git produces no warning.
Files the user intends to track are being ignored without any indication.

### Step 4 — Apply the Fix

Convert `dir/` to `dir/*` for every flagged pattern. This changes the
semantics from "ignore the directory" to "ignore the contents," allowing
Git to descend into the directory and evaluate negation patterns.

**Transformation rule:**

```
BEFORE:  dir/
AFTER:   dir/*
```

**Important constraints:**

- Only apply this fix when the directory-ignore is followed by negation
  patterns targeting that directory
- If a directory-ignore has **no** associated negations, leave it as `dir/`
  (it is intentionally ignoring everything)
- Preserve all comments, blank lines, and ordering in the `.gitignore`

### Step 5 — Verify with `git check-ignore`

After applying fixes, verify that the intended files are no longer
ignored and that other files remain ignored.

**Verify a file is tracked (not ignored):**

```powershell
git check-ignore -v "pevers/archive.zip"
# Expected: NO output (file is not ignored)
```

**Verify other files are still ignored:**

```powershell
git check-ignore -v "pevers/some_other_file.txt"
# Expected: output showing the ignore rule that matches
```

**Bulk verification:**

```powershell
# List all files Git sees in the directory
git ls-files --others "pevers/"

# List all ignored files in the directory
git ls-files --others --ignored --exclude-standard "pevers/"
```

If the negated files appear in `--others` (untracked but visible) and
NOT in `--ignored`, the fix is working correctly.

### Step 6 — Check for Additional Pitfalls

Scan for these additional common `.gitignore` problems:

#### 6a — Negation Before Ignore (Order Matters)

```gitignore
# BROKEN — negation comes before the ignore, has no effect
!logs/*.important
logs/*

# FIXED — ignore first, then negate
logs/*
!logs/*.important
```

**Rule:** Negation patterns (`!`) must come **after** the pattern they
are negating. `.gitignore` is processed top-to-bottom; later rules
override earlier ones.

#### 6b — Negating a File Inside a Deeply Ignored Parent

```gitignore
# BROKEN — parent directory is ignored, child negation fails
build/
!build/output/release.zip

# FIXED — must un-ignore each level of the path
build/*
!build/output/
build/output/*
!build/output/release.zip
```

**Rule:** To negate a file in a nested path, every intermediate
directory must also be un-ignored.

#### 6c — Trailing Whitespace

Lines with invisible trailing spaces can cause patterns to fail
silently. Scan for and remove trailing whitespace:

```powershell
# Detect trailing whitespace
Get-Content ".gitignore" | ForEach-Object { $n++; if ($_ -match '\s+$') {
    "Line ${n}: trailing whitespace detected"
}}
```

#### 6d — Already-Tracked Files

`.gitignore` only affects **untracked** files. If a file was previously
committed, adding it to `.gitignore` will NOT remove it from tracking.

```powershell
# Remove a file from Git tracking (keep local copy)
git rm --cached "path/to/file"
```

---

## Scope Coverage

| Pattern Type | Audited? | Fix Applied? |
|---|---|---|
| `dir/` + `!dir/*.ext` (directory-ignore + negation) | Yes | `dir/` → `dir/*` |
| Negation before ignore (wrong order) | Yes | Reorder |
| Nested negation without intermediate un-ignore | Yes | Add intermediate patterns |
| Trailing whitespace | Yes | Trim |
| Already-tracked files still showing | Detected | Manual `git rm --cached` advised |
| Redundant patterns | Detected | Reported, not auto-removed |

---

## Prohibited Behaviors

The agent is **BLOCKED** from:

- **Removing user-intended ignore rules** — only structural fixes are
  allowed; never delete a pattern the user explicitly added
- **Changing semantics without a negation reason** — do NOT convert
  `dir/` to `dir/*` if there are no negation patterns for that directory
- **Modifying without verification** — Step 5 (`git check-ignore`) is
  mandatory after every fix
- **Assuming files are untracked** — always check with
  `git ls-files` whether a file is already tracked before advising
  `.gitignore` changes
- **Reordering unrelated rules** — only reorder when fixing a
  negation-before-ignore problem; preserve the user's original grouping

---

## Common Pitfalls

| Pitfall | Cause | Solution |
|---|---|---|
| Negation pattern silently ignored | `dir/` prevents Git from descending into directory | Change `dir/` to `dir/*` |
| Negation has no effect | Negation line appears before the ignore line | Move negation **after** the ignore line |
| Nested file cannot be negated | Parent directory is fully ignored | Un-ignore each intermediate directory level |
| `.gitignore` change has no effect on existing file | File was previously committed and is tracked | Run `git rm --cached <file>` to untrack |
| Pattern fails on some systems | Trailing whitespace in `.gitignore` line | Trim trailing whitespace |
| `*.log` ignores too much | Overly broad glob in root `.gitignore` | Move pattern to a subdirectory `.gitignore` or use path-qualified pattern |
| Double-star confusion | `**/dir` vs `dir/` vs `dir/**` have different semantics | `**/dir` matches at any depth; `dir/**` matches contents at any depth inside `dir` |

---

## Related Skills

| Skill | Role |
|---|---|
| [`claude-config-change-gate`](../claude-config-change-gate/SKILL.md) | **Complementary** — `.gitignore` only blocks untracked files from being tracked; the change gate also blocks commits when tracked auto-timestamped files changed only their timestamps. Pair both for full protection. |
| [`git-post-gitignore-untrack`](../git-post-gitignore-untrack/SKILL.md) | **Post-processor.** When this skill (or any commit) adds/expands a `.gitignore` and previously tracked files now match the new rules, run `git-post-gitignore-untrack` to `git rm --cached` them and fold the cleanup into the originating commit. |
| [`git-cross-repo-cherry-pick`](../git-cross-repo-cherry-pick/SKILL.md) | When the audited `.gitignore` is propagated to other repos via cherry-pick, that skill chains into `git-post-gitignore-untrack` per target repo. |
| [`gitignore-whitelist-pattern`](../gitignore-whitelist-pattern/SKILL.md) | **Complementary pattern.** When the goal is not to fix a blacklist but to generate a deny-all + whitelist block (track only specific extensions, ignore everything else). |
| [`untracked-scratch-triage`](../untracked-scratch-triage/SKILL.md) | **Upstream decision.** Use it first to *decide* whether a stray untracked file warrants a shared `.gitignore` rule at all (vs. delete or `.git/info/exclude`); then return here to author the rule correctly. |

---

## Pitfall: Folder-Ignore Hides Future Schema Additions

When ignoring **ephemeral state** inside a folder whose **future schema is
unknown** (third-party tool spool dirs, IDE per-session storage, generated
caches with versioned layouts), do **NOT** ignore the parent folder. Ignore
only the *known-ephemeral leaves* so any new sibling file the tool starts
emitting later surfaces as untracked in `git status` for explicit review.

### Wrong (over-broad — silent future drift)

```gitignore
# Hides everything the tool may emit later, including
# files the user would actually want to version-control.
some/tool/per-session/*/
```

### Right (narrow leaves — unknown siblings surface)

```gitignore
# Ignore only the leaves we have audited as ephemeral.
# Anything new the tool emits in this folder later will
# show up as untracked and force a deliberate decision.
some/tool/per-session/*/state.json
some/tool/per-session/*/contents/
```

### Canonical Real-World Case: VS Code Copilot Chat `chatEditingSessions`

`workspaceStorage/<workspace-hash>/chatEditingSessions/<sessionId>/` contains:

| Path | Status | Rationale |
|---|---|---|
| `state.json` | **Ignore** | Per-chat-turn undo/redo timeline; rewritten on every turn; canonical edit history already lives in the repo's commit log. |
| `contents/` | **Ignore** | Content-addressed snapshots of pre/post-edit file text; pure redundant churn vs Git's own blob store. |
| (future sibling files) | **Do not pre-ignore** | VS Code may add new per-session artifacts later; let them surface for triage. |

### Companion `.gitattributes` Cleanup

When narrowing an ignore rule, also audit `.gitattributes` for any
`filter=` / `diff=` / textconv lines that targeted the now-ignored leaves —
they become dead config. Example: removing the `state.json` `jq-pretty`
filter line once `state.json` is ignored.

### Audit Cue

When asked to ignore "this whole VS Code / IDE / tool state folder", first
ask: **"What are all the leaf files actually in there, and is the schema
stable?"** If the schema is unstable or undocumented, default to narrow
per-leaf ignores plus a comment explaining why the parent folder is
deliberately *not* ignored.
