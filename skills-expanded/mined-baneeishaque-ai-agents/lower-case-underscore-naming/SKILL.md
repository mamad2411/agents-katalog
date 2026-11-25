---
name: lower-case-underscore-naming
description: Enforce lowercase snake_case naming for all project files, directories, and identifiers — with industry-standard exemptions.
category: Naming & Conventions
---

# Lower Case Underscore Naming Convention Skill

> **Skill ID:** `lower-case-underscore-naming`<br>
> **Version:** 1.2.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Enforce a consistent `lowercase_underscore_based` (snake_case) naming convention across all
project files, directories, artifact identifiers, and internal references.
All file and directory names MUST be in lowercase.
This skill detects violations, classifies exemptions, traces the full
blast radius of each rename, executes renames, updates all cross-references,
and verifies zero stale references remain.

Consistency in naming eliminates cognitive overhead, prevents build-tool
edge cases with special characters, and ensures grep/search reliability
across the entire codebase.

## Prerequisites

| Requirement | Minimum |
|---|---|
| Shell | PowerShell 5.1+ or Bash 4+ |
| VCS | Git (for `git mv` renames) |
| Access | Write access to the project repository |

## When to Apply

Apply this skill when:
- A new project is being initialized and naming conventions must be set
- A user asks to "enforce underscore naming" or "rename to underscore convention"
- A file, directory, or identifier with hyphens, camelCase, or mixed casing is detected
- An artifact ID, module name, or config key uses hyphens instead of underscores
- Pre-commit audit is requested to ensure naming consistency

Do NOT apply when:
- The file is an **industry-standard exempt name** (see Exemptions table below)
- The project explicitly uses a different convention (e.g., kebab-case for npm packages)
- Renaming would break external contracts (published API URLs, package registry names)

---

## Step-by-Step Procedure

### Step 1 — Scan for Violations

Detect all files and directories whose names contain hyphens or other
non-underscore separators.

#### 1a — Identify Tracked Files (Source of Truth)

Always start with `git ls-files` — this is the **authoritative list** of
what the project actually tracks. Do NOT rely on `Get-ChildItem` alone,
which includes git-ignored files and produces false positives.

```powershell
git ls-files
```

#### 1b — Read `.gitignore` Carefully

Before classifying violations, read `.gitignore` to understand which
files are tracked vs ignored. Pay special attention to **negation
patterns** (`!`) that re-include specific files inside ignored directories:

```gitignore
# Example: directory is ignored, but .zip and .md files are tracked
pevers/*
!pevers/*.zip
```

In this case, `pevers/*.zip` files ARE tracked and MUST be audited,
while everything else under `pevers/` is ignored and should be skipped.

#### 1c — Scan Tracked Files for Hyphens

**PowerShell:**
```powershell
git ls-files | Where-Object { $_ -match '-' }
```

**Bash:**
```bash
git ls-files | grep '-'
```

Also scan for untracked directories with hyphens (these won't appear
in `git ls-files` but still need renaming):

```powershell
Get-ChildItem -Directory -Recurse | Where-Object {
    $_.FullName -notmatch '\\(target|\.git|node_modules|dist|build)\\' -and
    $_.Name -match '-'
} | ForEach-Object { $_.FullName }
```

#### 1d — Present Complete Inventory

List **ALL tracked files** (not just violations) with their status.
This gives the user full visibility and prevents missed items:

| # | Tracked File | Has Hyphens? | Action |
|---|---|---|---|
| 1 | `.gitignore` | No | ✅ Exempt (industry-standard) |
| 2 | `my-module/data.zip` | **Parent dir** | 🔄 Moves with parent rename |
| 3 | `some-file.md` | **Yes** | 🔄 Rename |
| … | … | … | … |

### Step 2 — Classify Exemptions

Not every hyphenated name is a violation. The following are
**industry-standard names** that MUST keep their hyphens:

| File / Pattern | Reason |
|---|---|
| `azure-pipelines.yml` | Azure DevOps mandates this exact filename |
| `.gitignore`, `.gitmodules` | Git specification |
| `docker-compose.yml` | Docker Compose specification |
| `package-lock.json` | npm specification |
| `.eslintrc.cjs`, `.prettierrc` | Tool-specific dotfiles |
| `tsconfig.json` | TypeScript specification |
| `pom.xml`, `build.gradle` | Build tool specifications |
| `README.md`, `LICENSE`, `AGENTS.md` | Universal conventions (no hyphens — already compliant) |
| `Makefile`, `Dockerfile` | Tool specifications |
| `.env.*` files | Environment config convention |
| `-rules.md` files in `ai-agent-rules/` | Per `ai-rule-standardization-rules.md` — kebab-case mandated |

