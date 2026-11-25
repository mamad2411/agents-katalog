---
name: util-projectsync
model: claude-sonnet-4-6
effort: medium
description: >
  Synchronize project folder structure, PRD.md, and BUG.md files based on the canonical application
  and module definitions in CLAUDE.md. Validates dependencies (circular, missing, logical) and
  checks for orphaned services across all applications. Creates missing application folders,
  scaffolds new PRD.md and BUG.md files from templates, adds missing module sections to
  existing files. Inserts [TODO] annotations into CLAUDE.md for validation failures.
  Trigger on keywords: "sync project", "project sync", "sync folders", "sync modules",
  "sync PRD", "sync BUG", "initialize project structure", "scaffold project",
  "create project folders", "sync application structure", "validate dependencies".
  Accepts no arguments — reads all configuration from CLAUDE.md.
---

# Util Project Sync

Synchronize project folder structure, PRD.md, and BUG.md files to match the canonical structure defined in CLAUDE.md. Validates dependencies before syncing.

## Input Resolution

This skill requires no arguments. All configuration is read from CLAUDE.md in the project root.

### Required Sections in CLAUDE.md

| Section | Purpose |
|---------|---------|
| `# Custom Applications` | List of custom applications to create folders for and validate |
| `# Supporting 3rd Party Applications` | List of 3rd party applications referenced as dependencies |
| `## External Services` | External services (SMTP, Push Notifications, AI, WAF, etc.) referenced as dependencies |
| `# Modules` | Module definitions grouped under `## System Module` and `## Business Module` |

### Application Detection

1. Read the `# Custom Applications` section in CLAUDE.md
2. Each application is listed as a `## <Application Name>` heading under the section
3. If the section contains `**No Custom Applications**` or similar "none" indicator, report that there are no applications to sync and **stop**

### 3rd Party Application Detection

1. Read the `# Supporting 3rd Party Applications` section in CLAUDE.md
2. Each 3rd party application is listed as a `## <Application Name>` heading under the section
3. If the section contains `**No Supporting 3rd Party Applications**` or similar "none" indicator, treat as having zero 3rd party applications

### External Services Detection

1. Read the `## External Services` sub-section in CLAUDE.md. It may appear under `# Environment`, under `# Supporting 3rd Party Applications`, or as a standalone section — search the whole document.
2. Services are listed as heading entries that follow `## External Services` until the next top-level (`#`) heading. They typically appear at `## <Service Name>` level (siblings of `## External Services`), but may also appear at `### <Service Name>` level — accept either.
3. Extract the service name from each heading
4. If the section does not exist or contains no services, treat as having zero external services

### Module Detection

1. Read the `# Modules` section in CLAUDE.md
2. Modules are organized under `## System Module` and `## Business Module` subsections
3. **Each module is listed as a `### <Module Name>` heading (three hashes) under its parent `## <tier>` heading.** This is critical: modules in CLAUDE.md are nested one level deeper than in PRD.md/BUG.md because of the extra `# Modules` wrapper. Do not skip modules just because they use `###` — `###` is the correct and expected level.
4. Collect **every** `### <Name>` heading that appears between a `## System Module` / `## Business Module` heading and the next `##` or `#` heading. Treat siblings to the tier heading (not just immediate children in an outline sense) as in-scope. A module may be the first, last, or any-position heading in the list.
5. If a module section contains `**There is no System Module**` or `**There is no Business Module**` or similar "none" indicator, treat that category as having zero modules.

#### Heading-Level Mapping Reference

Modules live at **different heading levels in different files**. Match them by name, not heading level:

| File | Parent heading | Module heading | Example |
|------|----------------|----------------|---------|
| CLAUDE.md | `## System Module` / `## Business Module` (nested under `# Modules`) | `### <Module>` — **three hashes** | `### Support Ticket` |
| PRD.md | `# System Module` / `# Business Module` (top-level) | `## <Module>` — **two hashes** | `## Support Ticket` |
| BUG.md | `# System Module` / `# Business Module` (top-level) | `## <Module>` — **two hashes** | `## Support Ticket` |

When comparing module names across files, strip heading hashes and whitespace, and compare case-insensitively. A `### Support Ticket` in CLAUDE.md is the same module as `## Support Ticket` in PRD.md/BUG.md.

#### Pre-Flight Module Count

