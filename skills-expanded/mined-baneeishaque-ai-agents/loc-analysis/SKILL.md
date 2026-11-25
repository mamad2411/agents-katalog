---
name: loc-analysis
description: Calculate lines of code added, deleted, and modified — comparing two codebases or analyzing git history within a scoped feature.
category: Metrics & Reporting
---

# LOC Analysis Skill

> **Skill ID:** `loc-analysis`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Calculate lines of code (LOC) added, deleted, and modified across a
project transformation or feature integration. This skill supports two
analysis modes:

1. **Baseline Comparison** — Compare an original codebase (directory or
   repo) against a derived codebase to measure the full delta. Used for
   library extraction, refactoring, or project restructuring.

2. **Git Commit Analysis** — Analyze commits in a date range within a
   single repository, classify each changed file as in-scope or
   out-of-scope for a given feature, and compute scoped LOC. Used for
   measuring the footprint of a specific feature integration.

Both modes produce classified, detailed tables with per-file granularity,
category subtotals, and a grand summary.

## Prerequisites

| Requirement | Minimum |
|---|---|
| VCS | Git 2.x+ |
| Shell | PowerShell 5.1+ or Bash 4+ |
| Access | Read access to both codebases (Mode A) or the repository (Mode B) |

## When to Apply

Apply this skill when:

- A user asks to "calculate LOC", "count lines", or "measure code changes"
- A library has been extracted from an application and the user wants
  to quantify the transformation
- A feature was integrated into a project and the user wants its LOC
  footprint isolated from unrelated changes
- A user asks "how many lines did we add/delete/modify?"
- A release note or report needs quantified LOC metrics

Do NOT apply when:

- The user wants a simple `wc -l` on a single file (just run it directly)
- The user wants code complexity metrics (cyclomatic complexity, etc.)
  — that is a different analysis
- The user wants test coverage — that requires a test runner, not LOC

---

## Mode A — Baseline Comparison

Use when comparing two distinct codebases: an **original** (source) and a
**derived** (target) that was created from it.

### Step A1 — Identify the Scope

Determine which files in the original belong to the scope being analyzed.
**Not all files in the original may be relevant.**

Ask the user:

- Which files/directories in the original are **in-scope** (part of the
  library or module being measured)?
- Which files are **excluded** (application-specific code that was not
  carried over by design)?

**Critical:** Do not assume. A file that looks application-specific
(e.g., `RteConfigGenerator.java`) may have contributed to derived
artifacts (templates, examples, documentation). Verify by checking
whether any new-project file was **derived from** the excluded file.

**Verification command:**
```powershell
# Check if any new file references or resembles the "excluded" file
Select-String -Path "<new_project>\**\*" -Pattern "<excluded_file_name>" -Recurse
```

If a supposedly-excluded file contributed content to the new project,
it MUST be included in the baseline.

### Step A2 — Enumerate VCS-Tracked Files

List all VCS-tracked files in both codebases. Only tracked files count.

**Original:**
```powershell
cd "<original_repo>"
git ls-files
```

**Derived:**
```powershell
cd "<derived_repo>"
git ls-files
```

### Step A3 — Count Lines Per File

For every tracked file in both codebases, count lines. Use
`Measure-Object -Line` for text files. Identify binary files separately.

```powershell
git ls-files | ForEach-Object {
    $fp = Join-Path (Get-Location) $_
    $isBin = $_ -match "\.(jar|zip|exe|png|dll|class|war|ear|nvm|pib)$"
    if ($isBin) {
        $sz = (Get-Item $fp).Length
        Write-Host "$_ : binary ($sz bytes)"
    } else {
        $l = (Get-Content $fp | Measure-Object -Line).Lines
        Write-Host "$_ : $l lines"
    }
}
```

### Step A4 — Map File Pairs

Identify which files exist in both codebases (modified), which exist
only in the original (deleted), and which exist only in the derived
(added).

Files may have been **renamed** (e.g., `RteconfgenTULConstants.java` →
`TULConfig.java`). The agent MUST ask the user or infer from content
similarity which files are renamed counterparts.

Classification:

| Status | Definition |
|---|---|
| **Modified** | File exists in both (possibly renamed); content changed |
| **Deleted** | File exists only in original; removed or split into other files |
| **Added** | File exists only in derived; entirely new |
| **Binary** | Non-text file; report size only, not lines |

### Step A5 — Compute Diffs for Modified Files

For each modified file pair, use `git diff --no-index --numstat` to get
precise insertions and deletions:

```powershell
git diff --no-index --numstat "<original_file>" "<derived_file>"
```

This outputs: `<insertions>\t<deletions>\t<filepath>`

### Step A6 — Classify Added Files by Category

Group all added files into meaningful categories. Common categories:

