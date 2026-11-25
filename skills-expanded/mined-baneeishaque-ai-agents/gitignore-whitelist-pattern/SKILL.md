---
name: gitignore-whitelist-pattern
description: >-
  Generate a deny-all + whitelist `.gitignore` block for directories that should
  only contain specific file types (e.g., archives) and Git configuration files —
  the complementary pattern to the directory-ignore audit in gitignore-rules.
category: Git & Version Control
---

# Gitignore Whitelist Pattern Skill (v1)

> **Skill ID:** `gitignore-whitelist-pattern`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Generate a **deny-all + selective whitelist** `.gitignore` block for directories that
must track only a narrow set of file extensions (e.g., `.7z`, `.zip`) and Git
configuration files (`.gitignore`, `.gitattributes`), while ignoring everything else —
including extracted folders, temp files, and any future additions that do not match the
whitelist.

This is the inverse of the typical `.gitignore` approach (blacklisting specific
patterns). It is the correct pattern when:

- A directory stores large archives that must be tracked (often via Git LFS) alongside
  an unpredictable set of extracted or temporary artifacts that must **never** be
  committed.
- The set of **wanted** files is small and well-defined, while the set of **unwanted**
  files is open-ended and unpredictable.

***

## 1. Environment & Dependencies

| Requirement | Minimum |
|---|---|
| VCS | Git 2.x+ |
| Shell | PowerShell 5.1+ or Bash 4+ |
| Access | Write access to the target `.gitignore` |

### 1.1 Verification

```powershell
git --version
git rev-parse --is-inside-work-tree
```

***

## 2. When to Apply

Apply this skill when:

- A user asks to track **only** specific file extensions in a directory and ignore
  everything else (folders, other files, future additions)
- A directory contains large archives alongside extracted folders that must not be
  committed
- The user says "I only need X files here, nothing else"
- A directory's tracked content should be a closed whitelist, not an open blacklist

Do **NOT** apply when:

- The user wants to ignore specific known files/patterns (standard blacklist — use
  normal `.gitignore` rules)
- The directory has a predictable set of unwanted files that can be enumerated (standard
  blacklist is simpler)
- The user wants to ignore an entire directory with no exceptions
- The `.gitignore` already uses the deny-all + whitelist pattern correctly

***

## 3. Core Concept: Deny-All + Whitelist

### 3.1 The Pattern

```gitignore
# Ignore everything
*

# Allow git configuration files
!.gitignore
!.gitattributes

# Allow specific file types
!*.7z
```

### 3.2 How It Works

| Line | Git Behavior |
|---|---|
| `*` | Matches every file and directory — everything is ignored |
| `!.gitignore` | Negation — re-includes `.gitignore` so the rules themselves are tracked |
| `!.gitattributes` | Negation — re-includes `.gitattributes` (e.g., for LFS tracking rules) |
| `!*.7z` | Negation — re-includes all files matching `*.7z` at this directory level |

### 3.3 Why `*` and Not `*/`

Using `*` (no trailing slash) is deliberate:

- `*` ignores **both** files and directories at the current level.
- `*/` would ignore **only directories**, still allowing unknown files through.
- Since negation patterns (`!*.ext`) target files, and `*` blocks everything, the
  combination creates a tight whitelist where only explicitly negated patterns pass.

### 3.4 Why Git Config Files Must Be Whitelisted

The `*` pattern ignores the `.gitignore` file itself. Without `!.gitignore`, Git would
ignore the ignore file — creating a bootstrap paradox where the rules cannot be
committed. The same applies to `.gitattributes` if present (commonly used for LFS
tracking rules in archive directories).

***

## 4. Step-by-Step Procedure

### Step 1 — Identify the Target Directory

Determine which directory needs the whitelist pattern. Common indicators:

- Directory contains archives (`.7z`, `.zip`, `.tar.gz`) alongside extracted folders
- Directory stores binary deliverables that should be tracked while working copies
  should not
- User explicitly states only certain file types belong in version control

### Step 2 — Determine the Whitelist

Collect the set of extensions and files to whitelist. At minimum, always include:

1. **Git configuration files**: `.gitignore`, `.gitattributes`
2. **User-specified extensions**: e.g., `*.7z`, `*.zip`, `*.tar.gz`

Ask the user to confirm the whitelist before proceeding.

### Step 3 — Generate the `.gitignore` Block

Construct the block following this template:

```gitignore
# Ignore everything
*

# Allow git configuration files
!.gitignore
!.gitattributes

# Allow <description of whitelisted types>
!*.<ext1>
!*.<ext2>
```

**Ordering rules:**

1. The `*` deny-all rule MUST come first
2. Git configuration file negations MUST come second
3. Extension whitelist negations MUST come last, one per line

