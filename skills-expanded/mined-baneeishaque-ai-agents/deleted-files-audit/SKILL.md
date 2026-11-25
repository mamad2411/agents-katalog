---
name: deleted-files-audit
description: Systematic audit of deleted files in a Git repository — categorizing deletions, scanning for stale references, checking IDE configs, and reporting a safety verdict.
category: Code Hygiene & Maintenance
---

# Deleted Files Audit Skill

> **Skill ID:** `deleted-files-audit`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Audit files that have been deleted (but not yet committed) in a Git
repository. This skill detects all pending deletions, categorizes each
one by type (generated output, input data, snapshot, source code, config),
scans the entire codebase for stale references, checks IDE run
configurations, identifies `.gitignore` coverage gaps, and produces a
structured safety verdict per file or group.

Deleted files that are still referenced by source code, build scripts,
or IDE configurations cause silent failures — broken builds, runtime
`FileNotFoundException`, or IDE launch errors. This skill catches those
problems **before** the deletion is committed.

## Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.x+ |
| Shell | PowerShell 5.1+ or Bash 4+ |
| Access | Read access to the project repository |

## When to Apply

Apply this skill when:
- A user says they deleted files and asks you to verify the deletions
- `git status` shows pending `deleted:` entries (staged or unstaged)
- A user asks to "clean up" or "remove obsolete files" from a project
- A pre-commit review is requested after bulk file removal
- Output directories or generated artifacts were manually removed

Do NOT apply when:
- Files were deleted by a prior commit and the user is not questioning them
- The deletion is part of a `git mv` (rename) — that is a move, not a deletion
- The user explicitly says "just commit the deletions, no review needed"

---

## Step-by-Step Procedure

### Step 1 — Detect All Deleted Files

Run `git status` to discover every pending deletion — both staged and
unstaged.

**PowerShell:**

```powershell
# Full status showing all deleted files
git status

# Machine-parseable — deleted only (unstaged)
git diff --name-only --diff-filter=D

# Machine-parseable — deleted only (staged)
git diff --cached --name-only --diff-filter=D
```

**Bash:**

```bash
git status
git diff --name-only --diff-filter=D
git diff --cached --name-only --diff-filter=D
```

**Output:** A complete list of deleted file paths, separated into staged
and unstaged groups.

> `git diff --name-only` — lists only file paths (no patch content).
> `--diff-filter=D` — filters to show only **D**eleted files.
> `--cached` — restricts to the staging area (index).

### Step 2 — Categorize Each Deletion

Group every deleted file into one of the following categories. This
classification drives the risk assessment in the verdict.

| Category | Description | Typical Risk |
|---|---|---|
| **Generated output** | Build artifacts, compiled output, converter results (`.c`, `.h`, `.hex`, `.dcm`, `.class`, `.jar`) | ✅ Low — regenerated on next build/run |
| **Input data** | Source data files consumed by the application (`.nvm`, `.pib`, `.csv`, `.xml` configs) | ⚠️ Medium — may be needed for the app to function |
| **Old snapshot** | Dated or versioned output copies (`out_10_9_2024/`, `v1.2.1/`) | ✅ Low — historical reference only |
| **Pre-refactor reference** | Files kept as "before" comparison (`beforeRefactor/`, `old/`) | ✅ Low — reference only, not used by code |
| **Source code** | `.java`, `.py`, `.ts`, `.js` files in `src/` | ❌ High — may break compilation |
| **Configuration** | `.properties`, `.yml`, `.xml`, `pom.xml`, `build.gradle` | ❌ High — may break build or runtime |
| **Documentation** | `.md`, `.txt`, `.adoc` files | ✅ Low — unless referenced by other docs |

**Grouping rule:** If an entire directory was deleted, treat it as one
group rather than listing every file individually. State the directory
name, file count, and category.

**Example output:**

| # | Group | Files | Category | Risk |
|---|---|---|---|---|
| 1 | `PLCoutput/` | 11 (.c, .h, .hex, .dcm, .txt) | Generated output | ✅ Low |
| 2 | `beforeRefactor/` | 2 (.c, .h) | Pre-refactor reference | ✅ Low |
| 3 | Root `.nvm` files | 6 (mac-release-*-00 to -05.nvm) | Generated output (split NVM) | ✅ Low |
| 4 | `src/com/.../Service.java` | 1 | Source code | ❌ High |

### Step 3 — Scan Source Code for Stale References

Search the **entire** codebase for references to every deleted file and
directory name. This is the critical step — it determines whether a
deletion will break something.

**3.1 — Search for deleted directory names:**

