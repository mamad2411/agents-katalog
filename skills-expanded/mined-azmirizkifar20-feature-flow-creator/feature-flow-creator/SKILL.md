---
name: feature-flow-creator
version: 2.4.6
description: Use when initializing a new project, setting up documentation structure, or creating project scaffolding with AGENTS.md and docs/ folder hierarchy for feature-based documentation. Also use when user asks to setup project documentation, generate docs structure, or create issue documentation for bugs and root cause analysis.
---

# Feature Flow Creator

## Overview

Generates standardized project documentation structure following the rhapsodie-shell pattern. Creates `AGENTS.md` and `CLAUDE.md` at project root and organizes documentation under `docs/` with consistent folder hierarchy and README.md index files. Auto-creates a project-specific skill in `.agents/skills/{project-name}-feature-flow/` (read by opencode and Codex) and `.claude/skills/{project-name}-feature-flow/` (Claude Code). Because Codex reads skills from `.agents/skills/`, the same project skill serves both opencode and Codex.

## When to Use

- New project initialization requiring documentation structure
- Setting up feature-based documentation workflow
- Creating consistent docs/ folder hierarchy across projects
- Generating issue tracking documentation for bugs and root cause analysis
- User says "init docs", "setup dokumentasi", "buat struktur docs", "generate docs"

## Quick Reference

| Action | Description |
|--------|-------------|
| Auto-generate all | Call skill → agent auto-detects project, creates all docs (incl. setup.md, api-conventions.md for backend), fills placeholders, discovers features, creates feature docs + project skill (mode `setup`). If target files already exist, asks: overwrite (per-file choice) / continue / cancel |
| Add issue docs | User says "cek bugs" or "cari root cause" → auto-creates YYYY-MM-DD_issue.md |
| Refresh project skill only | If the project skill exists but is stale (older version marker), re-call the skill → agent runs mode `sync`: updates the project skill files (both `.agents/skills/` and `.claude/skills/`) without touching docs |
| Audit docs health (read-only) | User says "check docs", "audit docs", "cek dokumentasi", "docs gak sinkron" → agent runs mode `check`: verifies Recent/Updated lines are not bloated, indexes match real files, no placeholders, project skill current. Changes NOTHING — reports findings only |

## Implementation Steps

**Determine the operation MODE first. This decides whether to touch existing docs or only refresh the project skill.**

Three modes:
- **`setup` (default, new/empty project)**: Generate the full structure — directories, ALL doc files, feature discovery, and the project skill. Use when the project has no `docs/` yet or no `{project-name}-feature-flow` skill yet.
- **`sync` (project already scaffolded by this skill)**: Refresh ONLY `.agents/skills/{project-name}-feature-flow/SKILL.md` and `.claude/skills/{project-name}-feature-flow/SKILL.md` when their embedded version marker is older than this skill's version. Do NOT touch or regenerate any existing `docs/` files, `AGENTS.md`, or `CLAUDE.md`.
- **`check` (read-only audit)**: Verify docs health WITHOUT changing anything — no file writes, no marker updates, no `**Updated**:` bumps. Use when the user asks to check/audit/verify the docs ("check docs", "audit docs", "cek dokumentasi", "docs gak sinkron", "cek kesehatan docs") or when docs bloat/out-of-sync is suspected.

**How to choose the mode:**
1. Does the user want to VERIFY/AUDIT the existing docs (not generate or refresh)? → mode `check`: run the Check-Mode Checklist below, report PASS/FAIL per item, change NOTHING. Wait for the user to ask for fixes before writing anything.
2. Does `.agents/skills/{project-name}-feature-flow/SKILL.md` or `.claude/skills/{project-name}-feature-flow/SKILL.md` already exist? 
   - Neither → mode `setup`.
   - Either one exists → read its version marker (a line like `<!-- feature-flow-creator vX.Y -->`). Compare with this skill's version (frontmatter `version:`).
3. If the project skill exists AND its marker version >= this skill's version → already up to date, choose mode `setup` but SKIP Step 2–4 (protect existing docs) and only ensure Step 5 files match (create the missing location if only one exists, or report nothing changed).
4. If the project skill exists AND its marker version < this skill's version → choose mode `sync`: update the project skill files to the latest template content, merging/replacing their sections, and DO NOT touch existing docs.

**Check-Mode Checklist (mode `check` — read-only, changes NOTHING):**
1. **Recent/Updated lines within budget** — `**Recent**:` in `docs/features/README.md` and `**Updated**:` in `docs/design-system/README.md` are each ≤ 300 characters and describe ONE single most-recent change (no `;`-chained history, no "also X, then Y" accumulation). Flag any line over budget or holding multiple changes.
2. **Indexes match reality** — every entry in `docs/features/README.md`, `docs/steering/README.md`, `docs/issue/README.md`, and (if present) `docs/design-system/README.md` points to an existing file; AND every generated doc file is listed in its index. Report dangling index entries and orphan docs (file exists but not listed).
3. **No placeholders** — run the placeholder scrubber regex (Step 4.5) over `docs/` + `AGENTS.md` + `CLAUDE.md`; expect ZERO hits.
4. **Project skill current + identical** — BOTH `.agents/skills/{project-name}-feature-flow/SKILL.md` and `.claude/skills/{project-name}-feature-flow/SKILL.md` exist, carry a version marker >= this skill's version, and are identical to each other.
5. **Design-system only if UI** — `docs/design-system/` exists ONLY when a UI layer was detected.
Report each item as PASS/FAIL with concrete file paths. If everything passes, state the docs are healthy. If anything fails, list exactly what to fix — but DO NOT fix in `check` mode; wait for the user to ask.