After parsing CLAUDE.md, print a one-line confirmation of what was detected **before** proceeding to PRD.md/BUG.md sync, so a missed module is caught immediately:

```
[Module Detection] System Modules: <count> — <comma-separated names>
[Module Detection] Business Modules: <count> — <comma-separated names>
```

If a module the user expects to see is missing from this line, stop and investigate CLAUDE.md heading levels before continuing.

## Workflow

### 1. Parse CLAUDE.md

Read CLAUDE.md from the project root and extract:
- **Custom Application list**: names and their full content (description, dependencies) from `## <Name>` headings under `# Custom Applications`
- **3rd Party Application list**: names and their full content from `## <Name>` headings under `# Supporting 3rd Party Applications`
- **External Services list**: names from `## <Name>` headings under `## External Services`
- **All dependency target names**: combined list of custom application names, 3rd party application names, and external service names (used as the valid dependency pool)
- **System Modules**: names from every `### <Name>` heading (three hashes) appearing between `## System Module` and the next `##` or `#` heading. Do **not** look for `## <Name>` — that level is reserved for the tier heading itself.
- **Business Modules**: names from every `### <Name>` heading (three hashes) appearing between `## Business Module` and the next `##` or `#` heading.

After collecting both lists, emit the pre-flight module count line (see Module Detection → Pre-Flight Module Count). If the count is lower than expected for this project, stop and re-check heading levels before syncing — silently skipping a module that was incorrectly parsed is the primary failure mode this step guards against.

### 2. Validate Dependencies

Run all validation checks across `# Custom Applications`, `# Supporting 3rd Party Applications`, and `## External Services`. Collect all issues found. After all checks are complete, insert `[TODO]` annotations into CLAUDE.md for each issue.

#### 2a. Dependency Validation

For each application (custom and 3rd party) that has a `- Depends on:` section, extract its dependency list. Each dependency is a bullet item under "Depends on:" — the dependency name is the text before any parenthetical qualifier or "for"/"to"/"when" clause.

**Check 1: No Circular Dependencies**

Build a directed dependency graph from all applications. Detect cycles using depth-first traversal. A circular dependency exists when application A depends on B, and B depends (directly or transitively) on A.

Example of a circular dependency:
- Hub Middleware depends on HC Adapter Message Queue
- HC Adapter Message Queue depends on Hub Single Sign On
- Hub Single Sign On depends on Hub Middleware (cycle!)

For each cycle found, record the full cycle path (e.g., `Hub Middleware -> HC Adapter Message Queue -> Hub Single Sign On -> Hub Middleware`).

**Check 2: All Dependencies Exist**

For each dependency listed, verify that a matching entry exists in `# Custom Applications`, `# Supporting 3rd Party Applications`, or `## External Services`. Match by name, case-insensitively. The dependency name may include a database name qualifier in parentheses (e.g., `Hub Support Database (urp_hub_kc)`) — match against the application/service name only (e.g., `Hub Support Database`).

**Check 3: Dependencies Are Logical and Consistent**

Check for logical issues:
- **Duplicate dependencies**: The same dependency listed more than once under the same application (e.g., `Hub Cache` listed twice under Hub Middleware)
- **Self-dependency**: An application listing itself as a dependency
- **Dependency on application in wrong tier**: A 3rd party application or external service depending on a custom application (3rd party and external services should not depend on custom apps; custom apps depend on 3rd party, external services, or other custom apps)

**Check 4: No Orphaned Services or 3rd Party Applications**

For each application in `# Supporting 3rd Party Applications` and each service in `## External Services`, check whether at least one custom application (from `# Custom Applications`) lists it in its `- Depends on:` section. Match by name, case-insensitively, stripping parenthetical qualifiers.

Flag any 3rd party application or external service that is **not depended on by any custom application**. These are orphaned — they are defined in CLAUDE.md but no custom application uses them, which may indicate a missing dependency declaration or a service that is no longer needed.

#### 2b. Insert TODO Annotations into CLAUDE.md

For each validation issue found, insert a `[TODO]` annotation line **immediately above** the `## <Application Name>` heading of the affected application in CLAUDE.md.

**Format:**
```
- [TODO] <CATEGORY>: <description>
## <Application Name>
```

**Categories:**
| Category | Code |
|----------|------|
| Circular Dependency | `CIRCULAR_DEP` |
| Missing Dependency | `MISSING_DEP` |
| Duplicate Dependency | `DUP_DEP` |
| Self Dependency | `SELF_DEP` |
| Illogical Dependency | `ILLOGICAL_DEP` |
| Orphaned Service | `ORPHANED_SVC` |

