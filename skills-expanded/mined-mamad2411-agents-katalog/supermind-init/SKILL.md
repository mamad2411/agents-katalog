---
name: supermind-init
description: "Initialize a project with Supermind. Use when starting work in a new project, when ARCHITECTURE.md is missing, or when the user wants to set up CLAUDE.md, living documentation, and project health checks. Triggers on: new project setup, missing docs, /supermind-init"
---

# Project Initialization

One command to fully set up a project: creates or updates CLAUDE.md, detects the tech stack, generates living documentation (ARCHITECTURE.md + optional DESIGN.md), and optionally checks project health and discovers relevant tools.

---

## Phase 1: CLAUDE.md Management

Section-level merging preserves your project-specific customizations while keeping infrastructure sections up to date with the latest Supermind configuration.

### Section Ownership

**Project-specific** (preserved during merge — user content takes priority):
- Quick Reference
- Commands
- Tech Stack
- Project Structure
- Any custom section not listed below

**Infrastructure** (replaced from template on every run):
- Shell & Git Permissions
- Worktree Development Workflow
- MCP Servers
- UI Changes
- Living Documentation

### Steps

1. Read the template from `~/.claude/templates/CLAUDE.md`. If missing, tell the user to run `npx supermind-claude` first and stop. **Important:** The template is only a *source* to read from — all writes go to `./CLAUDE.md` in the project root. Never modify the template file at `~/.claude/templates/CLAUDE.md`.

2. Check if `CLAUDE.md` exists in the project root (`./CLAUDE.md`).

3. **No existing CLAUDE.md** — copy the template as-is, then proceed to step 5.