**Decision gate for pre-existing files (mode `setup`):** Before writing ANY doc file, check which of these already exist: `AGENTS.md`, `CLAUDE.md`, `docs/README.md`, `docs/steering/README.md`, `docs/steering/routing.md`, `docs/steering/system-flow.md`, `docs/steering/tech-stack.md`, `docs/steering/architecture.md`, `docs/steering/setup.md`, `docs/steering/api-conventions.md`, `docs/issue/README.md`, `docs/design-system/README.md`. Group the findings:

- If **NONE** of the target files exist → proceed automatically (no prompt needed), create everything.
- If **at least one** exists → STOP and ASK the user how to handle existing files. Present the list of existing files and offer these options:
  1. **Overwrite all** — replace every existing doc file with this skill's template (loses prior content; confirm this is intended).
  2. **Continue (skip existing, fill missing only)** — leave existing files untouched, only create the files that do not exist yet. (default, safest)
  3. **Cancel** — abort the whole operation, change nothing.

**If the user chooses "Overwrite all":** do NOT overwrite everything blindly. Instead, go file-by-file — show the list of existing files and ask the user to pick which specific ones to overwrite (one at a time or as a subset). For each selected file, list its current purpose/content briefly, then confirm the replacement before writing. For any file NOT selected, keep its existing content (skip it). Only after the user explicitly picks a file is it overwritten.
- Never silently decide on the user's behalf when existing files are present.
- Re-run the chosen action file-by-file. Never silently decide on the user's behalf when existing files are present.

**Hard rule for BOTH modes:** Never overwrite an existing `docs/**` file, `AGENTS.md`, or `CLAUDE.md` with an empty template — EXCEPT when the user explicitly chose "Overwrite all" at the decision gate above. Only create files that do not exist yet. Preserve any existing content unless overwrite was chosen.

### Step 1: Detect Project Name

Agent MUST auto-detect project name from:
1. `package.json` → `name` field
2. `composer.json` → `name` field
3. Folder name if no config found

```bash
# Auto-detect project name
PROJECT_NAME=$(node -e "console.log(require('./package.json').name)" 2>/dev/null || \
               composer show --name 2>/dev/null || \
               basename $(pwd))
```

### Step 2: Create Full Directory Structure

Agent MUST detect whether the project has a UI/frontend layer, then create directories accordingly. Creating directories is **idempotent** (`mkdir -p` never destroys existing folders); no files are touched here.

**UI presence check** (create `docs/design-system/` ONLY if any of these exist):
- View/template dirs: `resources/views`, `pages/`, `app/` (frontend), `src/` (frontend framework), `templates/`
- Frontend entry points: `package.json` with a frontend framework (React/Vue/Svelte), `vite.config.*`, `webpack.*`, `app.css`, `*.blade.php` alongside JS bundles
- API-only projects (pure Laravel API, Express API without views, FastAPI, etc.) → NO design-system

```bash
# Create all directories (core)
mkdir -p docs/{features,steering,issue}

# Create design-system ONLY if UI layer detected
if [ -d resources/views ] || [ -d pages ] || [ -f vite.config.* ] || [ -d src ]; then
  mkdir -p docs/design-system
fi

# Create project skill directories (opencode + Codex share .agents/skills/, Claude Code uses .claude/skills/)
mkdir -p ".agents/skills/${PROJECT_NAME}-feature-flow"
mkdir -p ".claude/skills/${PROJECT_NAME}-feature-flow"
```

### Step 3: Generate All Documentation Files

Agent MUST create all files with content (see Templates section). **Anti-overwrite guard:** for each file below, only write it if it does NOT already exist. If it exists, leave it untouched (log/skip it). Never replace existing content with an empty template — UNLESS the user explicitly selected that specific file for overwrite at the decision gate; only those selected files get overwritten, all others are skipped:
1. `AGENTS.md` at project root (skip if exists, or overwrite only if user selected it)
2. `CLAUDE.md` at project root — same content as `AGENTS.md` (Skills Auto-Load + Documentation Structure), for Claude Code. Skip if exists, or overwrite only if user selected it. (`AGENTS.md` is the file the AI agents read — opencode, Codex, and others; `CLAUDE.md` exists so Claude Code also auto-loads the project skill.)
3. `docs/README.md` (skip if exists)
4. `docs/features/README.md` (skip if exists)
5. `docs/steering/README.md` (skip if exists)
6. `docs/steering/routing.md` (skip if exists)
7. `docs/steering/system-flow.md` (skip if exists)
8. `docs/steering/tech-stack.md` (skip if exists)
9. `docs/steering/architecture.md` (skip if exists)
10. `docs/steering/setup.md` (skip if exists)
11. `docs/steering/api-conventions.md` — ONLY for backend/API projects with endpoint/controller code. Skip for pure frontend-only projects.
12. `docs/issue/README.md` (skip if exists)
13. `docs/design-system/README.md` + one sub-folder per UI module (see the design-system template guide) — ONLY if a UI/frontend layer was detected in Step 2. Skip entirely for pure backend/API projects. Also skip if it already exists.

### Step 4: Discover Existing Features & Create Feature Docs

Agent MUST scan the project to find already-implemented features and auto-create a numbered feature doc for each, so `docs/features/` is NOT left with only a README.md. **Anti-duplication guard:** this step runs only in mode `setup` for features NOT yet documented. Before creating a feature doc, check `docs/features/` for an existing doc covering that feature; if present, skip it (do not create a duplicate or overwrite).

