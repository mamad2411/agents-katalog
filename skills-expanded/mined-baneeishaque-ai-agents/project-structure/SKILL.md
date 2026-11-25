---
name: project-structure
description: Industrial-standard project folder structure, root hygiene, README conventions, and documentation placement rules.
category: Project Organization
---

# Project Structure & Documentation Skill

> **Skill ID:** `project-structure`<br>
> **Version:** 1.1.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## Description

Audit and organize any project to follow industrial-standard conventions
for folder structure, root-level file hygiene, documentation placement,
and mandatory project files. This skill classifies every file as either
tool-mandated (fixed location) or author-chosen (movable), then relocates
misplaced artifacts, establishes standard directories, and ensures
`README.md` and `AGENTS.md` follow proven patterns.

Clean project structure eliminates onboarding friction, enables IDE/tool
auto-discovery, and makes the codebase navigable at a glance.

## Prerequisites

| Requirement | Minimum |
|---|---|
| Shell | PowerShell 5.1+ or Bash 4+ |
| VCS | Git (for `git mv` renames) |
| Access | Write access to the project repository |

## When to Apply

Apply this skill when:
- A new project is being initialized from scratch
- A user asks to "organize the project" or "fix the folder structure"
- Design documents, plans, or internal docs are found in the project root
- CI/CD configs for non-active platforms clutter the root
- The project has no `README.md`
- `AGENTS.md` duplicates content from `README.md` or `SKILL.md`
- Root contains files that belong in subdirectories

Do NOT apply when:
- The project is a monorepo with its own established conventions
- A framework mandates a specific structure (e.g., Next.js `app/`, Rails `app/models/`)
- The user explicitly prefers a flat structure

---

## Step-by-Step Procedure

### Step 1 — Audit Root Directory

List every file and directory in the project root and classify each one:

#### 1a — Discover Root Contents

```powershell
Get-ChildItem -Path . -Force | Select-Object Name, Mode |
    Sort-Object Mode, Name
```

Classify each item against the **Root File Classification Table** (below).
Any file that is NOT in the "belongs in root" list is a candidate for
relocation.

### Step 2 — Establish Standard Directories

Create the standard directory structure. Only create directories that the
project actually needs — do not create empty placeholder dirs.

```
project_root/
├── src/              # Source code (language-specific subtree)
├── docs/             # Design docs, plans, ADRs, internal documentation
├── ci/               # Dormant or reference CI/CD configs (not auto-detected)
├── tools/            # Third-party executables invoked at runtime
├── packaging/        # Build scripts, launcher scripts, packaging resources
├── samples/          # Sample / test-data files for development use
├── releases/         # Release zips and release notes (versioned artifacts)
├── .launches/        # IDE shared launch configurations (Eclipse)
├── .agents/          # AI agent skills (agentskills.io standard)
│   └── skills/
│       └── {skill_name}/
│           ├── SKILL.md
│           ├── templates/
│           ├── references/
│           └── examples/
├── .settings/        # IDE-specific settings (Eclipse, IntelliJ via .idea/)
└── test/             # Test code (if not co-located with src/)
```

**Do NOT create:**
- `docs/` if there are no documents to put in it
- `ci/` if all CI configs are in their auto-detect locations
- `test/` if tests live inside `src/` (Maven/Gradle convention)
- `tools/` if the project has no runtime executables
- `packaging/` if build scripts live in root by convention (e.g., `Makefile`)
- `samples/` if there are no sample/test-data files
- `releases/` if the project uses a CI/CD pipeline for release artifacts
- `.launches/` if the project does not track shared launch configurations

### Step 3 — Relocate Misplaced Files

Move files that do not belong in root to their correct directory.
Use `git mv` to preserve history.

**Common relocations:**