### Step 4 — Insert into the `.gitignore`

**If the `.gitignore` already exists** (e.g., generated by a `.gitignore` generator):

- Append the deny-all + whitelist block under the `# Custom rules` section if one
  exists, or at the end of the file.
- The generated OS/IDE patterns above the block are still useful — they provide a second
  layer of defense for common noise files. The `*` deny-all makes them redundant in
  practice, but they serve as documentation of intent and protect against accidental
  removal of the `*` line.

**If no `.gitignore` exists:**

- Create the file with the deny-all + whitelist block as the sole content.

### Step 5 — Verify

```powershell
# Verify whitelisted files are NOT ignored
git check-ignore -v "path/to/dir/archive.7z"
# Expected: NO output (file is not ignored)

# Verify other files ARE ignored
git check-ignore -v "path/to/dir/some_folder"
# Expected: output showing the * rule matches

# List what Git sees in the directory
git ls-files --others "path/to/dir/"

# List what Git ignores in the directory
git ls-files --others --ignored --exclude-standard "path/to/dir/"
```

### Step 6 — Untrack Previously Committed Artifacts

If the directory previously tracked files that should now be ignored (e.g., extracted
folders committed before the whitelist was added), follow the
[`git-post-gitignore-untrack`](../git-post-gitignore-untrack/SKILL.md) skill to
`git rm --cached` them and fold the cleanup into the commit.

***

## 5. Common Whitelist Recipes

### 5.1 Archive-Only Directory (e.g., PVER deliverables)

```gitignore
# Ignore everything
*

# Allow git configuration files
!.gitignore
!.gitattributes

# Allow compressed archives
!*.7z
```

### 5.2 Archive + Documentation Directory

```gitignore
# Ignore everything
*

# Allow git configuration files
!.gitignore
!.gitattributes

# Allow compressed archives
!*.7z
!*.zip

# Allow documentation
!*.md
!*.txt
```

### 5.3 Multi-Extension Archive Directory

```gitignore
# Ignore everything
*

# Allow git configuration files
!.gitignore
!.gitattributes

# Allow all common archive formats
!*.7z
!*.zip
!*.tar.gz
!*.tar.xz
!*.tar.bz2
```

### 5.4 Nested Directory Whitelist

When the whitelisted files may exist in subdirectories, the `*` pattern must be
augmented. By default, `*` only matches at the current directory level. To deny
recursively and selectively whitelist at depth:

```gitignore
# Ignore everything at all depths
*

# Allow git configuration files
!.gitignore
!.gitattributes

# Allow subdirectories to be entered (required for nested whitelisting)
!*/

# Allow specific files at any depth
!**/*.7z
```

**Warning:** `!*/` re-includes all directories. This means empty directories become
visible. Only use this variant when whitelisted files genuinely live in subdirectories.

***

## 6. Interaction with `.gitattributes`

When the whitelisted extensions are large binaries, a `.gitattributes` file in the same
directory is common for Git LFS tracking:

```gitattributes
*.7z filter=lfs diff=lfs merge=lfs -text
```

The `!.gitattributes` line in the whitelist pattern ensures this file is tracked
alongside the archives. Without it, the LFS tracking rules themselves would be ignored.

***

## 7. Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| Whitelisted file still ignored | The `.gitignore` is in a parent directory and a parent `*` rule takes precedence | Place the whitelist `.gitignore` in the target directory itself, not a parent |
| Folder appears in `git status` | `!*/` was added for nested whitelisting but empty dirs are now visible | Remove `!*/` if nested whitelisting is not needed |
| `.gitignore` itself is not tracked | `!.gitignore` line is missing | Add `!.gitignore` before any extension whitelist lines |
| New file type not tracked | Extension not in the whitelist | Add `!*.newext` to the whitelist |
| `git check-ignore` shows no match for an ignored file | The file was previously committed and is tracked | Run `git rm --cached <file>` per [`git-post-gitignore-untrack`](../git-post-gitignore-untrack/SKILL.md) |

***

## 8. Related Skills

| Skill | Role |
|---|---|
| [`gitignore-rules`](../gitignore-rules/SKILL.md) | **Structural audit.** Detects directory-ignore + negation pitfalls in `.gitignore` files. Complementary — that skill audits blacklist-style patterns; this skill generates whitelist-style patterns. |
| [`git-post-gitignore-untrack`](../git-post-gitignore-untrack/SKILL.md) | **Post-processor.** After applying the deny-all + whitelist block, run this skill to untrack files that were previously committed but are now ignored. |
| [`git-lfs-selective-clone`](../git-lfs-selective-clone/SKILL.md) | **LFS companion.** When the whitelisted files are large binaries tracked by LFS, this skill handles selective LFS blob retrieval. |