**Discover features from the codebase** (stack-agnostic):
- Scan route files for grouped route prefixes → each group = one feature (e.g. `routes/web_admin.php`, `routes/api.php`).
- Scan controllers/modules/domains: `app/Http/Controllers`, `src/`, `app/`, `lib/`, `packages/` — each controller/module class = one feature candidate.
- Scan domain models/services that appear in multiple routes.
- Scan frontend views/pages if present (`resources/views`, `pages/`, `app/`).
- Group related routes/controllers/services under ONE feature doc; do not create one doc per route.

**Map each discovered feature to a doc:**
1. Number sequentially: `01-...md`, `02-...md`, ... in logical order (platform overview first if it exists).
2. Name file kebab-case: `01-user-authentication.md`, `02-checkout-flow.md`, ...
3. For each feature, write a doc following the Feature Doc Template below (trace real routes, controllers, models, views).
4. Add every doc as an entry + link in `docs/features/README.md` index.

**Ordering convention** (like rhapsodie): platform overview & access first, then core user flows, then admin/business modules, then shared/edge features.

**If the project is too small / has no distinguishable features**, create at least one doc capturing the overall app flow instead of leaving the folder empty.

### Step 4.5: Fill Placeholders — Zero-Placeholder Rule (REQUIRED)

Generated docs must be LIVING documentation, not empty templates. Every generated file MUST be filled with real content traced from the codebase — never left as a bare template.

**Fill rules:**
- Replace every `<!-- ... -->` comment, `[...]`, `[file path]`, `[paths]`, "Add ... here", "Document ... here" with actual content from the repo (real routes, file paths, components, commands).
- Trace real paths/names from the codebase; do not invent them. If a section genuinely has no content yet, write an explicit status — `Currently not used` or `Please document when introduced` — instead of leaving a placeholder. Never leave an empty placeholder comment.
- `docs/steering/` docs: fill from discovered entry points, configs, and conventions.
- `docs/design-system/` docs: fill from actual components/tokens found (or mark sections `Currently not used` if the repo has none).

**Cross-linking (docs must be a connected system, not isolated files):**
- Each feature doc: in its flow/data sections, link to the relevant `docs/steering/system-flow.md` (runtime path), `docs/steering/architecture.md` (component), and — if it touches UI — the relevant `docs/design-system/*` doc. Add links under a `## Cross-References` section at the end of the feature doc.
- Steering docs: if a steering doc describes a flow used by features, note which feature docs reference it.
- Use relative links so the whole `docs/` tree works when opened on disk/GitHub: `(../steering/system-flow.md)`, `(../design-system/README.md)`.

**Placeholder scrubber (run LAST, after Step 4 feature docs too):** grep the entire generated `docs/` + `AGENTS.md` + `CLAUDE.md` for leftover placeholders — regex: `<!--`, `\[\.\.\.\]`, `\[file path\]`, `\[paths\]`, `Add .*here`, `Document .*here`, `\[ONLY`, `\[describe`, `\[fill in`, `\[How to verify`. Beyond the regex, ALSO flag any remaining square-bracket instruction in generated docs — a `[...]` whose content is a generic template instruction (e.g. `[ONLY the single most recent change ...]`, `[describe last change]`, `[fill in real command ...]`, `[File paths involved in the issue]`, `[How to verify the fix works]`) rather than a real repo value. Resolve every hit with real content or an explicit `Currently not used` note. Output of the run MUST have ZERO placeholder hits. If any remain, keep fixing until clean.

### Step 5: Create or Sync Project-Specific Skill

Agent MUST ensure the project skill exists in BOTH locations, with content adapted from the Project-Specific Feature Flow Skill Template below, AND carrying the current version marker:
- `.agents/skills/{project-name}-feature-flow/SKILL.md` (opencode + Codex)
- `.claude/skills/{project-name}-feature-flow/SKILL.md` (Claude Code)

**Version marker:** the generated project skill MUST end with this exact comment line:
```
<!-- feature-flow-creator v2.4.6 -->
```
This marker is how future runs detect whether the project skill is stale.

**Behavior by mode:**
- **Mode `setup`** (no project skill yet): create the file fresh from the template, adapted to the repo (entry points, conventions, test commands). Append the version marker line at the end. Write it to BOTH `.agents/skills/` and `.claude/skills/`.
- **Mode `sync`** (project skill exists with an older marker): rewrite ONLY the project skill files to match the current template + this repo's specifics, preserving/merging any repo-specific sections the agent had added previously (entry points, conventions, test commands). Update the marker to `v2.4.6`. Write to BOTH locations. Do NOT touch `docs/`, `AGENTS.md`, or `CLAUDE.md`.
- **Project skill exists with same-or-newer marker**: do nothing to it (already current).

**In BOTH modes, if the project skill already contains repo-specific context (entry points, conventions, test commands), preserve that context — never strip it just to match the template verbatim.**
**If one location exists but the other doesn't, create the missing one** with the same content (a project may have been scaffolded before the dual-location rule).

**Test commands in the project skill:** detect the repo's actual test framework (from `package.json` scripts, `phpunit.xml`, `pyproject.toml`/`pytest.ini`, etc.) and write the REAL command into the project skill's "Verify" section (e.g. `npm test`, `npx jest src/__tests__/...`, `php artisan test --filter=...`). Use the Stack → Test Command Quick Map below as a shortcut, but always prefer the repo's detected command.