| File Pattern | From | To | Rationale |
|---|---|---|---|
| `implementation_plan*.md` | root | `docs/` | Internal design documentation |
| `architecture*.md` | root | `docs/` | Internal design documentation |
| `*-pipelines.yml` (dormant) | root | `ci/` | Not auto-detected; reference only |
| `ADR-*.md` | root | `docs/adr/` | Architecture Decision Records |
| `design_*.md` | root | `docs/` | Design artifacts |
| `*.exe`, `*.bin` (runtime) | root | `tools/` | Runtime executables invoked by application |
| `*.nvm`, `*.pib`, `*.hex` (samples) | root | `samples/` | Test/sample data not shipped in release |
| `*.xml` (Ant/build scripts) | root | `packaging/` | Build scripts (unless tool-mandated in root) |
| `*.cmd`, `*.sh` (launcher) | root | `packaging/` | End-user launcher scripts for packaging |
| `*.launch` (Eclipse) | workspace `.metadata` | `.launches/` | Shared launch configs tracked in VCS |
| UML diagrams, PNG/SVG docs | root | `docs/` | Visual documentation artifacts |

#### Recovering Eclipse Launch Configurations

Eclipse stores launch configs in the workspace `.metadata` directory,
not in the project. To share them in VCS:

1. **Locate the workspace** — check the Eclipse installation's
   `configuration/.settings/org.eclipse.ui.ide.prefs` or find the
   workspace path from Eclipse → Window → Preferences → General → Startup.
2. **Find launch files:**
   ```powershell
   Get-ChildItem "<workspace>/.metadata/.plugins/org.eclipse.debug.core/.launches" -Filter "*.launch"
   ```
3. **Copy** (not move) matching `.launch` files to `.launches/` in the
   project root.
4. **Add gitignore exceptions** for `!.launches/` and `!.launches/*.launch`
   (since `*.launch` is typically in the global ignore rules).

**Ordering:** Move deepest paths first to avoid parent-path invalidation.

#### Audit References After Relocation

```powershell
Get-ChildItem -Recurse -File |
    Where-Object { $_.FullName -notmatch '\\(target|\.git)\\' } |
    Select-String -Pattern "old_filename" |
    Format-Table Filename, LineNumber, Line -AutoSize
```

#### Source Code Updates After Executable Moves

When executables (e.g., `.exe` files) are moved to `tools/`, search
for `ProcessBuilder`, `Runtime.exec()`, or hardcoded command strings
in Java/C#/Python source that reference the old location. Update them
to use relative paths from the new location:

```java
// Before (root-relative)
new ProcessBuilder("nvmsplit.exe", ...)

// After (tools/ subfolder)
new ProcessBuilder(Paths.get("tools", "nvmsplit.exe").toString(), ...)
```

Also update the release/packaging build scripts so the distribution
zip mirrors the new directory layout.

#### Gitignore Rule Placement & Exceptions

All project-specific rules and exceptions MUST go at the **bottom** of
`.gitignore`, after the auto-generated block (e.g., gitignore.io).
Use a clear section header:

```gitignore
# End of https://www.toptal.com/developers/gitignore/api/...

# ── Project-specific ──────────────────────────────────────────
dist/
releases/*/
!.launches/
!.launches/*.launch
!packaging/jar-in-jar-loader.zip
!releases/RELEASE_NOTES_*.md
!releases/*.zip
```

**Key rules:**
- `dist/` (or equivalent build output dir) — project-specific ignore,
  not typically in generated templates.
- `releases/*/` — ignore exploded build directories but NOT the
  release zips or release notes at the `releases/` top level.
- Negation patterns (`!`) must come after the broader rules they
  override.

**Always verify** with `git status` that the moved files are tracked,
not silently ignored.

### Step 4 — Audit / Create README.md

Every project MUST have a `README.md` in root. It is the first file
anyone reads — on GitHub, GitLab, or any file browser.

#### Migrating an Existing Readme.txt

If the project already has a `Readme.txt` (or similar), do NOT discard
its contents. The old readme is the **voice of the original author** and
often reflects the end-user experience accurately:

1. **Read the old readme** — identify what it covers (usage, modes,
   examples, distribution path).
2. **Rename** `Readme.txt` → `README.md` using `git mv`.
3. **Rewrite in Markdown** — preserve all original content, distributing
   it into the mandatory sections below. Every fact in the old readme
   must appear in the new one.