```powershell
# For each deleted directory, search all source files
Get-ChildItem -Recurse -File |
    Where-Object { $_.FullName -notmatch '\\(target|\.git|node_modules|bin)\\' } |
    Select-String -Pattern "deleted_dir_name" |
    Format-Table Filename, LineNumber, Line -AutoSize
```

```bash
grep -rn "deleted_dir_name" \
    --include='*.java' --include='*.xml' --include='*.properties' \
    --include='*.md' --include='*.txt' --include='*.yml' \
    --exclude-dir='{target,.git,node_modules,bin}' .
```

**3.2 — Search for deleted file basenames:**

For individual files (not grouped by directory), search for the exact
filename without path:

```powershell
Select-String -Path (Get-ChildItem -Recurse -File |
    Where-Object { $_.FullName -notmatch '\\(target|\.git)\\' }) `
    -Pattern "deleted_filename\.ext"
```

**3.3 — Classify each match:**

| Match Type | Severity | Action |
|---|---|---|
| Import / require / include statement | ❌ Critical | Deletion will break compilation |
| Hardcoded file path in source code | ❌ Critical | Deletion will cause runtime error |
| Dynamic path construction (user-provided argument) | ✅ Safe | File is an output, not a hardcoded dependency |
| Documentation / comment reference | ⚠️ Low | Update docs but deletion is safe |
| Example command in README | ⚠️ Low | Update example but deletion is safe |

**Decision rule:** If **zero critical matches** are found for a file or
group, the deletion is **safe**. If any critical match exists, flag it
and report the exact file, line number, and matching text.

### Step 4 — Check IDE and Run Configurations

Deleted files referenced in IDE launch/run configurations will cause
silent startup failures. Check all common IDE config locations.

#### 4.1 — Eclipse

```powershell
# Find all Eclipse launch configurations
# Check the project workspace (may be outside repo)
Get-ChildItem -Path "$ECLIPSE_WORKSPACE\.metadata\.plugins\org.eclipse.debug.core\.launches" `
    -Filter "*.launch" -ErrorAction SilentlyContinue |
    ForEach-Object {
        $content = Get-Content $_.FullName -Raw
        Write-Host "=== $($_.Name) ==="
        Write-Host $content
    }
```

> **Where to find the Eclipse workspace path:** Ask the user, or check
> `.project` / `.classpath` files in the repo root for clues. Common
> locations: `C:\Users\<user>\eclipse-workspace\` or a project-specific
> workspace directory.

**What to look for in `.launch` files:**
- `PROGRAM_ARGUMENTS` — check if any argument references a deleted file or directory
- `WORKING_DIRECTORY` — check if it points to a deleted location
- `CLASSPATH` entries — check for deleted JARs or class directories

#### 4.2 — VS Code

```powershell
# Check VS Code launch configuration
$launchJson = ".vscode/launch.json"
if (Test-Path $launchJson) {
    Get-Content $launchJson
}
```

**What to look for in `launch.json`:**
- `args` array — check for deleted file/directory references
- `cwd` — check for deleted working directory
- `program` — check for deleted entry point

#### 4.3 — IntelliJ IDEA

```powershell
# Check IntelliJ run configurations
Get-ChildItem -Path ".idea/runConfigurations" -Filter "*.xml" `
    -ErrorAction SilentlyContinue |
    ForEach-Object { Get-Content $_.FullName }
```

**What to look for in IntelliJ `.xml` configs:**
- `PROGRAM_PARAMETERS` — check for deleted file references
- `WORKING_DIRECTORY` — check for deleted paths
- `MAIN_CLASS_NAME` — check if the main class itself was deleted

#### 4.4 — Verdict on IDE Configs

| Finding | Severity | Action |
|---|---|---|
| Launch config references a deleted **input** file | ⚠️ Medium | Config still works if file is re-supplied at runtime |
| Launch config references a deleted **output** directory | ✅ Safe | App creates output dir on startup (verify `mkdirs()` logic) |
| Launch config references a deleted **source** file | ❌ Critical | Config is broken — must be updated |

### Step 5 — Check .gitignore Coverage

If deleted files were generated artifacts that should never have been
committed, check whether `.gitignore` prevents future accidental commits.

```powershell
# Read current .gitignore
if (Test-Path .gitignore) {
    Get-Content .gitignore
} else {
    Write-Host "WARNING: No .gitignore file exists"
}
```

**For each deleted directory/pattern, check if it is covered:**