**If the repo has NO automated test suite** (no test script, no test framework deps): in the project skill's "Add or update tests" section, KEEP the test-evaluation rules (treat test evaluation as part of the implementation; don't force tests for low-risk edits; state the reason when choosing not to add tests). Replace ONLY the framework-specific lines with an explicit note — `No automated test suite is configured in this repo.` — plus the repo's real manual verification steps (e.g. dev server + health check + representative payloads). Do NOT strip the framework-agnostic guidance.

**Convention capture (automatic):** read 2–3 representative source files (entry file, one model, one controller/service) and extract the repo's conventions, then write them into the project skill's "repo conventions" section. Look for:
- Module system: CommonJS vs ESM (`require`/`module.exports` vs `import`/`export`), language (TypeScript/JavaScript/PHP/Python/etc.)
- Quote style, semicolons, formatting preferences visible in the sample
- Naming / file structure: `{name}.{role}.js`, folder conventions, casing
- Return shapes: e.g. `{ success, data, error, message }`, `{ code, data, error, message }`, REST envelope
- Error handling: try/catch style, error classes, middleware
- Data access: ORM/query builder, DB connection lifecycle (e.g. per-request / per-task dynamic connections)
- Auth / middleware patterns seen in the samples
Do NOT guess — only record what the samples actually show.

### Step 6: Quality Gate (REQUIRED before finishing)

Before declaring the operation complete, verify ALL of the following. If any check fails, fix it and re-check. Do not finish with known gaps.

1. **No placeholders left** — run the placeholder scrubber regex over `docs/` + `AGENTS.md` + `CLAUDE.md`; expect ZERO hits.
2. **Paths are real** — every file path referenced in feature docs / steering docs must actually exist in the repo (spot-check links and `[backtick]path[backtick]` refs). Remove or correct any path that does not exist.
3. **Indexes are populated** — `docs/README.md`, `docs/features/README.md`, `docs/steering/README.md`, `docs/issue/README.md` each list their actual contents (not empty "Add ... here").
4. **Feature docs exist** — `docs/features/` is not limited to a bare README; every discovered feature has a doc, or (small project) at least one overall-flow doc.
5. **Project skill is valid** — BOTH `.agents/skills/{project-name}-feature-flow/SKILL.md` and `.claude/skills/{project-name}-feature-flow/SKILL.md` exist with the current version marker and correct frontmatter (`name`, `description`).
6. **AGENTS.md / CLAUDE.md load the skill** — project root `AGENTS.md` and `CLAUDE.md` mention loading `{project-name}-feature-flow` for feature work.
7. **Design-system only if UI** — `docs/design-system/` exists ONLY when a UI layer was detected; pure backend has none.
8. **Recent/Updated lines within budget** — `**Recent**:` in `docs/features/README.md` and `**Updated**:` in `docs/design-system/README.md` are each ≤ 300 characters and describe ONE single most-recent change (no chained history, no "also/and" accumulation). If a line was already bloated by a previous run, collapse it to the latest change only.

## Templates

### AGENTS.md Template

```markdown
## Skills Auto-Load

Before implementing any feature, change, extension, or refactoring task, ALWAYS check and load the appropriate skill:
- For feature work (implement, add, create, change, extend, refactor): Load `{project-name}-feature-flow` skill first
- The skill defines the required workflow: read docs → trace runtime path → add/update tests when they protect the change → verify → update/create docs

When the user asks for any code change (implement, add, fix, refactor), ALWAYS load `{project-name}-feature-flow` before touching code — regardless of task size.

## Documentation Structure

This project uses structured documentation under `docs/`:
- `docs/features/` - Current-state feature documentation
- `docs/steering/` - Technical architecture and stack decisions
- `docs/issue/` - Bug reports and root cause analysis
<!-- Only if UI layer exists: -->
<!-- - `docs/design-system/` - UI conventions and shared components -->
```

### CLAUDE.md Template

`CLAUDE.md` is the Claude Code equivalent of `AGENTS.md` — same content, same purpose (Claude Code reads it automatically at session start). `AGENTS.md` is used by opencode and Codex. Generate both at project root whenever the project will be worked on with any AI agent. If `AGENTS.md` exists but `CLAUDE.md` does not (or vice versa), generate the missing one with the same content. Keep both files in sync: they MUST say the same thing.

```markdown
## Skills Auto-Load

Before implementing any feature, change, extension, or refactoring task, ALWAYS check and load the appropriate skill:
- For feature work (implement, add, create, change, extend, refactor): Load `{project-name}-feature-flow` skill first
- The skill defines the required workflow: read docs → trace runtime path → add/update tests when they protect the change → verify → update/create docs

When the user asks for any code change (implement, add, fix, refactor), ALWAYS load `{project-name}-feature-flow` before touching code — regardless of task size.

## Documentation Structure

This project uses structured documentation under `docs/`:
- `docs/features/` - Current-state feature documentation
- `docs/steering/` - Technical architecture and stack decisions
- `docs/issue/` - Bug reports and root cause analysis
<!-- Only if UI layer exists: -->
<!-- - `docs/design-system/` - UI conventions and shared components -->
```

### docs/README.md Template

```markdown
# Documentation Map

This folder is organized by document type.

## Primary Entry Points

- [Feature Documentation](./features/README.md)
- [Technical Steering](./steering/README.md)
- [Issue Tracking](./issue/README.md)
<!-- Only if UI layer exists: -->
<!-- - [Design System](./design-system/README.md) -->

## Folder Intent

- `features/`: Current-state feature documentation referenced by the repo workflow.
- `steering/`: Technical architecture, routing, and stack decisions.
- `issue/`: Bug reports, root cause analysis, and issue findings.
<!-- Only if UI layer exists: -->
<!-- - `design-system/`: UI conventions and shared surface/component guidance. -->
```