4. **Verify coverage** — diff the old and new to ensure nothing is lost.

#### Mandatory Sections

All sections below are required. The **recommended order** is shown,
but **Quick Start may be promoted to position 3** for CLI tools and
end-user applications where usage is more important than internals.

| # | Section | Purpose |
|---|---|---|
| 1 | `# Project Name` | H1 title — short, clear |
| 2 | Description paragraph | 2–3 sentences: what it does, who it's for |
| 3 | `## Quick Start` | Command / usage snippet — first thing users need |
| 4 | `## Requirements` | Table of minimum versions (Java, Node, Python, etc.) |
| 5 | `## Features` | Bullet list of key capabilities |
| 6 | `## Configuration` | Key config options (table or brief description) |
| 7 | `## Building from Source` | Exact commands to build/test |
| 8 | `## Project Structure` | Annotated directory tree (only top 2 levels) |
| 9 | `## Release Notes` | Table linking to `releases/RELEASE_NOTES_*.md` |
| 10 | `## Documentation` | Table of links to all docs (SKILL.md, API ref, design docs) |
| 11 | `## License` | License name + link |
| 12 | `## Maintainer` | Name and contact (derived from `git config`) |

#### README Section Content Guidelines

- **Quick Start** — for tools distributed via a corporate distribution
  system (e.g., toolbase), the primary Quick Start should show the
  end-user invocation from the distribution path. A developer-facing
  "run from source" command belongs in **Building from Source** instead.
- **Requirements** — list only what end-users need (e.g., Java). All
  runtime dependencies are bundled with the distribution.