4. **Existing CLAUDE.md** — perform a section-level merge:
   a. Parse both files into sections by splitting on `## ` headings. Content before the first `## ` is the preamble.
   b. Keep the user's preamble intact.
   c. **Project-specific sections**: keep the user's version if it contains real content (not just placeholder comments or "Fill as project grows"). If empty or placeholder, use the template's version.
   d. **Infrastructure sections**: always replace with the template's version.
   e. **Custom sections** (present in the user's file but not in either ownership list): preserve them, append at end.
   f. Output in template section order, with custom sections last.
   g. Show the user a summary: sections preserved / updated / added / kept as custom.

5. Auto-detect project context from manifest files:
   - `package.json` — scripts for Commands, dependencies for Tech Stack
   - `Cargo.toml` — workspace members, dependencies, build targets
   - `go.mod` — module path, dependencies
   - `requirements.txt` / `pyproject.toml` — Python dependencies, scripts
   - `Gemfile` — Ruby dependencies
   - Directory structure for Project Structure section

6. Fill empty or placeholder sections only (never overwrite user content):
   - **Commands**: from package.json scripts, Makefile targets, Cargo commands, etc.
   - **Tech Stack**: from dependencies and config files
   - **Project Structure**: top 2 directory levels, skipping node_modules, dist, .git, .worktrees, build, target, vendor, __pycache__

7. Tell the user what was created or updated and what they should review.

---

## Phase 2: Living Documentation

ARCHITECTURE.md uses tables-over-prose because it saves tokens — the AI reads the file index instead of scanning the entire project. This phase generates AI-optimized documentation from a deep codebase scan.

### Steps

8. **Determine if this is a UI project**:
   - Auto-detect from dependencies: react, vue, svelte, angular, next, nuxt, solid, qwik, lit, stencil
   - If not auto-detected, ask: "Does this project have a UI? (This determines whether a DESIGN.md is created)"

9. **Detect scope**:
   - If not at git root: ask "Document just this subfolder, or the entire repo?"
   - If monorepo indicators exist (`packages/`, `apps/`, `pnpm-workspace.yaml`, workspace configs): ask "Document entire repo, or a specific subfolder?"
   - Otherwise: scan_root = working directory

10. **Check for existing ARCHITECTURE.md**:
    - If found: ask "Keep as-is, or migrate to AI-optimized format?"
    - Keep: skip architecture generation. Migrate: back up to `.bak`, map content into template sections.

11. **Check for existing DESIGN.md** (if UI project):
    - Same keep/migrate flow as above.

12. **Generate files**:

    Read the skeleton templates from this skill's directory before generating:
    - `architecture-template.md` — section structure and table headers for ARCHITECTURE.md
    - `design-template.md` — section structure and table headers for DESIGN.md

    **Empty project** (fewer than 5 source files, excluding config, lock files, and dotfiles):
    - Write from skeleton templates with placeholder comments.

    **Existing project — Deep Scan**:

    Scan exclusions: `node_modules/`, `dist/`, `build/`, `.git/`, `__pycache__/`, `target/`, `vendor/`, `.next/`, `coverage/`, gitignored paths

    Scan limits:
    - Cap File Index at 200 entries (shallower files first)
    - Max 5 directory levels deep
    - Priority order: File Index + Tech Stack, then API Contracts + Env Vars, then Dependencies & Data Flow

    ARCHITECTURE.md scan targets:

    | Scan | How | Section |
    |------|-----|---------|
    | Source files | Glob, read headers/exports | **File Index** |
    | Tech stack | Read package.json, Cargo.toml, go.mod, etc. | **Tech Stack** |
    | API routes | Find route/endpoint definitions | **API Contracts** |
    | Env vars | Read .env.example, grep process.env / os.environ | **Environment Variables** |
    | Import graph | Read import/require statements | **Dependencies & Data Flow** |
    | Code patterns | Observe conventions (naming, error handling, state management) | **Key Patterns & Conventions** |

    DESIGN.md scan targets (if UI project):

    | Scan | How | Section |
    |------|-----|---------|
    | Colors | CSS custom properties, Tailwind config, theme files | **Color Tokens** |
    | Typography | Font declarations, heading styles, text utilities | **Typography** |
    | Spacing | CSS custom properties, Tailwind spacing config | **Spacing Scale** |
    | Components | Component files, variants, props interfaces | **Component Patterns** |
    | Layout | Grid systems, breakpoints, container max-widths | **Layout Conventions** |
    | Animations | Transitions, keyframes, motion variants | **Animation Patterns** |

    Leave unfilled sections with `<!-- No [X] detected -->`.

13. **Verify generated documentation**:
    - Re-read the generated ARCHITECTURE.md (and DESIGN.md if created)
    - Spot-check at least 5 claims (or 10% of all claims, whichever is larger) against actual source code: verify constant names, function signatures, dependency lists, and behavioral descriptions match the source
    - If discrepancies are found, fix each one and tell the user what was wrong and what was corrected
    - If more than 30% of checked claims are wrong, warn the user that generation quality was low and suggest reviewing the full document manually

14. **Commit** generated or migrated docs:
    - New project: `git commit -m "Initialize project (CLAUDE.md, ARCHITECTURE.md[, DESIGN.md])"`
    - Migrated: `git commit -m "Migrate living documentation to AI-optimized format"`

---

## Phase 3: Project Health & Discovery

Different projects benefit from different tools. A database-heavy project might want a Postgres MCP, while a frontend project might want shadcn component search. This phase checks your setup and suggests relevant additions.

### Steps

15. Ask the user: "Would you like me to check your Supermind setup and research additional tools for this project?"

16. **If yes**:

    a. **Verify session hooks are firing**:
       - Check `~/.claude/sessions/` for recent session files
       - If no recent files found, warn that session persistence may not be configured

    b. **Set up Serena** (semantic code navigation):
       - Check if `.serena/` directory exists in the project root
       - If already present, tell the user: "Serena directory already configured."
       - If missing, create it: `mkdir -p .serena/memories`
       - Verify `.serena/` is in `.gitignore` — if not, add it and commit
       - Tell the user: "Created `.serena/` for semantic code navigation."

    c. **Research relevant tools** — dispatch **two parallel agents**:

       **Agent 1: Skills research**
       - Search for Superpowers skills and Claude plugins relevant to the detected tech stack
       - Consider the project's language, framework, testing approach, and deployment target
       - Check installed vs. available skills and identify gaps

       **Agent 2: MCP servers research**
       - Search for MCP servers relevant to the detected tech stack
       - Consider database, API, deployment, and tooling needs
       - Check installed vs. available MCPs and identify gaps
       - **Exclusion:** Never recommend `sequential-thinking-mcp` — it is incompatible with Supermind's skill system

    d. **Present findings** (after both agents complete):
       - Combine results from both agents into a unified list
       - Show suggestions grouped by category: code navigation, testing, deployment, UI, database, etc.
       - Include a brief explanation of why each tool is relevant to this project
       - Do not auto-install anything — let the user decide

17. **If no**: skip this phase. Initialization is complete.

---

## Template Reference

Skeleton templates are sibling files in this skill's directory:
- `architecture-template.md` — sections and table headers for ARCHITECTURE.md
- `design-template.md` — sections and table headers for DESIGN.md

Read these before generating files to match the expected format.