### docs/features/README.md Template

```markdown
# Feature Documentation

This folder contains documentation for implemented features and current state.

**Updated**: YYYY-MM-DD
**Recent**: [ONLY the single most recent change — REPLACE this line on every update, NEVER append]

## Index

<!-- Add feature documentation entries here -->
<!-- Example: -->
<!-- 1. [Feature Name](./01-feature-name.md) -->

---

**Catatan**: Tambahkan dokumen baru untuk fitur baru dengan nomor urut berurutan (misal terakhir `05-...md`, berikutnya `06-...md`). Perbarui dokumen yang ada saat fitur direvisi, dan selalu catat tanggal update di bagian atas README ini.
```

### Feature Doc Template (`NN-feature-name.md`)

One file per feature, traced from the real codebase. Used by Step 4 (discovery) and by the recurring update/create rule:

```markdown
# {Feature Name}

## 1) What This Feature Is

One-paragraph summary of the feature and its purpose.

- Routes: [route file(s)](../../routes/...)
- {View/Pages}: [path](../../resources/views/...)

## 2) Flow / Behavior

- Step-by-step flow from entry point to completion.
- Note branching by surface if behavior differs (admin vs public, cart vs direct checkout, etc).

## 3) Domain & Data

- Key models/tables involved and their relationships.
- Relevant enums / status values / constants.
- Key services/controllers handling the logic.

## 4) UI

- Main screens/pages and their routes.
- Reusable components used.
- Any input formatting / validation rules worth noting.

## 5) Edge Cases & Rules

- Non-obvious business rules, validations, or operational rules.
- Known caveats or gaps found during tracing.

## Related Files

- [Actual file paths involved in the feature]

## Cross-References

- System flow: [../steering/system-flow.md](../steering/system-flow.md)
- Architecture: [../steering/architecture.md](../steering/architecture.md)
- UI/Design: [../design-system/README.md](../design-system/README.md) (if applicable)
```

### docs/design-system/README.md Template

```markdown
# Design System

This folder documents the front-end design system(s), one per UI module or surface.

**Updated**: YYYY-MM-DD — [ONLY the single most recent design-system change — REPLACE this line on every update, NEVER append a changelog here; the full history lives in the per-topic/per-module docs below]

## Structure

| Folder | Module / Surface | Status |
|--------|------------------|--------|
| [`<module-a>/`](module-a/README.md) | <one-line description> | ✅ Active |
| [`<module-b>/`](module-b/README.md) | <one-line description> | ✅ Active |
<!-- Add module folders here -->

Shared building blocks that are not module-scoped live at the top level:

| Doc | Covers |
|-----|--------|
| [`<shared-doc>.md`](shared-doc.md) | <what it covers> |
<!-- Add shared top-level docs here -->

## Multi-Surface Architecture

How the module-oriented design systems are organized and loaded. Describe the CSS/JS/component entry points per module (details live in each module folder's README).

```
<design-system-entry>
  <module-a files...>
  <module-b files...>
```

## Modules

- **<module-a>** — directory `[<module-a>/](module-a/README.md)`. <2-3 sentence summary>
- **<module-b>** — directory `[<module-b>/](module-b/README.md)`. <2-3 sentence summary>

## Design Tokens (shared)

- **Colors**: `[palette source]` — semantic roles vs raw values
- **Typography**: `[font stack, scale, source]`
- **Spacing / Radius / Shadows**: `[source]`
- **Dark mode**: `[how it is enabled]`

## State Management (shared)

- Library / pattern: `[Redux / Zustand / Context / Pinia / Vuex / server state ...]`
- Where stores/slices live, how data flows into components
- Server vs client state boundary
```

**Note for the generator (design-system master):** resolve the `<!-- ... -->` conditional comments while filling this template — keep the shared top-level docs table rows and module rows only where they exist, and remove the comment lines. Leftover `<!--` will fail the placeholder scrubber (Step 4.5).

### docs/design-system/<module>/README.md Template

One folder per UI module/surface. Guide the generator on how to pick folders below.

```markdown
# <Module Name> Design System

A design system for the <module> surface: <one-line description>.

## Current Status

<short status update on this module's design-system coverage>

## Goals

1. <goal>
2. <goal>

## Architecture

| Layer | Location | Purpose |
|-------|----------|---------|
| Styling / CSS | `<paths>` | tokens + component classes, how it loads |
| Scripts / JS | `<paths>` | utilities, framework glue |
| Components | `<paths>` | component library location + naming |

## Component Rules

1. <rule for building UI in this module>
2. <rule>

## Known Exceptions

- <accepted deviation, and why>

See also:

- [Styling](css.md) (if applicable)
- [Scripts / JS](js-utilities.md) (if applicable)
- [Components](components.md) (if applicable)
- [Progress](progress.md)
```

**Guide for the generator (design-system sub-folders):** after creating `docs/design-system/README.md`, detect the project's UI modules/surfaces (e.g. route prefixes like `/admin`, `/business`, `/user`; component/layout dirs; portal entry points). Create **one sub-folder per module** — `<module>/README.md` from the template above, plus layer files `css.md`, `js-utilities.md`, `components.md`, `progress.md` ONLY if the module actually has that layer (omit what doesn't exist; do not create empty placeholder files). Update the master README's Structure & Modules tables to list every folder created. For a project with a single uniform UI (no distinct module/surface split), create ONE sub-folder named after the app or `core/` instead of forcing multiple.

### docs/steering/README.md Template