**Examples:**
```markdown
- [TODO] CIRCULAR_DEP: Circular dependency detected: Hub Middleware -> HC Adapter Message Queue -> Hub Single Sign On -> Hub Middleware
- [TODO] MISSING_DEP: Dependency "Hub Analytics" does not exist in Custom Applications, Supporting 3rd Party Applications, or External Services
- [TODO] DUP_DEP: Dependency "Hub Cache" is listed more than once
- [TODO] ORPHANED_SVC: No custom application depends on this service
## Hub Middleware
```

**Note:** If an application has multiple issues, insert multiple `[TODO]` lines above its heading — one per issue.

### 3. Ensure Application Folders Exist

For each application in the `# Custom Applications` list:
1. Convert the application name to `snake_case` for the folder name (e.g., "Hub Middleware" -> `hub_middleware`)
2. Check if a root-level folder exists matching that name (also check for numeric-prefixed variants like `1_hub_middleware`)
3. If the folder **does not exist**, create it at the project root using the snake_case name
4. If the folder **already exists**, skip creation

**Note:** Folders are only created for Custom Applications, not for Supporting 3rd Party Applications.

### 4. Sync PRD.md for Each Application

For each custom application folder:

#### 4a. PRD.md Does Not Exist

Create a new `PRD.md` inside the application folder using the template below:
- Populate the `# System Module` section with all system modules from CLAUDE.md
- Populate the `# Business Module` section with all business modules from CLAUDE.md
- Each module gets the standard subsections: `### User Story`, `### Non Functional Requirement`, `### Constraint`, `### Reference`, `### Test` — all versioned with `[v1.0.0]`

#### 4b. PRD.md Already Exists

1. **Check for top-level extended sections.** Verify that the following three top-level sections exist in PRD.md. These sections sit between `# Context` and `# System Module`:
   - `# Design System`
   - `# Architecture Principle`
   - `# High Level Process Flow`

   For each section that is **missing**, insert it at the correct position (after `# Context` and before `# System Module`, in the order listed above) using the placeholder content from the PRD.md template. Record the addition for the summary output.

   For each section that **already exists**, do nothing — never modify existing content.

2. Parse the existing PRD.md to find all module headings (`## <Module Name>`) under `# System Module`, `# Business Module`, and (if present) `# Deprecated Modules`. For deprecated headings like `## ~~<Module>~~ [DEPRECATED]`, strip the strikethrough markers and `[DEPRECATED]` tag to obtain the canonical module name for comparison.
3. Compare against the module list from CLAUDE.md:
   - **Module exists in both CLAUDE.md and PRD.md (active section)**: Do nothing
   - **Module exists in CLAUDE.md but is currently deprecated in PRD.md** (found under `# Deprecated Modules`): **Restore it.** Remove the `~~...~~` strikethrough and `[DEPRECATED]` tag from the heading, remove the `_Was: System Module_` / `_Was: Business Module_` hint line directly below the heading, and move the entire module block (heading through its closing `---`) back to the end of its original parent section (`# System Module` or `# Business Module`, per the hint). Preserve all existing content (user stories, NFRs, versions). Record the restoration for the summary.
   - **Module exists in CLAUDE.md but NOT in PRD.md (neither active nor deprecated)**: Append the missing module section at the end of its parent section (`# System Module` or `# Business Module`) using the template structure with empty versioned subsections `[v1.0.0]`
   - **Module exists in PRD.md (active) but NOT in CLAUDE.md**: **Soft-deprecate it.** Rename the heading from `## <Module>` to `## ~~<Module>~~ [DEPRECATED]`, insert an italic hint line `_Was: System Module_` or `_Was: Business Module_` immediately below the heading (so the original tier is recoverable), and move the entire module block (heading through its closing `---`) to a `# Deprecated Modules` section at the end of the file. If `# Deprecated Modules` does not yet exist, create it (see Deprecated Modules Template). **Do not touch the inner subsections or version tags** — only the heading is marked, and the block is relocated. Record the deprecation for the summary output.
   - **Module is deprecated in PRD.md AND still absent from CLAUDE.md**: Do nothing — it is already deprecated. No duplicate markers.