| Deleted Path | Pattern Needed | Currently in .gitignore? |
|---|---|---|
| `output/` | `output/` | ❌ No — recommend adding |
| `*.hex` | `*.hex` | ❌ No — recommend adding |
| `target/` | `target/` | ✅ Yes |

**Recommend additions** for any generated artifact patterns that are
missing. Format the recommendation as a ready-to-append block:

```gitignore
# Generated output directories
output/
PLCoutput/
out_put/

# Generated artifacts
*.hex
*.dcm
plc_converter_ref.txt
```

> **Do NOT auto-edit `.gitignore`** — present the recommendation and let
> the user decide. Some projects intentionally track generated artifacts.

### Step 6 — Report Verdict

Present the final verdict as a structured table covering every deleted
file or group. The table is the **deliverable** of this skill.

#### Verdict Table Format

| # | Group / File | Category | Source Refs | IDE Refs | .gitignore | Verdict |
|---|---|---|---|---|---|---|
| 1 | `output/` (11 files) | Generated output | None found | `output` in Eclipse args (safe — auto-created) | ❌ Missing | ✅ Safe to delete |
| 2 | `src/Service.java` | Source code | 3 imports in other files | None | N/A | ❌ DO NOT delete — breaks compilation |

#### Verdict Symbols

| Symbol | Meaning |
|---|---|
| ✅ | Safe — no issues found, deletion is clean |
| ⚠️ | Caution — minor references exist (docs, comments) but no functional impact |
| ❌ | Dangerous — deletion will break builds, runtime, or IDE configurations |

#### Final Summary

After the verdict table, provide a one-paragraph summary:
- Total files deleted
- How many are safe / cautionary / dangerous
- Any recommended `.gitignore` additions
- Any recommended source code or config updates

---

## Edge Cases

### Renamed Files (git mv)

If `git status` shows a file as both deleted and added (with a new name),
it is a **rename**, not a deletion. Verify with:

```powershell
git status -M
```

> `-M` — enables rename detection. Renames show as `renamed:` instead of
> separate `deleted:` + `new file:` entries.

Do NOT flag renames as deletions.

### Files Deleted in Prior Commits

This skill audits **pending** (uncommitted) deletions only. For files
deleted in prior commits, use:

```powershell
git log --diff-filter=D --summary --since="2024-01-01" -- "*.java"
```

> `--diff-filter=D` — shows only commits that deleted files.
> `--summary` — includes the deleted file paths.
> `--since` — limits the time range.

### Binary Files

Binary files (`.nvm`, `.pib`, `.jar`, `.dll`) cannot be grep-searched
for content references. Instead, search for the **filename** across all
text files in the project. The filename is the reference vector, not the
binary content.

### Large Deletions (50+ files)

For bulk deletions, group by directory first, then scan per-directory
rather than per-file. This prevents combinatorial explosion of grep
searches. The categorization table (Step 2) is designed for this — each
row is a group, not an individual file.

---

## Prohibited Behaviors

- **DO NOT** auto-commit or auto-stage deletions — only audit and report
- **DO NOT** skip the IDE config check — silent launch failures are the
  most common post-deletion problem
- **DO NOT** report a file as "safe" without completing the source
  reference scan (Step 3) — assumptions cause breakage
- **DO NOT** ignore binary input files — they may be required test data
  or runtime dependencies
- **DO NOT** truncate the verdict table — every deleted file or group
  must have a row, regardless of how obvious the verdict seems

---

## Environment & Dependencies

This skill requires only Git and a shell. No additional tools need to be
installed.

**Verification:**

```powershell
git --version
```

```bash
git --version
```

If Git is not available, the skill cannot execute. Instruct the user to
install Git via their system package manager:

- **Windows:** `winget install Git.Git`
- **macOS:** `brew install git`
- **Linux (Debian):** `sudo apt install git`
- **Linux (RHEL):** `sudo yum install git`

---

## Related Skills

- [near-duplicate-file-comparison](../near-duplicate-file-comparison/SKILL.md)
  — apply **before** deleting one of two near-duplicate files (e.g.
  `Foo.java` + `Foo_old.java`) to prove which file is canonical and
  capture the rationale. Then use this skill to confirm no stale
  references remain after the deletion.
- [untracked-scratch-triage](../untracked-scratch-triage/SKILL.md)
  — the symmetric counterpart for **untracked** leftovers (this skill
  covers deletions of tracked files; that one covers files that were
  never tracked).
- [git-commit-dangling-link-audit](../git-commit-dangling-link-audit/SKILL.md)
  — complementary: a deleted-by-move link target is the dangling
  subclass — link audit classifies it as DANGLES vs GIT_ONLY.