```markdown
# Technical Steering

This folder contains technical architecture and stack decisions.

## Contents

- [Routing Structure](./routing.md)
- [System Flow](./system-flow.md)
- [Technology Stack](./tech-stack.md)
- [System Architecture](./architecture.md)
- [Setup & Running](./setup.md)
<!-- Only if the project has backend/API code: -->
<!-- - [API Conventions](./api-conventions.md) -->
```

**Note for the generator:** resolve the `<!-- ... -->` conditional comments while filling this template — keep the API Conventions line only when the project is backend/API, and remove the comment lines. Leftover `<!--` will fail the placeholder scrubber (Step 4.5).

### docs/steering/routing.md Template

```markdown
# Routing Structure

## Overview

Document route structure and conventions for this project.

## Routes

<!-- Add route documentation here -->
```

### docs/steering/system-flow.md Template

```markdown
# System Flow

How the application boots, initializes, and routes requests at runtime. This is the starting point for tracing any feature end-to-end.

## Bootstrap & Entry Points

- **App bootstrap**: `[file path]` — what runs first (e.g. `app.js`, `index.php`, `main.py`, `server.ts`)
- **Server start**: `[file path]` — how the process is launched (e.g. `bin/www`, `artisan serve`, `uvicorn`, `next start`)
- **Startup hooks / initializers**: `[file paths]` — middleware, service registrations, DB connections, queue workers, scheduled jobs

## Request Lifecycle

1. Incoming request/event → entry route (`[path]`)
2. Middleware chain / auth gate (`[paths]`)
3. Controller / handler (`[path]`)
4. Domain service / model calls (`[paths]`)
5. Response / side effects (DB writes, queues, external calls)

## Background / Scheduled Flows

- `[job/queue/cron name]` → `[handler path]` → purpose

## Environment & Config

- Required env vars (`.env.example`) and where config is loaded
- Feature flags / multi-tenant switches that change the flow
```

### docs/steering/setup.md Template

```markdown
# Setup & Running

How to run, debug, and work on this project locally.

## Prerequisites

- Runtime/toolchain versions (Node `[xx]`, PHP `[xx]`, Python `[xx]`, DB server, etc.)
- Package manager / dependency install command (`npm install`, `composer install`, `pip install`, etc.)

## Install & Configure

1. `[install command]`
2. Copy `[.env.example]` → `[.env]` and fill required vars (listed in system-flow.md Env section)
3. Migrations / schema setup: `[command]` (if applicable)
4. Seed data / fixtures: `[command]` (if applicable)

## Run

- Dev server: `[npm run dev / php artisan serve / uvicorn ... ]`
- Build (if frontend): `[npm run build]`
- Tests: `[npm test / php artisan test / pytest ...]`

## Debug

- Log locations / logging setup
- Debugger / breakpoint workflow (e.g. `--inspect`, Xdebug, PyCharm attach)
- Common issues & quick checks

## DB / Tooling Access

- Local DB connection details (host, name, user), admin UI
- Queue/worker or scheduled-task runners to start locally
```

### docs/steering/api-conventions.md Template

```markdown
# API Conventions

Conventions every endpoint/handler should follow. For use when adding/editing API or controller code.

## Response Envelope

- Success shape: `{ code, data, message }` (adjust to the repo's real shape — see **Conventions** in the project skill)
- Error shape: `{ code, error, message }` — how failures are returned
- HTTP status usage: which codes map to which cases (200/201/400/401/403/404/422/500)

## Error Handling

- Where errors are caught (middleware, async wrappers, controller try/catch)
- Error classes / codes used; how to log them
- Validation failures → format returned to the client

## Naming & Routing

- Route / resource naming convention, pluralization, versioning (`/api/v1/...`)
- Controller/handler file naming and location
- Query params vs path params vs body conventions

## Auth & Permissions

- Auth mechanism (JWT, sessions, API key) and where the token lives
- Middleware / guards applied to which route groups
- Role/permission checks and where they run

## Data Access

- Persistence layer used (ORM/query builder) and transaction guidelines
- Multi-tenant isolation (e.g. dynamic DB connection per tenant, tenant id scoping)
- Pagination / filtering / sorting conventions
```

### docs/steering/tech-stack.md Template

```markdown
# Technology Stack

## Overview

Document the technology stack used in this project.

## Backend

<!-- Add backend technologies -->

## Frontend

<!-- Add frontend technologies -->

## Database

<!-- Add database technologies -->

## DevOps

<!-- Add DevOps tools -->
```

### docs/steering/architecture.md Template

```markdown
# System Architecture

## Overview

Document the system architecture and design patterns.

## Architecture Diagram

<!-- Add architecture diagram or description -->

## Layers & Boundaries

- **Presentation / API layer**: `[paths]` — routes, controllers, serializers
- **Application / Service layer**: `[paths]` — use cases, orchestration, business rules
- **Domain layer**: `[paths]` — models, entities, domain services
- **Infrastructure layer**: `[paths]` — DB access, external integrations, queues, caching
- Dependency direction: `[describe which layer may call which; e.g. outer → inner only]`

## Key Components

| Component | Responsibility | Key Files |
|-----------|----------------|-----------|
<!-- Add key components here -->

## Cross-Module Communication

- How modules talk to each other: direct calls, events, queues, HTTP, message broker
- Event / message payloads and where they are published vs consumed
- Shared services vs per-module-owned services

## Data Flow

<!-- Add data flow documentation -->

## Concurrency & Multi-Tenancy Notes

- How state is isolated per tenant/user (e.g. dynamic DB connections, tenant context)
- Locks, transactions, queues, idempotency considerations
```

### docs/issue/README.md Template