**Decision rule:** If a tool, platform, or specification **mandates** the
exact filename, it is exempt. If the name is author-chosen, it MUST use
underscores.

### Step 3 — Trace the Blast Radius

Before renaming anything, find **every reference** to the old name across
the entire codebase. This prevents orphaned links, broken imports, and
stale documentation.

**Use `git ls-files` to search only tracked files** — this avoids false
positives from git-ignored content:

**PowerShell:**
```powershell
git ls-files | ForEach-Object {
    Select-String -Path $_ -Pattern "old-name" -ErrorAction SilentlyContinue
} | Format-Table Filename, LineNumber, Line -AutoSize
```

**Bash:**
```bash
git ls-files | xargs grep -n "old-name" 2>/dev/null
```

**Critical target: `.gitignore`** — This file frequently references
directory names in ignore/negation patterns. When renaming a directory,
`.gitignore` rules referencing that directory MUST be updated or tracked
files inside will become untracked (or vice versa).

Document every match. This is the **blast radius** — every file in this
list must be updated after the rename.

### Step 4 — Rename (Deepest-First)

Rename files and directories using `git mv` to preserve history.
Always rename **deepest paths first** to avoid parent-path invalidation.

```bash
# Directory rename (deepest first)
git mv path/to/old-name path/to/old_name

# File rename
git mv path/to/old-file.ext path/to/old_file.ext
```

**Ordering rule:** If renaming both a directory and files inside it,
rename the **files first**, then the directory. This ensures `git mv`
can locate the files at their current paths.

#### Fallback — Empty Directories

`git mv` fails on empty directories (`fatal: source directory is empty`).
Use `Rename-Item` (PowerShell) or `mv` (Bash) instead:

```powershell
Rename-Item -Path "path/to/old-name" -NewName "old_name"
```

```bash
mv path/to/old-name path/to/old_name
```

Empty directories are not tracked by Git, so no history is lost.

#### Fallback — Locked Directories

If the directory cannot be renamed because it is locked by VS Code,
OneDrive, or another process, use the **mirror-and-remove** strategy:

1. **Remove from VS Code workspace** — if the directory is a workspace
   root folder, remove it first to release file watchers:
   - **File → Remove Folder from Workspace**, or
   - Run VS Code command: `workbench.action.removeRootFolder`
2. **Mirror** the directory to the new name:
   ```powershell
   robocopy "path/to/old-name" "path/to/old_name" /MIR /R:1 /W:1
   ```
3. **Verify** the new directory has identical contents.
4. **Remove contents** of the old directory:
   ```powershell
   Get-ChildItem "path/to/old-name" -Recurse -Force -File |
       Remove-Item -Force -ErrorAction SilentlyContinue
   Get-ChildItem "path/to/old-name" -Recurse -Force -Directory |
       Sort-Object { $_.FullName.Length } -Descending |
       Remove-Item -Force -ErrorAction SilentlyContinue
   ```
5. **Delete the empty shell** — if still locked, instruct the user to
   close VS Code and run manually:
   ```powershell
   rmdir "path/to/old-name"
   ```
6. **Re-add to workspace** — if the directory was a VS Code workspace
   folder, remind the user to re-add the renamed folder via
   **File → Add Folder to Workspace…** or:
   ```powershell
   code --add "path/to/old_name"
   ```

### Step 5 — Update All Cross-References

Using the blast radius from Step 3, update every reference to the old
name in all affected files:

- **`.gitignore` / `.gitattributes`**: Directory ignore patterns and negation rules — **critical**, or tracked files become untracked
- **Documentation** (`.md` files): Links, titles, inline references
- **Build configs** (`pom.xml`, `build.gradle`, `package.json`): Artifact IDs, module names
- **CI/CD** (`azure-pipelines.yml`, `.github/workflows/`): Artifact references, paths
- **IDE configs** (`.project`, `.classpath`, `.idea/`): Project names, module paths
- **Source code**: Import statements, string literals, constants
- **Agent skills** (`SKILL.md`, `AGENTS.md`): Skill IDs, references, templates