- **Configuration** — if the tool works out of the box with no user
  configuration, state that explicitly (e.g., "TUL logging is
  pre-configured and works out of the box on the corporate network.
  No user configuration is required.").
- **Building from Source** — this is the developer section. Include:
  library JAR versions (from `libs/`), IDE setup (Eclipse `.classpath`
  notes), Ant/Maven commands, and compile-from-CLI commands. Note that
  build tool paths (e.g., Ant bundled with Eclipse) are machine-specific
  and should use a variable or instructions to locate them.
- **Samples** — mention that sample files exist in `samples/` for
  development use but are NOT shipped in the release distribution.

#### README Rules

- **Zero duplication with AGENTS.md** — README is for humans; AGENTS.md is for AI agents
- **No internal implementation details** — those go in `docs/`
- **Code examples must be copy-pasteable** — complete, not truncated
- **Links use relative paths** — portable across forks and clones
- **Configuration table** references the source code defaults — not invented values

### Step 5 — Audit / Create AGENTS.md

This project uses a three-file AGENTS.md architecture:

| File | Role | Content |
|------|------|---------|
| `AGENTS.md` | Permanent Operating Reminders (all tools) | SSOT for common reminders |
| `AGENTS-legacy.md` | Skills table for legacy runtimes | One row per skill with path and trigger |
| `AGENTS-github-copilot.md` | Copilot-specific instructions (delta only) | Tool-specific; references `AGENTS.md` |

Each file MUST NOT duplicate content from the others.

`AGENTS.md` is a **thin bridge** for AI agent discovery. It MUST NOT
duplicate content from `README.md` or `SKILL.md`.

#### Template (AGENTS-legacy.md)

```markdown
# AGENTS-legacy.md — Legacy Skills Table

For common Permanent Operating Reminders that apply to all tools,
see [AGENTS.md](AGENTS.md).

## Skills

| Skill | Path | When to use |
|---|---|---|
| Skill Name | [`.agents/skills/skill-name/SKILL.md`](.agents/skills/skill-name/SKILL.md) | One-line trigger description |

## Conventions

- Convention 1 (e.g., "Underscore naming for files and directories")
- Convention 2
- See [README.md](README.md) for build commands and project overview
```

#### AGENTS.md Rules

- **Maximum ~15 lines** — it is a routing table, not documentation
- **Skills table** — one row per skill, with relative path and trigger
- **Conventions** — 3–5 bullet points of project-wide rules
- **Defer to README** — link to it for build commands, structure, etc.
- **Defer to SKILL.md** — link to it for procedures, templates, etc.
- **Zero duplicated tables** — if a table exists in SKILL.md or README, do not copy it here
- **Zero duplication across the three AGENTS.* files** — AGENTS.md is SSOT for common reminders; AGENTS-legacy.md and AGENTS-github-copilot.md are delta-only, each pointing back to AGENTS.md

### Step 6 — Audit CI/CD Placement

CI/CD config files have two categories:

| Category | Location | Examples |
|---|---|---|
| **Auto-detected** (active) | Tool-mandated location in root | `.github/workflows/*.yml`, `azure-pipelines.yml`, `.gitlab-ci.yml`, `Jenkinsfile` |
| **Dormant / reference** | `ci/` directory | Pipelines for platforms you're not actively using |

**Decision rule:**
- If the project uses Azure DevOps → `azure-pipelines.yml` stays in root
- If the project pushes to GitHub but has an `azure-pipelines.yml` → move to `ci/`
- If the project has configs for multiple CI platforms → active one in root, others in `ci/`

**After moving**, update any documentation that references the old path.

### Step 7 — Release Engineering

If the project produces distributable artifacts (JAR, zip, installer):

1. **Create a `releases/` directory** for release zips and release notes.
2. **Create or update the build script** (Ant, Maven, Gradle, Makefile)
   with a `release` target that produces a versioned zip matching the
   existing distribution layout. Note: build tool paths (e.g.,
   `<tools-root>/eclipse/plugins/org.apache.ant_*/bin/ant.bat`) are
   machine-specific — use path variables or document how to locate them.
   **Do NOT include sample/test-data files** in the release zip —
   samples stay in `samples/` for development only.
3. **Write release notes** as `releases/RELEASE_NOTES_<version>.md`.
   Each release note should include: What's New, Available Modes/Features,
   Distribution Layout, Dependencies Added (if any), Requirements.
4. **Version constants** — search for hardcoded version strings in source
   code (e.g., `TOOL_VERSION = "1.2.1"`) and update them to match the
   release version.
5. **Bundle all dependencies** — verify the release artifact includes
   all runtime JARs. Test with a clean directory outside the source tree.
6. **Gitignore exceptions** — whitelist `releases/*.zip` and
   `releases/RELEASE_NOTES_*.md`; ignore exploded build dirs with
   `releases/*/`.

**Test the release** by extracting the zip to a temp directory and
running the application from there. Common failures:
- `NoClassDefFoundError` — a dependency JAR is missing from the bundle
- `FileSystemNotFoundException` — classpath URI schemes (e.g., `rsrc:`)
  not handled when running from a fat JAR
- Hardcoded absolute paths — should be relative to working directory

### Step 8 — Verify

After all changes, verify the root is clean and all links work:

```powershell
# List root — should be only convention files
Get-ChildItem -Path . -Force -Name | Sort-Object

# Check for broken relative links in markdown
Get-ChildItem -Recurse -Filter "*.md" |
    Where-Object { $_.FullName -notmatch '\\(target|\.git)\\' } |
    Select-String -Pattern "\[.*\]\(((?!http)[^)]+)\)" |
    ForEach-Object {
        $link = $_.Matches[0].Groups[1].Value
        $dir = Split-Path $_.Path
        $target = Join-Path $dir $link
        if (-not (Test-Path $target)) {
            [PSCustomObject]@{File=$_.Filename; Line=$_.LineNumber; BrokenLink=$link}
        }
    } | Format-Table -AutoSize
```

**Expected root contents** (typical Java/Maven project):

```
.agents/          # AI agent skills
.classpath        # IDE (if tracked)
.gitignore        # Git
.project          # IDE (if tracked)
.settings/        # IDE (if tracked)
AGENTS.md         # Agent bridge
ci/               # Dormant CI configs (if any)
docs/             # Design documentation
jitpack.yml       # JitPack config (if applicable)
pom.xml           # Maven build
README.md         # Human entry point
src/              # Source code
```

**Expected root contents** (Eclipse/Ant project without Maven):

```
.classpath        # Eclipse build path
.gitignore        # Git
.launches/        # Shared launch configurations
.project          # Eclipse project descriptor
AGENTS.md         # Agent bridge
docs/             # Design documentation
libs/             # Runtime JAR dependencies
packaging/        # Ant build file, launcher, packaging resources
README.md         # Human entry point
releases/         # Release zips and release notes
samples/          # Test data for development
src/              # Source code
tools/            # Runtime executables (exe, sh)
```

---

## Root File Classification Table (SSOT)

Files that **belong in root** (tool-mandated or universal convention):

| File | Reason | Movable? |
|---|---|---|
| `README.md` | Universal convention — first file read | No |
| `AGENTS.md` | Agent discovery convention | No |
| `LICENSE` | Universal convention | No |
| `CHANGELOG.md` | Universal convention | No |
| `.gitignore` | Git specification | No |
| `.gitmodules` | Git specification | No |
| `pom.xml` | Maven specification | No |
| `build.gradle` / `build.gradle.kts` | Gradle specification | No |
| `package.json` | npm/Node specification | No |
| `Cargo.toml` | Rust specification | No |
| `go.mod` | Go specification | No |
| `Makefile` | Make specification | No |
| `Dockerfile` | Docker specification | No |
| `docker-compose.yml` | Docker Compose specification | No |
| `.classpath`, `.project` | Eclipse IDE (if tracked) | No |
| `azure-pipelines.yml` | Azure DevOps auto-detect (only if active) | `ci/` if dormant |
| `.gitlab-ci.yml` | GitLab auto-detect (only if active) | `ci/` if dormant |
| `Jenkinsfile` | Jenkins auto-detect (only if active) | `ci/` if dormant |
| `jitpack.yml` | JitPack auto-detect | No |
| `libs/` | Library JARs (Eclipse projects without Maven/Gradle) | No |

Directories that **belong in root** (standard subdirectories):

| Directory | Purpose | When to Create |
|---|---|---|
| `tools/` | Runtime executables invoked by the application | Project calls `.exe` / `.bin` via ProcessBuilder or similar |
| `packaging/` | Build scripts, launcher scripts, jar-in-jar resources | Ant/custom build — NOT for Maven/Gradle (they stay in root) |
| `samples/` | Sample input files for development/testing | Binary test data that doesn't belong in `src/test/resources/` |
| `releases/` | Versioned release zips and release notes | Project produces distributable artifacts |
| `.launches/` | Shared IDE launch configurations | Eclipse projects with tracked launch configs |

Files that **do NOT belong in root:**

| File Pattern | Move To | Reason |
|---|---|---|
| `implementation_plan*.md` | `docs/` | Internal design artifact |
| `architecture*.md` | `docs/` | Internal design artifact |
| `ADR-*.md` | `docs/adr/` | Architecture Decision Record |
| `design_*.md` | `docs/` | Internal design artifact |
| `*_plan_v*.md` | `docs/` | Versioned plan document |
| Dormant CI config | `ci/` | Not auto-detected by any active platform |
| `*.exe`, `*.bin` (runtime) | `tools/` | Executables invoked by the application |
| `*.nvm`, `*.pib`, `*.hex` (test data) | `samples/` | Binary sample/test files |
| Ant `*.xml` build scripts | `packaging/` | Build scripts for non-Maven/Gradle projects |
| `*.cmd`, `*.sh` (launcher) | `packaging/` | End-user launcher scripts shipped in release |
| `*.launch` (Eclipse) | `.launches/` | IDE launch configurations |
| `jar-in-jar-loader.zip` | `packaging/` | Eclipse packaging resource |
| UML diagrams, `*.png`, `*.svg` | `docs/` | Visual documentation |

***

## Standard Directory Map (SSOT)

| Directory | Purpose | When to Create |
|---|---|---|
| `src/` | Source code | Always (language-specific subtree inside) |
| `docs/` | Design docs, plans, ADRs | When project has internal documentation |
| `ci/` | Dormant/reference CI configs | When CI config is not in its auto-detect location |
| `tools/` | Runtime executables (`.exe`, `.bin`, `.sh`) | When the app invokes external executables via ProcessBuilder / `exec()` |
| `packaging/` | Build scripts, launcher, packaging resources | Ant/custom builds — not Maven/Gradle (they mandate root location) |
| `samples/` | Sample/test-data input files | When binary test data lives in root or doesn't fit `src/test/resources/` |
| `releases/` | Versioned release zips and release notes | When the project produces distributable artifacts |
| `libs/` | Runtime JAR dependencies | Eclipse projects without Maven/Gradle dependency management |
| `.launches/` | Shared IDE launch configurations | Eclipse projects with tracked launch configs |
| `.agents/skills/` | AI agent skills | When project has agent skills |
| `.settings/` | IDE settings (Eclipse) | When tracking shared IDE config |
| `.idea/` | IDE settings (IntelliJ) | When tracking shared IDE config |
| `.github/workflows/` | GitHub Actions | When using GitHub Actions (auto-detected) |
| `test/` | Test code (if separate) | Only if tests don't live inside `src/` |

***

## Prohibited Behaviors

The agent is **BLOCKED** from:

- **Creating empty directories** — only create directories that will immediately contain files
- **Duplicating content across README, AGENTS.md, and SKILL.md** — each has a distinct purpose. Zero overlap
- **Moving tool-mandated files** — `pom.xml`, `.gitignore`, `Makefile`, etc. MUST stay in root
- **Moving active CI configs** — only dormant/unused configs go to `ci/`
- **Creating README.md without all mandatory sections** — partial READMEs are worse than none
- **Inventing project details** — derive from `git config`, `pom.xml`, `package.json`, or ask the user
- **Removing files** — this skill relocates and organizes; it never deletes
- **Ignoring reference updates** — every file move MUST include a search for all references to update
- **Using absolute paths in documentation** — all links MUST be relative for portability

## Common Pitfalls

| Pitfall | Solution |
|---|---|
| Moved `azure-pipelines.yml` but it was the active CI | Check if the project actually uses Azure DevOps before moving |
| Created `docs/` with only one file | Still correct — `docs/` signals "documentation lives here" even with one file |
| README duplicates the SKILL.md procedure | README shows Quick Start (3 steps); SKILL.md has the full procedure |
| AGENTS.md grew to 40+ lines | Trim to ~15 lines — it's a routing table. Defer to README and SKILL.md |
| Moved a file but broke markdown links | Always run blast radius search after every move (Step 3) |
| Created `test/` but Maven expects `src/test/` | Respect the build tool's convention — Maven/Gradle use `src/test/` |
| Root still has stray `.md` files after audit | Re-run Step 1 classification — every root file must be justified |
| `ci/` directory confused for source code | The name `ci/` is a well-known convention (Docker, GitLab, many OSS projects) |
| Moved `.exe` to `tools/` but app still calls old path | Search for `ProcessBuilder`, `Runtime.exec()`, hardcoded exe names in source |
| Moved build script to `packaging/` but named it `build/` | `build/` is commonly gitignored — use `packaging/` for VCS-safe naming |
| Release JAR missing dependency classes | Always test the release from outside the source tree; bundle all runtime JARs |
| Fat JAR crashes with `rsrc:` URI scheme | Jar-in-Jar Loader uses `rsrc:` — code using `Paths.get(URI)` must catch non-`file` schemes |
| Gitignore blocks moved files silently | After every move, run `git status` to confirm files are tracked; add exceptions if needed |
| Version constant stale after restructuring | Search for `VERSION`, `TOOL_VERSION`, etc. in source and update to match release |
| README section order doesn't match user expectations | For CLI tools, promote Quick Start before Requirements/Features |
| Old Readme.txt content lost during rewrite | Always diff old vs new README — every fact from the original must be preserved |
| Quick Start shows developer commands, not end-user | If tool is distributed via toolbase/installer, Quick Start = end-user invocation; dev commands go in Building from Source |
| Samples included in release zip | Samples are for development only — exclude from release target |
| Ant path hardcoded in README | Build tool install paths are machine-specific — use variables or document discovery instructions |