```markdown
# Issue Tracking

This folder contains bug reports, root cause analysis, and issue findings.

## Naming Convention

Issue documentation follows the format: `YYYY-MM-DD_issue-name.md`

## Index

<!-- Add issue documentation entries here -->
<!-- Example: -->
<!-- - [2026-08-05_login-authentication-failure](./2026-08-05_login-authentication-failure.md) -->

---

**Catatan**: Buat dokumentasi issue baru dengan format `YYYY-MM-DD_nama-issue.md` saat diminta oleh user.
```

### Issue Documentation Template (YYYY-MM-DD_issue-name.md)

```markdown
# Issue: [Issue Name]

**Date**: YYYY-MM-DD
**Status**: Open
**Severity**: [Low/Medium/High/Critical]
**Reporter**: [Agent/User]

## Problem Description

[Describe the issue or bug clearly]

## Steps to Reproduce

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Expected Behavior

[What should happen]

## Actual Behavior

[What actually happens]

## Root Cause Analysis

[Analysis of the root cause - fill after investigation]

## Solution

[Proposed or implemented solution - fill after fix]

## Verification

[How to verify the fix works]

## Related Files

- [File paths involved in the issue]
```

### Project-Specific Feature Flow Skill Template

```markdown
---
name: {project-name}-feature-flow
description: Workflow for implementing, changing, extending, or refactoring features in {project-name}. Covers current-state documentation, runtime-path tracing, tests, verification, and documentation updates.
---

# {Project Name} Feature Flow

Follow this flow for feature work in this repository.

## 1. Read the current-state docs first

- Start by checking [docs/features/README.md](../../../docs/features/README.md).
- Find the most relevant existing doc with repo terms before coding.
- Also check [docs/steering/](../../../docs/steering/) for architecture, routing, tech-stack, and system-flow context.

## 2. Trace the real runtime path

- Prove the implementation path from the repo, not from assumptions.

## 3. Add or update tests when they materially protect the change

- Treat test evaluation as part of the implementation, not optional follow-up.
- Add a focused test or update an existing one when the change affects behavior that is easy to regress or expensive to verify manually (feature flow, domain rules, calculations, query shaping, persistence, reusable UI logic with meaningful branching).
- Do not force tests for every low-risk edit (copy tweaks, layout-only adjustments, trivial wiring). When you choose not to add tests, state the reason in the completion summary.
- Match the existing test layout in this repo:
  - Unit tests for isolated domain logic, formatting, helpers, enums, support classes.
  - Feature/integration tests for route, controller, DB, end-to-end flow, multi-layer behavior.
  - Follow this repo's existing test conventions (frameworks, base test classes, DB strategy) — check `phpunit.xml` / `jest.config.*` / `pytest.ini` / `vitest.config.*` and existing test files first.
- **If this repo has NO automated test suite:** keep ALL the evaluation rules above; replace ONLY the framework-specific lines with an explicit note — `No automated test suite is configured in this repo.` — plus the repo's real manual verification steps. NEVER delete the evaluation/state-the-reason rules; they still apply.

## 4. Verify the changed path

- Run the focused tests you added or changed; confirm they pass. Repo test command: `[fill in real command during generation, e.g. npm test / npx jest src/__tests__/... / php artisan test]`.
- If no test was added because the change was low-value to cover, verify the path with another focused check matching the risk (manual run, targeted command).
- Prefer targeted tests over broad legacy suites when the broad suite is known to be noisy.

## 5. Update or create docs after implementation

Docs are part of feature work, not optional follow-up. Never leave implementation reflected only in code.

**When creating a NEW feature or a feature not covered by an existing doc:**
1. Create a new numbered feature doc in `docs/features/...md` (sequential numbering, e.g. if highest is `05-...md`, new doc is `06-...md`)
2. Follow the same structure as existing feature docs (flow, routes, domain, UI, data shape)
3. Add an entry + link to that new doc in `docs/features/README.md` index

**When REVISING/CHANGING an existing feature:**
1. Update the existing feature doc in `docs/features/` that covers it
2. REPLACE the `**Recent**:` line in `docs/features/README.md` with ONLY the latest change — one short sentence ≤ 300 chars (never append to it — the line holds just the single most recent change); set `**Updated**:` to today's date
3. If the change affects shared UI AND a `docs/design-system/` folder exists, also update the relevant `docs/design-system/` doc, and REPLACE the `**Updated**:` line in `docs/design-system/README.md` with ONLY today's date + the latest change — one short sentence ≤ 300 chars (never append to it)

**When a bug / root cause is investigated or fixed:**
1. Create `docs/issue/YYYY-MM-DD_nama-issue.md`
2. If it changes feature behavior, update the matching `docs/features/` doc too
<!-- feature-flow-creator v2.4.6 -->
```

## Feature Work — Update & Create Docs (Recurring)

This skill is NOT only for initial scaffolding. On EVERY feature implementation, change, extension, or refactoring task, agent MUST keep docs in sync:

**When creating a NEW feature or a feature not covered by an existing doc:**
1. Create a new numbered feature doc in `docs/features/...md`
2. Use sequential numbering matching existing docs (e.g. if highest is `05-...md`, new doc is `06-...md`)
3. Follow the same structure as existing feature docs (flow, routes, domain, UI, data shape)
4. Add an entry + link to that new doc in `docs/features/README.md` index