4. **Check for missing `### Test` subsections in active modules.** For each module that already exists in PRD.md under `# System Module` or `# Business Module` (not under `# Deprecated Modules`), check whether it contains a `### Test` subsection. If the `### Test` subsection is **missing**, insert it after the last existing standard subsection (`### Reference`) and before the `---` separator that ends the module section, using the template:
   ```markdown
   ### Test
   [v1.0.0]
   ```
   Record the addition for the summary output. If the `### Test` subsection already exists, do nothing — never modify existing content. Deprecated modules are skipped for this check.

### 5. Sync BUG.md for Each Application

For each custom application folder:

#### 5a. BUG.md Does Not Exist

Create a new `BUG.md` inside the application folder using the template below:
- Include the `# Common Module` section
- Populate the `# System Module` section with all system modules from CLAUDE.md
- Populate the `# Business Module` section with all business modules from CLAUDE.md
- Each module gets an empty section with a separator

#### 5b. BUG.md Already Exists

1. Parse the existing BUG.md to find all module headings (`## <Module Name>`) under `# System Module`, `# Business Module`, and (if present) `# Deprecated Modules`. For deprecated headings like `## ~~<Module>~~ [DEPRECATED]`, strip the strikethrough markers and `[DEPRECATED]` tag to obtain the canonical module name for comparison.
2. Compare against the module list from CLAUDE.md:
   - **Module exists in both CLAUDE.md and BUG.md (active section)**: Do nothing
   - **Module exists in CLAUDE.md but is currently deprecated in BUG.md** (found under `# Deprecated Modules`): **Restore it.** Remove the `~~...~~` strikethrough and `[DEPRECATED]` tag from the heading, remove the `_Was: ..._` hint line, and move the block back to the end of its original parent section (`# System Module` or `# Business Module`, per the hint). Preserve all existing bug content and version tags. Record the restoration for the summary.
   - **Module exists in CLAUDE.md but NOT in BUG.md (neither active nor deprecated)**: Append the missing module section at the end of its parent section using the template structure
   - **Module exists in BUG.md (active) but NOT in CLAUDE.md**: **Soft-deprecate it.** Rename the heading from `## <Module>` to `## ~~<Module>~~ [DEPRECATED]`, insert an italic hint line `_Was: System Module_` or `_Was: Business Module_` immediately below the heading, and move the entire module block (heading through its closing `---`) to a `# Deprecated Modules` section at the end of the file. If `# Deprecated Modules` does not yet exist, create it (see Deprecated Modules Template). Do not alter bug entries or version tags. Record the deprecation for the summary output.
   - **Module is deprecated in BUG.md AND still absent from CLAUDE.md**: Do nothing.

### 6. Resolve PRD.md and BUG.md Paths

PRD.md and BUG.md files are located inside the application folder. The exact path depends on whether the project uses a `context/` subfolder:
- If `<app_folder>/context/` exists, use `<app_folder>/context/PRD.md` and `<app_folder>/context/BUG.md`
- Otherwise, use `<app_folder>/PRD.md` and `<app_folder>/BUG.md`

Follow the folder structure defined in CLAUDE.md's `# Application Folder structure` section (or `# Folder structure` in older projects) to determine the correct path. When the CLAUDE.md specification lists `context/` as the home of PRD.md and BUG.md, treat the `context/` subfolder path as authoritative and create it if missing before scaffolding the files.

### 7. Output Summary

Print a summary of all actions taken, validation results, and warnings:

```
## Project Sync Summary

### Modules Detected in CLAUDE.md
| Tier | Count | Names |
|------|-------|-------|
| System Module | 7 | Authentication and Authorization, User, Notification, Activities, Audit Trail, Document Management, Batch Job |
| Business Module | 14 | Dashboard, Location Information, Corridor, Recruitment Step, Employer, Recruitment Agent, Industrial Classification, Occupation Classification, Job Demand, Candidate Profile, Recruitment Agent Sync, News and Announcement, Support Ticket, ... |

### Dependency Validation
| Check | Status | Issues |
|-------|--------|--------|
| Circular Dependencies | PASS/FAIL | 0 or description |
| Missing Dependencies | PASS/FAIL | 0 or count |
| Duplicate Dependencies | PASS/FAIL | 0 or count |
| Self Dependencies | PASS/FAIL | 0 or count |
| Illogical Dependencies | PASS/FAIL | 0 or count |
| Orphaned Services | PASS/FAIL | 0 or count |

### Validation TODOs Inserted
| Application | Section | Issues |
|-------------|---------|--------|
| Hub Middleware | Custom Applications | DUP_DEP: "Hub Cache" listed twice |
| Hub Analytics | Supporting 3rd Party Applications | ORPHANED_SVC: No custom application depends on this service |

### Application Folders
| Application | Folder | Status |
|-------------|--------|--------|
| Hub Middleware | hub_middleware | Created |
| HC Adapter | hc_adapter | Already exists |

### PRD.md Sync
| Application | Status | Sections Added | Modules Added | Modules Deprecated | Modules Restored | Test Subsections Added |
|-------------|--------|----------------|---------------|--------------------|------------------|------------------------|
| hub_middleware | Updated | Design System, Architecture Principle | Payment, Billing | Legacy Auth | Activities | User, Notification |
| hc_adapter | Created | (all sections) | (all modules) | - | - | (all modules) |

### BUG.md Sync
| Application | Status | Modules Added | Modules Deprecated | Modules Restored |
|-------------|--------|---------------|--------------------|------------------|
| hub_middleware | Updated | Payment, Billing | Legacy Auth | Activities |
| hc_adapter | Created | (all modules) | - | - |

### Deprecation Notes
- [hub_middleware/PRD.md] Module "Legacy Auth" was removed from CLAUDE.md — soft-deprecated under `# Deprecated Modules` (content preserved).
- [hub_middleware/PRD.md] Module "Activities" is back in CLAUDE.md — restored from `# Deprecated Modules` to `# System Module`.
```

## PRD.md Template

When creating a new PRD.md or adding module sections, use this structure:

```markdown
# Context
- This document contain user stories, non-functional requirements, constraints and references by module about this application
- The application name can be inferred from the root folder name where this file is located.
- This is a version controlled document, the version is indicated in the square bracket after each section title, and it will be updated whenever there is any change in the content of that section. The versioning format is [v{major}.{minor}.{patch}] where:
  - Major version will be updated when there is a significant change in the content that may affect the overall understanding of the module or the system.
  - Minor version will be updated when there is a minor change in the content that may affect some details but not the overall understanding of the module or the system.
  - Patch version will be updated when there is a small change in the content that does not affect the overall understanding of the module or the system, such as fixing typos or formatting issues.
- For user any item which is no longer valid or applicable, it will be marked with strikethrough and indicated in the new version.

---

# Design System
- No design system defined yet. Refer to a design system specification file if available (e.g., `[DESIGN_SYSTEM.md](reference/DESIGN_SYSTEM.md)`).

---

# Architecture Principle
- No architecture principles defined yet.

---

# High Level Process Flow
- No high level process flows defined yet.

---

# System Module

## {{System Module Name}}

### User Story
[v1.0.0]

### Non Functional Requirement
[v1.0.0]

### Constraint
[v1.0.0]

### Reference
[v1.0.0]

### Test
[v1.0.0]

---

# Business Module

## {{Business Module Name}}

### User Story
[v1.0.0]

### Non Functional Requirement
[v1.0.0]

### Constraint
[v1.0.0]

### Reference
[v1.0.0]

### Test
[v1.0.0]

---
```

### Adding a Missing Module to Existing PRD.md

When a module exists in CLAUDE.md but not in PRD.md, append this block at the end of the appropriate parent section (before the next `#` heading or end of file):

```markdown

## {{Module Name}}

### User Story
[v1.0.0]

### Non Functional Requirement
[v1.0.0]

### Constraint
[v1.0.0]

### Reference
[v1.0.0]

### Test
[v1.0.0]

---
```

## BUG.md Template

When creating a new BUG.md or adding module sections, use this structure:

```markdown
# Context
- This document contain list of bugs reported by users or testers about this application
- All previously reported bugs have been resolved and merged into the PRD.md as NFRs or constraints.

---

# Common Module

[v1.0.0]

---

# System Module

## {{System Module Name}}

[v1.0.0]

---

# Business Module

## {{Business Module Name}}

[v1.0.0]

---
```

### Adding a Missing Module to Existing BUG.md

When a module exists in CLAUDE.md but not in BUG.md, append this block at the end of the appropriate parent section:

```markdown

## {{Module Name}}

[v1.0.0]

---
```

## Deprecated Modules Template