| Category | Examples |
|---|---|
| Java Source | `.java` files |
| AI Agent Skill | `.agents/skills/**` (SKILL.md, templates, references, examples) |
| Build & CI | `pom.xml`, `build.gradle`, `azure-pipelines.yml`, `jitpack.yml` |
| Eclipse Project | `.classpath`, `.project`, `.settings/*` |
| Documentation | `README.md`, `AGENTS.md`, `docs/*.md` |
| VCS Config | `.gitignore`, `.gitattributes` |
| Configuration | `*.properties`, `*.yml` (non-CI) |

### Step A7 — Produce Output Tables

Generate the following tables (see Output Template section below):

1. **Excluded Files** — files deliberately excluded from scope
2. **Original Baseline** — all in-scope files with line counts
3. **Modified Files** — per-file old LOC, new LOC, insertions, deletions, delta
4. **Deleted Files** — files removed with line counts
5. **Added Files** — grouped by category with line counts
6. **Grand Summary** — total lines added, deleted, net change
7. **Project Size Comparison** — file count and LOC before/after

---

## Mode B — Git Commit Analysis

Use when measuring the LOC footprint of a **specific feature** within a
single repository's commit history.

### Step B1 — Identify the Baseline Commit

Find the last commit before the feature work began:

```powershell
cd "<repo>"
git log --oneline --before="<feature_start_date>" -1
```

This is the **baseline commit**.

### Step B2 — List All Commits in Scope

```powershell
git log --oneline --since="<start_date>" --until="<end_date>"
```

### Step B3 — Classify Each Commit

For each commit, examine the files changed and classify the commit:

```powershell
git log --oneline --stat <baseline>..<head>
```

Classification per commit:

| Label | Meaning |
|---|---|
| ✅ Full | All changes are feature-related |
| ✅ Partial | Some changes are feature-related, some are not |
| ❌ No | No changes are feature-related |

### Step B4 — Get the Cumulative Diff

```powershell
git diff --numstat <baseline_commit> HEAD
```

### Step B5 — Classify Each Changed File

For every file in the cumulative diff, determine whether the change is
**feature-related** or **unrelated**.

**For modified files** (exist in both baseline and HEAD), inspect the
actual diff to identify feature-specific lines:

```powershell
git diff <baseline> HEAD -- <filepath>
```

Count feature-related added lines by searching for feature-specific
patterns (imports, API calls, comments):

```powershell
$diff = git diff <baseline> HEAD -- <filepath>
$added = ($diff -split "`n") | Where-Object { $_ -match "^\+" -and $_ -notmatch "^\+\+\+" }
$featureAdded = $added | Where-Object { $_ -match "<feature_keyword>" }
Write-Host "Total added: $($added.Count)"
Write-Host "Feature added: $($featureAdded.Count)"
```

**For new files**, determine if the entire file is feature-dedicated or
if it is a shared file with partial feature content.

**For deleted files**, determine if the deletion was caused by the feature
work or by unrelated cleanup.

### Step B6 — Handle Partial Files

Some files are **shared** — they contain both feature-related and
unrelated content (e.g., `README.md` with a TUL section among other
sections). For these:

1. Report the **total lines** in the file
2. Report the **feature-related lines** specifically
3. Report the **non-feature lines** as context

### Step B7 — Identify Non-Feature Changes

Explicitly list all changes that are **not** part of the feature scope.
This provides transparency and prevents inflated metrics.

Common non-feature changes that appear in the same period:

- Generated output files committed/deleted
- Project restructuring (file moves/renames)
- Unrelated bug fixes
- Historical release notes
- Cleanup of old directories

### Step B8 — Produce Output Tables

Generate the following tables (see Output Template section below):

1. **Commit Log** — every commit with hash, message, and TUL/feature classification
2. **Feature-Dedicated New Files** — grouped by category
3. **Feature Integration in Existing Files** — per-file with per-line detail
4. **Feature Mentions in Documentation** — partial content in shared docs
5. **Non-Feature Changes** — explicitly listed and excluded
6. **Grand Summary** — total feature lines added, deleted, net change

---

## Output Template

### Excluded Files Table

```markdown
| File | Lines | Reason |
|---|---:|---|
| `ExcludedFile.java` | 1,674 | Application code, not part of library |
```

### Baseline Table

```markdown
| # | Category | File | Lines |
|---|---|---|---:|
| 1 | Java Source | `path/to/File.java` | 114 |
| | | **Baseline Total** | **N** |
```

### Modified Files Table

```markdown
| # | Original File | New File | Old LOC | New LOC | Ins (+) | Del (−) | Δ |
|---|---|---|---:|---:|---:|---:|---:|
| 1 | `OldName.java` | `NewName.java` | 861 | 236 | 240 | 997 | −625 |
| | | **Subtotal** | **X** | **Y** | **A** | **B** | **C** |
```

### Deleted Files Table

```markdown
| # | Category | File | Lines Deleted |
|---|---|---|---:|
| 1 | Java Source | `path/to/Removed.java` | 185 |
| | | **Subtotal** | **N** |
```

### Added Files Table (grouped by category)

```markdown
### Category Name