**When REVISING/CHANGING an existing feature:**
1. Update the existing feature doc in `docs/features/` that covers it
2. REPLACE the `**Recent**:` line in `docs/features/README.md` with ONLY the latest change — one short sentence ≤ 300 chars (never append to it — the line holds just the single most recent change); set `**Updated**:` to today's date
3. If the change affects shared UI AND a `docs/design-system/` folder exists, also update the relevant `docs/design-system/` doc, and REPLACE the `**Updated**:` line in `docs/design-system/README.md` with ONLY today's date + the latest change — one short sentence ≤ 300 chars (never append to it)

**When a bug / root cause is investigated or fixed:**
1. Create `docs/issue/YYYY-MM-DD_nama-issue.md` (see Issue Documentation Command below)
2. If it changes feature behavior, update the matching `docs/features/` doc too

Do NOT leave implementation reflected only in code. Kept-in-sync docs are part of the feature work, not optional follow-up.

## Issue Documentation Command

**Trigger keywords**: "cek bugs", "cari root cause", "debug error", "fix issue", "investigate masalah"

When user requests bug check or root cause analysis:

1. Auto-create issue documentation file in `docs/issue/`
2. Use naming format: `YYYY-MM-DD_issue-name.md`
3. Issue name should be kebab-case, descriptive of the problem
4. Use template from Issue Documentation Template above

## Stack → Test Command Quick Map

Use these as a starting point when generating the project skill or writing test instructions. ALWAYS verify against the actual repo config (`package.json`, `composer.json`, `phpunit.xml`, `pyproject.toml`/`pytest.ini`, etc.) before instructing the user — the map is a shortcut, not the source of truth.

| Stack | Framework / Runner | Typical test command | Single test / focused run |
|-------|--------------------|----------------------|---------------------------|
| Laravel | PHPUnit | `php artisan test` | `php artisan test --filter=ClassName` |
| Laravel | Pest | `./vendor/bin/pest` | `./vendor/bin/pest tests/Feature/FileTest.php` |
| Node/Express | Jest | `npm test` | `npx jest path/to/file.test.js` |
| Node/NestJS | Jest | `npm test` / `npm run test:e2e` | `npx jest --testPathPattern="file.test.ts"` |
| Node (any) | Vitest | `npm test` / `npx vitest run` | `npx vitest run path/to/file.test.ts` |
| Python (FastAPI/Django) | pytest | `pytest` / `python -m pytest` | `pytest tests/test_file.py::test_func` |
| React/Vite | Vitest | `npm test` / `npx vitest run` | `npx vitest run src/components/X.test.tsx` |
| React | Jest (CRA) | `npm test` | `npm test -- --testPathPattern="X.test.js"` |
| Vue/Nuxt | Vitest | `npm test` / `npx vitest run` | `npx vitest run components/X.test.ts` |
| Go | `go test` | `go test ./...` | `go test ./internal/pkg -run TestName` |

Rules when generating the project skill: if the repo's test framework is detected, write the ACTUAL command into the skill file (like traxex-be got `npm test` + `npx jest src/__tests__/...`). Only fall back to the map when detection is ambiguous.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Missing README.md in subfolders | Always create README.md first in each docs/ subfolder |
| Inconsistent issue naming | Use YYYY-MM-DD_issue-name.md format strictly |
| Empty feature index | Update features/README.md when adding new feature docs |
| `**Recent**:` line keeps growing | REPLACE the `**Recent**:` line with ONLY the latest change (never append); it must always hold just the single most recent change. Update `**Updated**:` to today's date |
| `**Updated**:` line in design-system README grows into a changelog | REPLACE the `**Updated**:` line in `docs/design-system/README.md` with ONLY today's date + the latest change (never append); full history lives in the per-topic docs |
| Missing AGENTS.md / CLAUDE.md | Create AGENTS.md (opencode + Codex) and CLAUDE.md (Claude Code) at project root for AI workflow (both files, same content) |
| Missing project skill | Create .agents/skills/{project-name}-feature-flow/ (opencode + Codex) and .claude/skills/{project-name}-feature-flow/ (Claude Code) automatically (both locations) |
| Not creating doc for a new feature | Create a new numbered doc in docs/features/ + add to index |
| Not updating existing feature doc on change | Update the matching docs/features/ doc + note date in README |
| Leaving implementation only in code | Docs are part of feature work, not optional follow-up |
| docs/features/ left with only README.md | Run feature discovery (Step 4): scan routes/controllers/models and create numbered feature docs |
| Creating design-system for pure backend/API project | Skip docs/design-system entirely when no UI layer exists (Step 2 detection) |
| Rerunning the skill overwrites existing docs | Never overwrite existing docs/**, AGENTS.md, or CLAUDE.md — only create missing files. If the project skill exists, run mode `sync` (refresh the project skill files only), not a full regenerate |
| Project skill stale / missing new sections | Add a `<!-- feature-flow-creator vX.Y -->` marker at the end of the generated skill; on re-run, detect older marker and run mode `sync` to refresh the project skill files in both locations |
| Duplicate feature docs on rediscovery | In mode `setup`, before creating a feature doc, skip any feature already covered by an existing doc in docs/features/ |
| Silently overwriting existing docs without asking | When target docs/AGENTS.md/CLAUDE.md already exist in mode `setup`, STOP and ask the user (overwrite per-file / continue / cancel) before writing anything |
| Overwriting ALL existing docs when the user only wanted a few | When the user chooses "Overwrite", go file-by-file and overwrite only the specific files they select; keep all others untouched |

## Real-World Impact

- Consistent documentation structure across projects
- Easy navigation with README.md index files
- Standardized issue tracking with date-based naming
- Clear separation of concerns (features, steering, issues) + design-system only when UI exists
- Auto-created project-specific skill for feature workflow