When a module is soft-deprecated (present in PRD.md/BUG.md but removed from CLAUDE.md), it is relocated under a single trailing `# Deprecated Modules` section. The original tier is preserved in an italic hint line for later restoration.

**Section skeleton (created on first deprecation, appended to end of file):**

```markdown

---

# Deprecated Modules
- Modules in this section were present in a prior CLAUDE.md but have since been removed. Content is preserved (not deleted) so that historical user stories, NFRs, constraints, tests, or bug reports remain auditable. If a module returns to CLAUDE.md, the sync skill restores it automatically.

---

## ~~{{Module Name}}~~ [DEPRECATED]
_Was: System Module_

### User Story
[v1.0.0]
... (original content preserved verbatim) ...

---
```

**Rules for the deprecation move:**

- Only the `## <Module>` heading is rewritten (to `## ~~<Module>~~ [DEPRECATED]`) and a single `_Was: <tier>_` hint line is inserted directly under it. Everything else inside the module block — subsection headings, version tags, text, tables — is moved verbatim.
- The trailing `---` separator that closes the module block moves with it.
- If `# Deprecated Modules` already exists, append the block to its end rather than creating a second section.
- For BUG.md, the same structure applies, but the module body is a single `[v1.0.0]` (or whatever version was already present) followed by any bug entries — move them verbatim.

**Rules for restoration (module returns to CLAUDE.md):**

- Locate the deprecated block by canonical name (strip `~~...~~` and `[DEPRECATED]`).
- Rewrite the heading back to `## <Module>` and delete the `_Was: <tier>_` hint line.
- Move the block to the end of the parent section named in the hint (`# System Module` or `# Business Module`).
- If after restoration `# Deprecated Modules` contains no more module blocks, leave the empty `# Deprecated Modules` section in place — do not delete it (users may want to see that deprecations have historically occurred). Re-running the skill with all modules active leaves it untouched.

## Important Rules

- **NEVER delete existing authored content** (user stories, NFRs, constraints, references, tests, bug entries) in PRD.md or BUG.md. When a module is removed from CLAUDE.md, soft-deprecate the module block — do not hard-delete it.
- **NEVER modify existing version tags** (e.g., `[v1.0.0]`). These are immutable, including when a module is deprecated or restored.
- **NEVER modify the inner subsections of an existing module** — only the `## <Module>` heading may be rewritten (for deprecation marking or restoration), and only the `_Was: <tier>_` hint line may be inserted or removed by this skill.
- Preserve all existing content, formatting, and indentation exactly.
- Application folder names must use `snake_case`.
- Folders are only created for `# Custom Applications`, not for `# Supporting 3rd Party Applications`.
- PRD.md and BUG.md are only created/synced for `# Custom Applications`.
- Dependency validation covers `# Custom Applications`, `# Supporting 3rd Party Applications`, and `## External Services`.
- When matching existing folders, account for numeric prefixes (e.g., `1_hub_middleware` matches application "Hub Middleware").
- When adding modules to existing files, maintain the correct order: system modules under `# System Module`, business modules under `# Business Module`.
- Always include separator lines (`---`) between module sections.
- New module sections added to existing files use `[v1.0.0]` as the initial version.
- Module synchronization is bi-directional with content preservation:
  - Module added to CLAUDE.md → appended to PRD.md/BUG.md (or restored from `# Deprecated Modules` if a deprecated block with the same canonical name exists).
  - Module removed from CLAUDE.md → soft-deprecated (heading marked `~~...~~ [DEPRECATED]`, block relocated under `# Deprecated Modules`). Content is never destroyed.
- Module name matching for deprecation/restoration is by **canonical name only** — strip `~~` strikethrough, `[DEPRECATED]` tag, and surrounding whitespace before comparing against CLAUDE.md entries. Name matching is case-insensitive.
- If CLAUDE.md has no custom applications defined, report this clearly and stop without making any changes.
- When inserting `[TODO]` annotations in CLAUDE.md, insert them **immediately above** the `## <Application Name>` heading — never inside the application's content.
- Do not insert duplicate `[TODO]` annotations. If re-running the skill, check for existing `[TODO]` lines above each application heading and skip if the same issue is already annotated.
- When matching dependency names, strip parenthetical qualifiers (e.g., `Hub Support Database (urp_hub_kc)` matches `Hub Support Database`).
- Validation is advisory — it does not block folder creation or PRD.md/BUG.md syncing. All steps run regardless of validation results.