| # | File | Lines |
|---|---|---:|
| 1 | `path/to/NewFile.java` | 220 |
| | **Subtotal** | **N** |
```

### Grand Summary Table

```markdown
| Metric | Source | Lines |
|---|---|---:|
| **Lines Added** | | **N** |
| — Modified files | Section X | A |
| — New files: Category 1 | Section Y | B |
| **Lines Deleted** | | **M** |
| — Modified files | Section X | C |
| — Deleted files | Section Z | D |
| **Net Change** | | **±K** |
```

### Project Size Comparison Table

```markdown
| Metric | Original | New | Change |
|---|---:|---:|---|
| VCS-tracked files | X | Y | ±N |
| Source LOC | A | B | ±C (±P%) |
| Total VCS-tracked LOC | D | E | ±F (±Q%) |
```

### Commit Log Table (Mode B only)

```markdown
| # | Commit | Message | Feature? | Description |
|---|---|---|---|---|
| 1 | `abc1234` | feat: add TUL | ✅ Full | TUL logger and constants |
| 2 | `def5678` | cleanup | ❌ No | Deleted old outputs |
```

### Integration Lines Table (Mode B only)

For files where only **some** lines are feature-related, list each
feature line individually:

```markdown
| # | Line | Code | Purpose |
|---|---|---|---|
| 1 | import | `import ...TULLogger;` | Import |
| 2 | init | `TULLogger logger = TULLogger.getInstance();` | Singleton init |
| | | **Feature lines added** | **N** |
```

---

## Prohibited Behaviors

The agent is **BLOCKED** from:

- **Counting generated output files** — Build artifacts, compiled
  `.class` files, generated `.c`/`.h` outputs, `.hex` files, etc. are
  NOT source code. They MUST be excluded or listed separately as
  non-feature changes.

- **Counting binary files as LOC** — `.jar`, `.zip`, `.exe`, `.png`,
  `.nvm`, `.pib` files have no line count. Report size in bytes/KB/MB
  only.

- **Assuming file scope without verification** — If a file looks
  application-specific but might have contributed to derived work
  (templates, examples), the agent MUST verify before excluding it.

- **Inflating metrics with unrelated changes** — In Mode B, changes
  that happened in the same time period but are unrelated to the feature
  (restructuring, cleanup, unrelated bug fixes) MUST be explicitly
  separated and excluded from feature LOC.

- **Counting file renames as additions + deletions** — A `git mv` is a
  rename, not an addition and deletion. If the content is unchanged, the
  LOC delta is zero.

- **Omitting deleted files from the baseline** — Files that were deleted
  as part of the transformation still contribute to the "lines deleted"
  metric. They must be counted.

- **Double-counting partial documentation** — If `README.md` has 11
  feature-related lines out of 193 total, count **11** for the feature
  — not 193.

- **Skipping non-feature changes table** — Transparency requires that
  excluded changes are explicitly listed with rationale, not silently
  dropped.

- **Using `Measure-Object -Line` and `.Count` interchangeably without
  noting the difference** — `Measure-Object -Line` counts non-empty
  lines; `.Count` counts all lines including blanks. Pick one method
  and use it consistently. When comparing with `git diff --numstat`,
  use `.Count` (total lines) for consistency, since git counts all lines.

---

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| Generated output committed to VCS inflates LOC | Exclude `output/`, `dist/`, `build/`, `target/` — list in non-feature table |
| Renamed file counted as add + delete | Use `git diff --no-index` between old and new file to get true delta |
| Excluded file actually contributed to templates | Verify with `Select-String` — if content was derived, include in baseline |
| Binary JARs counted as LOC | Detect with extension regex; report size only |
| `Measure-Object -Line` vs `.Count` mismatch | Use `.Count` consistently when comparing with git numstat |
| Cleanup commits mixed with feature commits | Classify each commit individually; separate scoped vs unscoped |
| Feature lines in shared docs over-counted | Count only feature-specific lines, not the entire file |
| Old output dirs deleted inflate "lines deleted" | These are generated files — list under non-feature changes |
| Forgot to check `.classpath` / `.gitignore` for feature lines | These config files often have 1–3 feature-related lines mixed in |
| Baseline did not include all contributing files | Ask the user explicitly which original files are in-scope vs excluded |

---

## Checklist

Before finalizing the analysis, verify:

- [ ] All VCS-tracked files enumerated (`git ls-files`)
- [ ] Excluded files justified and verified (no derived content missed)
- [ ] Binary files reported as size, not LOC
- [ ] Modified file pairs correctly identified (including renames)
- [ ] `git diff --no-index --numstat` used for modified file diffs
- [ ] Added files classified by category
- [ ] Deleted files counted with line totals
- [ ] Grand summary adds up (subtotals = total)
- [ ] Non-feature changes explicitly listed (Mode B)
- [ ] Feature lines in shared docs counted individually (Mode B)
- [ ] Consistent line-counting method used throughout
- [ ] Output written to `docs/loc_analysis.md` (or user-specified path)