**Critical:** Artifact identifiers (Maven `<artifactId>`, npm package `name`,
Gradle `rootProject.name`) are first-class rename targets — not just filenames.

### Step 6 — Verify Zero Stale References

After all renames and updates, verify that **zero** references to the old
name remain:

**PowerShell:**
```powershell
git ls-files | ForEach-Object {
    Select-String -Path $_ -Pattern "old-name" -ErrorAction SilentlyContinue
} | Format-Table Filename, LineNumber, Line -AutoSize
```

**Bash:**
```bash
git ls-files | xargs grep -n "old-name" 2>/dev/null
```

**Expected result:** No output. If matches appear, return to Step 5.

Also verify the final tracked file list is fully compliant:

```powershell
git ls-files | Where-Object { $_ -match '-' }
```

**Expected result:** Only industry-standard exempt names (e.g.,
`azure-pipelines.yml`). Author-chosen names must have zero hyphens.

**Exception:** The workspace folder name itself (e.g., `my-project`
as a parent directory) is NOT a violation — it exists outside the project's
controlled scope.

---

## Scope Coverage

The naming convention applies to these categories:

| Category | Convention | Example |
|---|---|---|
| Files (author-chosen) | `snake_case` | `tul_api_reference.md` |
| Directories (author-chosen) | `snake_case` | `tul_logging/` |
| Maven `<artifactId>` | `snake_case` | `tul_logging` |
| Gradle `rootProject.name` | `snake_case` | `tul_logging` |
| Skill IDs | `snake_case` | `lower_case_underscore_naming` |
| Template files | `snake_case` + `.tpl` | `integration_snippet.java.tpl` |
| Config keys (author-chosen) | `snake_case` or `dot.notation` | `tul.server.url` |

---

## Prohibited Behaviors

The agent is **BLOCKED** from:

- **Renaming industry-standard files** — `azure-pipelines.yml`, `docker-compose.yml`, `package-lock.json`, etc. (see Exemptions table)
- **Renaming without tracing blast radius** — Every rename MUST be preceded by a full-codebase grep
- **Partial updates** — If a rename has 10 references, ALL 10 must be updated atomically. Leaving stale references is forbidden
- **Renaming external contract names** — Published package names, public API URLs, or registry-registered identifiers without explicit user approval
- **Renaming files in `ai-agent-rules/`** — These follow kebab-case per `ai-rule-standardization-rules.md`
- **Guessing references** — If the blast radius search returns unexpected results, the agent MUST pause and confirm with the user before proceeding
- **Skipping verification** — Step 6 (zero stale references) is mandatory. Never assume the rename is complete without running the verification command

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| Renamed file but forgot Maven `<artifactId>` | Artifact IDs are first-class targets — always include in blast radius search |
| Renamed directory but child paths broke | Rename deepest-first; for `git mv`, rename the directory in one operation |
| Eclipse `.project` still has old name | IDE configs (`.project`, `.classpath`, `.idea/`) must be updated |
| CI/CD pipeline references old artifact glob | Search CI configs (`*-pipelines.yml`, `*.yml` in `.github/`) for old name |
| Documentation links broken after rename | Run blast radius search on the **new** name after rename to verify link targets exist |
| Renamed a tool-mandated filename | Check the Exemptions table first — some hyphens are mandatory |
| `ai-agent-rules/` files renamed to underscores | These files follow kebab-case per their own standardization rules — exempt |
| Directory locked by VS Code / OneDrive | Use `robocopy /MIR` fallback: mirror → remove contents → user deletes empty shell after closing VS Code |
| Renamed folder disappeared from VS Code workspace | After renaming a workspace root folder, re-add it via **File → Add Folder to Workspace…** or `code --add` |
| Scanned with `Get-ChildItem` and got false positives | Use `git ls-files` as the source of truth — it shows only tracked files, skipping git-ignored content |
| Missed `.gitignore` references to renamed directory | `.gitignore` patterns referencing old directory names MUST be updated — otherwise tracked files become untracked |
| `.gitignore` negation patterns (`!`) missed | Read `.gitignore` carefully — `!dir/*.zip` means those zips ARE tracked even though `dir/*` is ignored |
| `git mv` failed on empty directory | Empty dirs aren't tracked by Git — use `Rename-Item` (PowerShell) or `mv` (Bash) instead |
| Only listed violations, not all tracked files | Present a **complete inventory** of ALL tracked files with their status — users need full visibility |
